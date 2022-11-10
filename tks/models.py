from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    tupc_id = models.BigIntegerField(primary_key=True)
    role = models.CharField(max_length=10)
    year_course = models.CharField(max_length=20, null=True)

class Tools(models.Model):
    tool_id = models.BigIntegerField(primary_key=True)
    tool_name = models.CharField(max_length=25, unique=True)
    tool_image = models.ImageField(upload_to='imgs/', null=False, blank=False)
    storage = models.IntegerField()
    layer = models.IntegerField()
    status = models.CharField(max_length=25, default="AVAILABLE")

class Transactions(models.Model):
    transaction_id = models.BigAutoField(primary_key=True)
    tupc_id = models.ForeignKey("User", on_delete=models.CASCADE)
    borrow_datetime = models.DateTimeField()
    return_datetime = models.DateTimeField()
    status = models.CharField(max_length=25)


class TransactionDetails(models.Model):
    transaction_id = models.ForeignKey("Transactions", on_delete=models.CASCADE)
    tool_id = models.ForeignKey("Tools", on_delete=models.CASCADE)
