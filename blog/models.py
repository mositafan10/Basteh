from django.db import models
from account.models import User, BaseModel




class Post(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_of_blog")
    text = models.TextField("text_of_blog")
    pic_of_text = models.FileField("picture_of_text")
    category_of_text = models.CharField(
        "category_of_text", max_length=50)  # need choices
    count_of_visits = models.IntegerField("count_of_visit")
    count_of_comments = models.IntegerField("count_of_comment")


class Comment(BaseModel):

    blog_of_comment = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name="blog_of_comment")
    author_of_comment_on_blog = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author_of_comment_on_blog")
