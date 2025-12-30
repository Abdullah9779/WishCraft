import os
import shutil
from django.contrib import admin
from django.contrib.sessions.models import Session
from django.contrib import messages
from .models import UsersTemplates
from .utils import get_upload_folder

class UsersTemplatesAdmin(admin.ModelAdmin):
    list_display = ('template_code', 'template_id', 'session_id', 'created_at')
    list_filter = ('template_id', 'created_at')
    search_fields = ('template_code', 'session_id')
    readonly_fields = ('created_at',)

    def delete_model(self, request, obj):
        """Override delete to clean up files and sessions"""
        self.cleanup_template_data(obj)
        super().delete_model(request, obj)
        messages.success(request, f"Template {obj.template_code} and its files deleted successfully.")

    def delete_queryset(self, request, queryset):
        """Override bulk delete to clean up files and sessions"""
        for obj in queryset:
            self.cleanup_template_data(obj)
        super().delete_queryset(request, queryset)
        messages.success(request, f"{queryset.count()} templates and their files deleted successfully.")

    def cleanup_template_data(self, template_obj):
        """Clean up template files and session data"""
        # Delete template files
        upload_folder = get_upload_folder()
        user_folder = os.path.join(upload_folder, template_obj.template_code)

        if os.path.exists(user_folder):
            shutil.rmtree(user_folder)

        # Clean up session data if session exists
        if template_obj.session_id:
            try:
                session = Session.objects.get(session_key=template_obj.session_id)
                session_data = session.get_decoded()

                if 'user-templates' in session_data:
                    user_templates = session_data['user-templates']
                    if template_obj.template_code in user_templates:
                        del user_templates[template_obj.template_code]
                        session_data['user-templates'] = user_templates
                        session.session_data = Session.objects.encode(session_data)
                        session.save()
            except Session.DoesNotExist:
                pass

admin.site.register(UsersTemplates, UsersTemplatesAdmin)
