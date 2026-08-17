from datetime import timedelta

from django.db.models import Count, Q, Sum
from django.utils import timezone

from users.roles import STUDENT_ROLES
from users.models import Profile

from .models import StudentLead, StudentProject, StudentTask, Submission, TeachingSession

PILLAR_WEIGHTS = {
    'learn': 25,
    'teach': 20,
    'field': 25,
    'earn': 30,
}

LEVEL_EXCELLENT = 'excellent'
LEVEL_GOOD = 'good'
LEVEL_DEVELOPING = 'developing'
LEVEL_AT_RISK = 'at_risk'


def pillar_status(user, on_date):
    return {
        'learn': Submission.objects.filter(user=user, submitted_at__date=on_date).exists(),
        'teach': TeachingSession.objects.filter(user=user, created_at__date=on_date).exists(),
        'field': StudentLead.objects.filter(user=user).filter(
            Q(created_at__date=on_date) | Q(updated_at__date=on_date),
        ).exists(),
        'earn': StudentTask.objects.filter(
            user=user, stage=StudentTask.STAGE_EARN, status=StudentTask.STATUS_DONE,
            completed_at__date=on_date,
        ).exists(),
    }


def _empty_pillars():
    return {'learn': False, 'teach': False, 'field': False, 'earn': False}


def _bulk_pillar_hits(user_ids, start_date, end_date):
    """Same evidence rules as pillar_status(), but for many users and many
    days at once: one query per evidence model instead of one query per
    pillar per user per day. Returns {(user_id, date): {pillar: bool}}."""
    user_ids = list(user_ids)
    hits = {}
    if not user_ids:
        return hits

    def mark(user_id, on_date, pillar):
        hits.setdefault((user_id, on_date), _empty_pillars())[pillar] = True

    for user_id, d in Submission.objects.filter(
        user_id__in=user_ids,
        submitted_at__date__gte=start_date, submitted_at__date__lte=end_date,
    ).values_list('user_id', 'submitted_at__date'):
        mark(user_id, d, 'learn')

    for user_id, d in TeachingSession.objects.filter(
        user_id__in=user_ids,
        created_at__date__gte=start_date, created_at__date__lte=end_date,
    ).values_list('user_id', 'created_at__date'):
        mark(user_id, d, 'teach')

    for user_id, created_d, updated_d in StudentLead.objects.filter(user_id__in=user_ids).filter(
        Q(created_at__date__range=(start_date, end_date)) | Q(updated_at__date__range=(start_date, end_date)),
    ).values_list('user_id', 'created_at__date', 'updated_at__date'):
        if start_date <= created_d <= end_date:
            mark(user_id, created_d, 'field')
        if start_date <= updated_d <= end_date:
            mark(user_id, updated_d, 'field')

    for user_id, d in StudentTask.objects.filter(
        user_id__in=user_ids, stage=StudentTask.STAGE_EARN, status=StudentTask.STATUS_DONE,
        completed_at__date__gte=start_date, completed_at__date__lte=end_date,
    ).values_list('user_id', 'completed_at__date'):
        mark(user_id, d, 'earn')

    return hits


def _score_from_status(status):
    return sum(PILLAR_WEIGHTS[pillar] for pillar, done in status.items() if done)


def _avg_score_from_hits(user_id, hits, today, days):
    scores = [
        _score_from_status(hits.get((user_id, today - timedelta(days=n)), _empty_pillars()))
        for n in range(days)
    ]
    return round(sum(scores) / len(scores)) if scores else 0


def daily_score(user, on_date=None):
    on_date = on_date or timezone.localdate()
    status = pillar_status(user, on_date)
    return sum(PILLAR_WEIGHTS[pillar] for pillar, done in status.items() if done)


def score_level(score):
    if score >= 85:
        return LEVEL_EXCELLENT
    if score >= 70:
        return LEVEL_GOOD
    if score >= 50:
        return LEVEL_DEVELOPING
    return LEVEL_AT_RISK


def rolling_average(user, days=7):
    today = timezone.localdate()
    hits = _bulk_pillar_hits([user.id], today - timedelta(days=days - 1), today)
    return _avg_score_from_hits(user.id, hits, today, days)


def _active_students():
    return Profile.objects.filter(role__in=STUDENT_ROLES).select_related('user')


