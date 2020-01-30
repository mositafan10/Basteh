from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseModel (models.Model):

    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Profile (BaseModel):
    user = models.OneToOneField(User, on_delete=models.PROTECT,)
    picture = models.FileField("picture_of_profile",)
    id_cart = models.FileField("id_cart",)
    country_of_living = models.CharField("user_country", max_length=10)


class Social(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="social_id_of_user")
    title = models.CharField(max_length=10)
    social_username = models.CharField(max_length=35)


class Score(BaseModel):

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_give_score')
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_recieve_score')
    score_of_user = models.IntegerField("score_of_user",)


class CommentUser(BaseModel):

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_give_comment")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_receive_comment")
    comment_on_user = models.TextField("comment_on_user")
