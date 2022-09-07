from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    tupc_id = models.BigIntegerField(primary_key=True)
    year_course = models.CharField()
    role = models.CharField()


class Tools(models.Model):
    tool_id = models.BigIntegerField(primary_key=True)
    tool_name = models.CharField()
    tool_image = models.ImageField(upload_to='imgs/', null=False, blank=False)
    storage = models.CharField()
    layer = models.CharField()
    status = models.CharField()


class Transactions(models.Model):
    borrower_id = models.ForeignKey(User, on_delete=models.CASCADE)
    fullname = models.CharField()
    year_course = models.CharField()
    borrow_datetime = models.DateTimeField()
    return_datetime = models.DateTimeField()
    status = models.CharField()


class ToolsBorrowed(models.Model):
    transaction_id = models.ForeignKey(Transactions, on_delete=models.CASCADE)
    tool_id = models.ForeignKey(Tools, on_delete=models.CASCADE)
