import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    tupc_id = models.BigIntegerField(primary_key=True)
    role = models.CharField(max_length=10)
    year_course = models.CharField(max_length=20, null=True)
    user_img = models.ImageField(upload_to='profile_pics/', null=True)

class Tools(models.Model):
    tool_id = models.BigIntegerField(primary_key=True)
    tool_name = models.CharField(max_length=25, unique=True)
    tool_image = models.ImageField(upload_to='tool_images/', null=False, blank=False)
    storage = models.IntegerField()
    layer = models.IntegerField()
    current_user = models.ForeignKey("User", on_delete=models.CASCADE, null=True, default=None)
    current_transaction = models.ForeignKey("Transactions", on_delete=models.CASCADE, null=True, default=None)
    status = models.CharField(max_length=25, default="AVAILABLE")

class Transactions(models.Model):
    transaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable = False)
    tupc_id = models.ForeignKey("User", on_delete=models.CASCADE)
    borrow_datetime = models.DateTimeField()
    return_datetime = models.DateTimeField()
    status = models.CharField(max_length=25)
    qrcode = models.ImageField(upload_to='qrcodes/', null=False, blank=False)