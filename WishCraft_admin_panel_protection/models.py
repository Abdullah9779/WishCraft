from django.db import models
from django.contrib.auth.models import User
from itsdangerous import URLSafeTimedSerializer
from django.conf import settings
import uuid

# Create your models here.

class AdminPanelWhitelist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="The user associated with this whitelist entry.")
    ipv4_address = models.GenericIPAddressField(protocol='IPv4', blank=True, null=True, help_text="The IPv4 address for which the admin panel access is being controlled.")
    user_agent = models.CharField(max_length=1024, blank=True, null=True, help_text="The user agent string of the browser/client used to access the admin panel.")
    also_check_ipv4_address = models.BooleanField(default=False, help_text="Indicates whether to also check the IPv4 address when validating admin panel access.")
    activation_url = models.CharField(max_length=255, unique=True, blank=True, help_text="The unique activation URL generated for the user session to access the admin panel. This URL is valid for a limited time.")
    activation_token = models.CharField(max_length=128, unique=True, blank=True, help_text="The unique activation token associated with the activation URL. This token is used to verify the authenticity of the activation request.")
    status = models.BooleanField(default=False, choices=[(True, 'Allowed'), (False, 'Blocked')], help_text="Indicates whether the user session is allowed or blocked from accessing the admin panel.")
    is_active = models.BooleanField(default=False, help_text="Indicates whether the user is currently activated to see the admin panel Browser sessions.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="The timestamp when the whitelist entry was created.")
    active_on = models.DateTimeField(null=True, blank=True, help_text="The timestamp when the user session was activated for admin panel access.")


    def generate_activation_token(self):
        token = URLSafeTimedSerializer(settings.SECRET_KEY).dumps(
            {'user_id': self.user.id, "whitelist_id": self.id, 'uuid': str(uuid.uuid4())}
        )

        self.activation_token = token
        self.activation_url = f"https://wishcraft.pythonanywhere.com/apwlr/{token}"

        self.save(update_fields=['activation_token', 'activation_url'])
        return self.activation_token

    def save(self, *args, **kwargs):
        if self.status and not self.activation_token:
            super().save(*args, **kwargs)
            self.generate_activation_token()
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.ipv4_address}"

