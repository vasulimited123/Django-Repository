from django.contrib import admin
from django.contrib.auth import get_user_model
from account.models import UserDetails
from .models import *
from django.utils.html import format_html


class UserAdmin(admin.ModelAdmin):
    list_display = ('id','email','is_deleted','created_at','company','buttonClick')
    list_display_links = ('email','id')
    list_filter = ('is_deleted','created_at')
    radio_fields = {"tags":admin.VERTICAL}
    search_fields = ['tags']
    def less(self,obj):
        return format_html(f'<span style ="color:green">{obj.last_name[0:2]}</span>')
    def buttonClick(self,obj):
        return format_html(f'<a href = "/admin/account/user/{obj.id}/change/">View</a>')  



    


admin.site.register(get_user_model(),UserAdmin)
admin.site.register(UserDetails)