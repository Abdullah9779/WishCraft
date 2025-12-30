from .models import AdminPanelWhitelist
from django.shortcuts import render

class AdminPanelProtectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.path.startswith('/admin/'):
            ipv4_address = self.get_ipv4_address(request)
            session_data = request.session.get('admin_panel_session_data')
            if session_data is None:
                return render(request, '404.html', status=404)

            if session_data:
                try:
                    whitelist_entry = AdminPanelWhitelist.objects.get(id=session_data.get('whitelist_id'), user_id=session_data.get('user_id'))
                    registered_ipv4_address = whitelist_entry.ipv4_address

                    if not whitelist_entry.status:
                        return render(request, 'blocked_user_page.html', {'ipv4_address': ipv4_address, "registered_ipv4_address": registered_ipv4_address, "full_name": request.user.get_full_name(), "username": request.user.username}, status=403)

                    if whitelist_entry.also_check_ipv4_address:

                        if registered_ipv4_address != ipv4_address:
                            return render(request, 'ipv4_not_whitelist_page.html', {'ipv4_address': ipv4_address, 'registered_ipv4_address': registered_ipv4_address, "full_name": request.user.get_full_name(), "username": request.user.username}, status=404)

                    if not whitelist_entry.is_active:
                        return render(request, 'in_active_session.html', {'full_name': request.user.get_full_name(), 'username': request.user.username, 'registered_ipv4_address': registered_ipv4_address, 'ipv4_address': ipv4_address}, status=404)

                except AdminPanelWhitelist.DoesNotExist:
                    return render(request, 'not_found_in_whitelist.html', {"ipv4_address": ipv4_address}, status=403)

        response = self.get_response(request)
        return response

    def get_ipv4_address(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

