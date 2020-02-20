from django.db import models
from account.models import User, BaseModel 
from django.utils.translation import gettext_lazy as _
from django.core.cache import cache


class Post(BaseModel):
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name="posts")
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name="posts")
    tags = models.ManyToManyField('Tag', related_name="posts")
    pic = models.ImageField(blank=True, null=True, ) # need more arguments (validation,...) TODO
    text = models.TextField()
    score = models.PositiveIntegerField() #limit to 5 TODO
    view_post = models.PositiveIntegerField()
    like_count = models.PositiveIntegerField()
    # do we need dislike field ? TODO
    comment_count = models.PositiveIntegerField()      
    is_approved = models.BooleanField(default=False) #is needed when a user want to insert post

    def __str__(self):
        return "%s" %(self.id)

    def like(self, request):
        ip = request.META.get("HTTP_REMOTE_ADDR")
        model_name = "like"
        key = '%s_%s_%s' % (self.id, model_name, ip)
        if not cache.get(key):
            cache.set(key,True)
            like_count =+ 1
    
    def dislike(self):
        ip = request.META.get("HTTP_REMOTE_ADDR")
        model_name = "dislike"
        key = '%s_%s_%s' % (self.id, model_name, ip)
        if not cache.get(key):
            cache.set(key,True)
            like_count =- 1
    
    def view(self):
        ip = request.META.get("HTTP_REMOTE_ADDR")
        model_name = "view"
        key = '%s_%s_%s' % (self.id, model_name, ip)
        if not cache.get(key):
            cache.set(key,True)
            view_post =+ 1

    def score(self): #score should be insert by users noy anonymous
        ip = request.META.get("HTTP_REMOTE_ADDR")
        model_name = "Score"
        value = "5" # how get ip from client ?
        key = '%s_%s_%s_%s' % (self.id, model_name, value, ip)
        if not cache.get(key):
            cache.set(key,True)
            # how calculate the avg score ?
            

class Category(BaseModel):
    title = models.CharField(max_length=40)
    description = models.TextField(blank=True) # is this needed ? TODO
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
   
    def __str__(self):  
        return self.title

class Tag(BaseModel):
    title = models.CharField(max_length=40)

    def __str__(self):  
        return self.title

class Comment(BaseModel):
    user   = models.ForeignKey(User, on_delete=models.CASCADE)
    post   = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="posts")
    text   = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        return "%s  ->  %s" %(self.user, self.post)

class Score(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="scores")
    post = models.ForeignKey(Post, on_delete=models.PROTECT, related_name="scores")
    value = models.PositiveIntegerField() 

    def __str__(self):
        return "%s  ->  %s" %(self.user,self.post)
    
class Bookmark(BaseModel):
    user = user = models.ForeignKey(User, on_delete=models.PROTECT)
    post = models.ForeignKey(Post, on_delete=models.PROTECT)

    def __str__(self):
        return "%s  ->  %s" %(self.user,self.post)

# class Like(BaseModel):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")

#     def __str__(self):
#         return self.id
