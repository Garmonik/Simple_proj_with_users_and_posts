from django.contrib import admin

from facecontrol.models import CodeEmail


# Register your models here.
@admin.register(CodeEmail)
class CodeEmailAdmin(admin.ModelAdmin):
    search_fields = ['email', 'code']
