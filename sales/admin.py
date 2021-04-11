from django.contrib import admin
from sales import models

# Register your models here.
admin.site.register(models.Custumer)
admin.site.register(models.Campuses)
admin.site.register(models.Classlist)
admin.site.register(models.UserInfo)

admin.site.register(models.ConsultRecord)
admin.site.register(models.Enrollment)
admin.site.register(models.CourseRecord)
admin.site.register(models.StudyRecord)

class PermissionAdmin(admin.ModelAdmin):
    # list_display = ['url']
    list_display = ['id','url','is_menu','title']
    list_editable = ['is_menu']
##rbac
admin.site.register(models.Role)
admin.site.register(models.Permission,PermissionAdmin)
admin.site.register(models.Menu)