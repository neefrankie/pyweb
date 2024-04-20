from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from datetime import timezone, datetime, timedelta
import uuid
import secrets

# Create your models here.


# Create your models here.
class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mobile = models.CharField(max_length=32, null=True, unique=True)
    wechat_id = models.CharField(max_length=256, null=True, unique=True)
    email = models.CharField(max_length=64, null=True, unique=True)
    password = models.TextField(null=True)
    emai_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    deleted_at = models.DateTimeField(null=True)

    @classmethod
    def from_email(cls, email: str, pw: str):
        return cls(
            email=email,
            password=make_password(pw)
        )

    def is_password_matched(self, pw: str) -> bool:
        return check_password(self.password, pw)


def generate_token() -> str:
    return secrets.token_hex(32)


class PasswordResetter(models.Model):
    token = models.CharField(max_length=64, unique=True, default=generate_token)
    expires_in = models.IntegerField(default=10800)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    deleted_at = models.DateTimeField(null=True)

    def is_expired(self) -> bool:
        return (datetime.now(timezone.utc) - self.created_at) > timedelta(seconds=self.expires_in)
