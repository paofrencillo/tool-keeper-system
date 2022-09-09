from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    tupc_id = models.BigIntegerField(primary_key=True)
    year_course = models.CharField(max_length=20)
    role = models.CharField(max_length=11)


class Tools(models.Model):
    tool_id = models.BigIntegerField(primary_key=True)
    tool_name = models.CharField(unique=True)
    tool_image = models.ImageField(upload_to='imgs/', null=False, blank=False)
    storage = models.CharField(max_length=10)
    layer = models.CharField(max_length=8)
    status = models.CharField(max_length=25)


class Transactions(models.Model):
    borrower_id = models.ForeignKey(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=255)
    year_course = models.CharField(max_length=20)
    borrow_datetime = models.DateTimeField()
    return_datetime = models.DateTimeField()
    status = models.CharField(max_length=25, default="AVAILABLE")


class ToolsBorrowed(models.Model):
    transaction_id = models.ForeignKey(Transactions, on_delete=models.CASCADE)
    tool_id = models.ForeignKey(Tools, on_delete=models.CASCADE)
