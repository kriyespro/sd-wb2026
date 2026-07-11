# Agency roles
ROLE_SUPER_ADMIN = 'super_admin'
ROLE_DIRECTOR = 'director'
ROLE_SALES = 'sales_executive'
ROLE_PM = 'project_manager'
ROLE_ACCOUNT_MANAGER = 'account_manager'
ROLE_SEO = 'seo_specialist'
ROLE_GOOGLE_ADS = 'google_ads_specialist'
ROLE_META_ADS = 'meta_ads_specialist'
ROLE_WEB_DEV = 'web_developer'
ROLE_DESIGNER = 'ui_ux_designer'
ROLE_CONTENT = 'content_writer'
ROLE_QA = 'qa_specialist'

# Academy roles
ROLE_ACADEMY_ADMIN = 'academy_admin'
ROLE_MENTOR = 'mentor'
ROLE_TRAINER = 'trainer'
ROLE_STUDENT = 'student'
ROLE_INTERN = 'intern'
ROLE_PLACEMENT = 'placement_coordinator'

# Client roles
ROLE_CLIENT_OWNER = 'client_owner'
ROLE_CLIENT_MEMBER = 'client_member'

# Partner / DGC
ROLE_PARTNER = 'partner'

ROLE_CHOICES = [
    (ROLE_SUPER_ADMIN, 'Super Admin'),
    (ROLE_DIRECTOR, 'Director'),
    (ROLE_SALES, 'Sales Executive'),
    (ROLE_PM, 'Project Manager'),
    (ROLE_ACCOUNT_MANAGER, 'Account Manager'),
    (ROLE_SEO, 'SEO Specialist'),
    (ROLE_GOOGLE_ADS, 'Google Ads Specialist'),
    (ROLE_META_ADS, 'Meta Ads Specialist'),
    (ROLE_WEB_DEV, 'Web Developer'),
    (ROLE_DESIGNER, 'UI/UX Designer'),
    (ROLE_CONTENT, 'Content Writer'),
    (ROLE_QA, 'QA Specialist'),
    (ROLE_ACADEMY_ADMIN, 'Academy Admin'),
    (ROLE_MENTOR, 'Mentor'),
    (ROLE_TRAINER, 'Trainer'),
    (ROLE_STUDENT, 'Student'),
    (ROLE_INTERN, 'Intern'),
    (ROLE_PLACEMENT, 'Placement Coordinator'),
    (ROLE_CLIENT_OWNER, 'Business Owner'),
    (ROLE_CLIENT_MEMBER, 'Team Member'),
    (ROLE_PARTNER, 'DGC (Digital Growth Consultant)'),
]

CLIENT_ROLES = {ROLE_CLIENT_OWNER, ROLE_CLIENT_MEMBER}
STUDENT_ROLES = {ROLE_STUDENT, ROLE_INTERN}
PARTNER_ROLES = {ROLE_PARTNER}
OPS_ROLES = {
    ROLE_SUPER_ADMIN, ROLE_DIRECTOR, ROLE_SALES, ROLE_PM, ROLE_ACCOUNT_MANAGER,
    ROLE_SEO, ROLE_GOOGLE_ADS, ROLE_META_ADS, ROLE_WEB_DEV, ROLE_DESIGNER,
    ROLE_CONTENT, ROLE_QA, ROLE_ACADEMY_ADMIN, ROLE_MENTOR, ROLE_TRAINER,
    ROLE_PLACEMENT,
}

PORTAL_CLIENT = 'client'
PORTAL_STUDENT = 'student'
PORTAL_OPS = 'ops'
PORTAL_PARTNER = 'partner'

PORTAL_URL_NAMES = {
    PORTAL_CLIENT: 'clients:dashboard',
    PORTAL_STUDENT: 'academy_dashboard:dashboard',
    PORTAL_OPS: 'operations:dashboard',
    PORTAL_PARTNER: 'partners:dashboard',
}

PORTAL_PATHS = {
    PORTAL_CLIENT: '/dashboard/client/',
    PORTAL_STUDENT: '/dashboard/student/',
    PORTAL_OPS: '/ops/',
    PORTAL_PARTNER: '/dashboard/dgc/',
}
