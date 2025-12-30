from django.contrib import admin
from django.utils.html import format_html
from .models import AdminPanelWhitelist

# Register your models here.

class AdminPanelWhitelistAdmin(admin.ModelAdmin):
    list_display = ('user', 'ipv4_address', 'status', 'activation_token_display', 'activation_url_link', 'is_active', 'also_check_ipv4_address')
    search_fields = ('user__username', 'ipv4_address')
    list_filter = ('status', 'active_on', "is_active", 'also_check_ipv4_address')
    readonly_fields = ('activation_token', 'activation_url', "active_on")
    actions = ['refresh_activation_urls']
    
    def activation_token_display(self, obj):
        if obj.activation_token:
            return obj.activation_token[:15] + '...' if len(obj.activation_token) > 50 else obj.activation_token
        return 'No token'
    activation_token_display.short_description = 'Token'
    
    def activation_url_link(self, obj):
        if obj.activation_url:
            return format_html('<button onclick="navigator.clipboard.writeText(\'{}\')">Copy URL</button>', obj.activation_url)
        return 'No URL'
    activation_url_link.short_description = 'Activation URL'
    
    def refresh_activation_urls(self, request, queryset):
        count = 0
        for obj in queryset:
            obj.is_active = False
            obj.active_on = None
            obj.ipv4_address = None
            obj.also_check_ipv4_address = False
            obj.save(update_fields=['is_active', 'active_on', 'ipv4_address', 'also_check_ipv4_address'])
            obj.generate_activation_token()
            count += 1
        self.message_user(request, f'Successfully refreshed {count} activation URLs.')
    refresh_activation_urls.short_description = 'Refresh activation URLs'
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.status and not obj.activation_token:
            obj.generate_activation_token()
            
    class Meta:
        model = AdminPanelWhitelist
        exclude = ('created_at')
        


admin.site.register(AdminPanelWhitelist, AdminPanelWhitelistAdmin)
