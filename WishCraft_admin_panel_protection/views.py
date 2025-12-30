from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from django.conf import settings
from .models import AdminPanelWhitelist
from django.utils import timezone


def activate_user_sessions(request, token):
    try:
        serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
        token_data = serializer.loads(token, max_age=3600)  # 1 hour expiry
        user_id = token_data['user_id']

    except BadSignature:
        return HttpResponse('Invalid token!', status=400)

    except SignatureExpired:
        return HttpResponse('Token has expired!', status=400)

    except Exception:
        return HttpResponse('An unexpected error occurred.', status=500)

    try:
        whitelist_entry = get_object_or_404(AdminPanelWhitelist, user_id=user_id)

        user = whitelist_entry.user

        if whitelist_entry is None:
            return HttpResponse('Whitelist entry not found.', status=404)

        elif user.id != int(user_id):
            return HttpResponse('Token does not match the user. Invalid Token.', status=403)

        elif not whitelist_entry.status:
            return HttpResponse('User is blocked.', status=403)

        elif whitelist_entry.active_on is not None:
            return HttpResponse(f'Activation link is already used. It was used on {whitelist_entry.active_on}', status=403)

        else:
            ipv4_address = get_ipv4_address(request)
            user_agent = request.META.get('HTTP_USER_AGENT', 'None')
            current_time = timezone.now()

            request.session['admin_panel_session_data'] = {
                'user_id': user.id,
                'whitelist_id': whitelist_entry.id,
                'activated_at': str(current_time),
            }


            whitelist_entry.user.is_active = True
            whitelist_entry.is_active = True
            whitelist_entry.active_on = current_time
            whitelist_entry.ipv4_address = ipv4_address
            whitelist_entry.user_agent = user_agent

            whitelist_entry.save(update_fields=['active_on', 'ipv4_address',  'user_agent', 'is_active'])
            whitelist_entry.user.save(update_fields=['is_active'])

            return HttpResponse('User session activated successfully for admin panel access.', status=200)

    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)

def get_ipv4_address(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

