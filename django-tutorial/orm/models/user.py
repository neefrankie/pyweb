import uuid
from django.db import models


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