def get_leaderboard(days=7):
    leads_won = dict(
        StudentLead.objects.filter(status=StudentLead.STATUS_WON)
        .values_list('user_id')
        .annotate(n=Count('id'))
        .values_list('user_id', 'n'),
    )
    revenue = dict(
        StudentProject.objects.values_list('user_id')
        .annotate(s=Sum('revenue_collected'))
        .values_list('user_id', 's'),
    )
    projects_active = dict(
        StudentProject.objects.filter(status=StudentProject.STATUS_ACTIVE)
        .values_list('user_id')
        .annotate(n=Count('id'))
        .values_list('user_id', 'n'),
    )

    students = list(_active_students())
    today = timezone.localdate()
    hits = _bulk_pillar_hits(
        [p.user_id for p in students], today - timedelta(days=days - 1), today,
    )

    rows = []
    for profile in students:
        user = profile.user
        rows.append({
            'user': user,
            'avg_score': _avg_score_from_hits(user.id, hits, today, days),
            'leads_won': leads_won.get(user.id, 0),
            'revenue': revenue.get(user.id, 0),
            'projects_active': projects_active.get(user.id, 0),
        })
    rows.sort(key=lambda r: r['avg_score'], reverse=True)
    return rows


def get_batch_health():
    today = timezone.localdate()
    students = [p.user for p in _active_students()]
    total = len(students)
    if total == 0:
        return {
            'total_students': 0,
            'pillar_rates': {p: 0 for p in PILLAR_WEIGHTS},
            'avg_score': 0,
        }

    hits = _bulk_pillar_hits([u.id for u in students], today, today)
    pillar_hits = {p: 0 for p in PILLAR_WEIGHTS}
    score_sum = 0
    for user in students:
        status = hits.get((user.id, today), _empty_pillars())
        for pillar, done in status.items():
            if done:
                pillar_hits[pillar] += 1
        score_sum += _score_from_status(status)

    return {
        'total_students': total,
        'pillar_rates': {p: round(hits / total * 100) for p, hits in pillar_hits.items()},
        'avg_score': round(score_sum / total),
    }


def pending_teaching_evaluations():
    return TeachingSession.objects.filter(
        status=TeachingSession.STATUS_SUBMITTED,
    ).select_related('user').order_by('created_at')


def get_score_history(user, days=30):
    today = timezone.localdate()
    hits = _bulk_pillar_hits([user.id], today - timedelta(days=days - 1), today)
    history = []
    for n in range(days - 1, -1, -1):
        on_date = today - timedelta(days=n)
        status = hits.get((user.id, on_date), _empty_pillars())
        history.append({'date': on_date, 'score': _score_from_status(status), 'pillars': status})
    return history


def current_streak(user, max_days=365):
    today = timezone.localdate()
    hits = _bulk_pillar_hits([user.id], today - timedelta(days=max_days - 1), today)
    streak = 0
    for n in range(0, max_days):
        status = hits.get((user.id, today - timedelta(days=n)), _empty_pillars())
        if _score_from_status(status) > 0:
            streak += 1
        else:
            break
    return streak


def get_activity_feed(user, limit=30):
    from .models import ActivityLog, StudentLead, StudentTask, Submission, TeachingSession

    items = []
    for submission in Submission.objects.filter(user=user).select_related('assignment')[:limit]:
        items.append({
            'pillar': 'learn',
            'title': f'Submitted: {submission.assignment.title}',
            'detail': submission.content[:140],
            'timestamp': submission.submitted_at,
            'source': 'submission',
        })
    for session in TeachingSession.objects.filter(user=user)[:limit]:
        title = f'Taught: {session.topic}'
        if session.status == TeachingSession.STATUS_EVALUATED:
            title += f' — scored {session.score}/100'
        items.append({
            'pillar': 'teach',
            'title': title,
            'detail': session.explanation[:140],
            'timestamp': session.created_at,
            'source': 'teaching',
        })
    for lead in StudentLead.objects.filter(user=user)[:limit]:
        items.append({
            'pillar': 'field',
            'title': f'Lead: {lead.business_name} — {lead.get_status_display()}',
            'detail': lead.notes[:140],
            'timestamp': lead.updated_at,
            'source': 'lead',
        })
    for task in StudentTask.objects.filter(
        user=user, stage=StudentTask.STAGE_EARN, status=StudentTask.STATUS_DONE,
        completed_at__isnull=False,
    )[:limit]:
        items.append({
            'pillar': 'earn',
            'title': f'Completed: {task.title}',
            'detail': task.description[:140],
            'timestamp': task.completed_at,
            'source': 'task',
        })
    for log in ActivityLog.objects.filter(user=user)[:limit]:
        items.append({
            'pillar': log.pillar,
            'title': log.title,
            'detail': log.details[:140],
            'timestamp': log.logged_at,
            'source': 'note',
        })

    items.sort(key=lambda item: item['timestamp'], reverse=True)
    return items[:limit]


def get_pillar_totals(user):
    from .models import ActivityLog, StudentLead, StudentTask, Submission, TeachingSession

    return {
        'learn': Submission.objects.filter(user=user).count(),
        'teach': TeachingSession.objects.filter(user=user).count(),
        'field': StudentLead.objects.filter(user=user).count(),
        'earn': StudentTask.objects.filter(
            user=user, stage=StudentTask.STAGE_EARN, status=StudentTask.STATUS_DONE,
        ).count(),
        'notes': ActivityLog.objects.filter(user=user).count(),
    }
