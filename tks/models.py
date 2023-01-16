import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    tupc_id = models.IntegerField(default=None, null=True, blank=True, unique=True)
    role = models.CharField(max_length=225)
    year_course = models.CharField(max_length=20, null=True)
    user_img = models.ImageField(upload_to='profile_pics/', default=None, null=True, blank=True)
    has_ongoing_transaction = models.BooleanField(default=False)

class Tools(models.Model):
    tool_id = models.BigIntegerField(primary_key=True)
    tool_name = models.CharField(max_length=25, unique=False)
    tool_image = models.ImageField(upload_to='tool_images/', null=False, blank=False)
    storage = models.IntegerField()
    layer = models.IntegerField()
    current_user = models.ForeignKey("User", to_field="tupc_id", on_delete=models.CASCADE, null=True, default=None)
    current_transaction = models.ForeignKey("Transactions", on_delete=models.CASCADE, null=True, default=None)
    status = models.CharField(max_length=25, default="AVAILABLE")
    is_removed = models.BooleanField(default=False)
    is_under_maintenance = models.BooleanField(default=False)

class ToolQuantity(models.Model):
    tool_name = models.CharField(max_length=255)
    quantity = models.IntegerField()

class ReservedTools(models.Model):
    transaction_id = models.ForeignKey("Transactions", on_delete=models.DO_NOTHING)
    tool_name = models.CharField(max_length=255)

class VoidedTransactions(models.Model):
    transaction_id = models.ForeignKey("Transactions", on_delete=models.CASCADE)
    tool_name = models.CharField(max_length=255)

class Transactions(models.Model):
    transaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    entry_datetime = models.DateTimeField()
    tupc_id = models.ForeignKey("User", to_field="tupc_id", related_name="tupc_ids", on_delete=models.CASCADE)
    expected_borrow = models.DateTimeField()
    expected_return = models.DateTimeField()
    actual_borrowed = models.DateTimeField(null=True, default=None)
    actual_returned = models.DateTimeField(null=True, default=None)
    voided_on = models.DateTimeField(null=True, default=None)
    status = models.CharField(max_length=25)
    voided_by = models.ForeignKey("User", related_name="voided_bys", default=None, null=True, on_delete=models.CASCADE)

class FinishedTransactions(models.Model):
    transaction_id = models.ForeignKey("Transactions", on_delete=models.CASCADE)
    tool_borrowed = models.ForeignKey("Tools", on_delete=models.CASCADE)
    tool_status = models.CharField(max_length=25)

class RpiIP(models.Model):
    ip_address = models.CharField(max_length=255, default=None)