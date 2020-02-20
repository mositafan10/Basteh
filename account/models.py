from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator, MinValueValidator

# from django.contrib.auth.models import BaseUserManager  : why we don't use this ?

User = get_user_model() 

SOCIAL = [
    ('0','Facebook'),
    ('1','Instagram'),
    ('2','Twitter'),
    ('3','Telegram'),
    ('4','Linkidin'),
]

# should be check due to bussines TODO
Level = [ 
    ('1','Gold'),
    ('2','Silver'),
    ('3','Bronz'),
]

class BaseModel (models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Profile (BaseModel):
    user    = models.OneToOneField(User, on_delete=models.PROTECT)
    picture = models.ImageField(blank=True) # should validate size TODO
    id_cart = models.ImageField(blank=True) # should validate size TODO
    country = models.ForeignKey('Country', on_delete=models.CASCADE, blank=True)
    city    = models.ForeignKey('City', on_delete=models.CASCADE, blank=True)
    phone   = PhoneNumberField()
    birthday = models.DateField(blank=True)
    level = models.CharField(max_length=1, choices=Level)
    favorite_gift = models.CharField(max_length=50)
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.user)
        
class Social(BaseModel):  
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=10, choices=SOCIAL)
    social_id = models.CharField(max_length=20)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

class Score(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='score_receiver')
    score = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ]) 

    def __str__(self):
        return "%s --> %s" %(self.owner ,self.reciever)

    # we need to calculate average score for each user TODO
    # @property
    # def calculated_score(self):
    #     score_sum = 0
    #     queryset = Score.objects.filter(owner=self.owner)
    #     for i in queryset.score:
    #         score_sum = score_sum + i
    #         count = Score.objects.count()
    #         avg = score_sum/count
    #     return avg
    
class CommentUser(BaseModel): # each user should comment for a person just one time TODO
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_give_comment")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_receive_comment")
    comment = models.TextField()
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return "%s --> %s" %(self.owner ,self.receiver)
    
    # we need to calculate the number of comment for each user TODO
    
    # def calculate_comment(cls,user):
    #     return cls.objects.filter(owner=user).count()
    

class Follow(BaseModel): # are we need a model for unfollow ? TODO
    follower  = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    
    def __str__(self):
        return "%s --> %s" %(self.follower ,self.following)

    # we need to calculate the count of folowing and follower for each user TODO
    def following_count(self,user):
        pass
    def follower_count(self,user):
        pass

class Country(BaseModel):
    name = models.CharField(max_length=15)
    # is_active
    def __str__(self):
        return self.name

# we need a mathode to list the cities of a country for select by user TODO

class City(BaseModel): 
    name = models.CharField(max_length=20)  
    country = models.ForeignKey(Country, on_delete=models.CASCADE) 
    # is_active
    def __str__(self):
        return self.name

   
