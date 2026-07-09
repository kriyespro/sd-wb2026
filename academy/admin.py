from django.contrib import admin

from .models import (
    AdmissionApplication,
    Assignment,
    Attendance,
    Certificate,
    Course,
    CourseModule,
    Enrollment,
    Lesson,
    MentorAllocation,
    PlacementApplication,
    PortfolioItem,
    StudentProject,
    StudentTask,
    Submission,
)


class CourseModuleInline(admin.TabularInline):
    model = CourseModule
    extra = 0


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'duration_weeks', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [CourseModuleInline]


@admin.register(CourseModule)
class CourseModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    inlines = [LessonInline]


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'status', 'progress_percent', 'enrolled_at')
    list_filter = ('status', 'course')


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'due_date')
    list_filter = ('course',)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'assignment', 'status', 'submitted_at')
    list_filter = ('status',)


@admin.register(StudentTask)
class StudentTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'due_date')
    list_filter = ('status',)


@admin.register(StudentProject)
class StudentProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'project_type', 'status')
    list_filter = ('project_type', 'status')


@admin.register(MentorAllocation)
class MentorAllocationAdmin(admin.ModelAdmin):
    list_display = ('student', 'mentor', 'allocated_at')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_name', 'date', 'status')
    list_filter = ('status',)


@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'issued_at')


@admin.register(PlacementApplication)
class PlacementApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'role', 'status', 'applied_at')
    list_filter = ('status',)


@admin.register(AdmissionApplication)
class AdmissionApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'course_interest', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('name', 'email')
