from django.contrib import admin
from .models import APCourse, Award, CollegeStats, ExtracurricularActivity

class CollegeStatsAdmin(admin.ModelAdmin):
    list_display = ('id', 'gpa', 'sat', 'act', 'race', 'gender', 'income')

admin.site.register(CollegeStats, CollegeStatsAdmin)

class ExtracurricularActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'activity_name', 'activity_type', 'ranking')

admin.site.register(ExtracurricularActivity, ExtracurricularActivityAdmin)

@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ('award_name', 'award_type', 'ranking', 'user')
    search_fields = ('award_name', 'user__username')

@admin.register(APCourse)
class APCourseAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'score')


