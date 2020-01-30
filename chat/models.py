from django.db import models
from account.models import User


class BaseChat (models.Model):
    id = models.AutoField(primary_key=True)
    create_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)


class Massaging (BaseChat):

    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sender_of_massage")
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="receiver_of_massage")
    text_of_massage = models.TextField("text_of_massage")
