from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

User = get_user_model()

SOCIAL = [
    ('0', 'Facebook'),
    ('1', 'Instagram'),
    ('2', 'Twitter'),
    ('3', 'Linkdin'),
]

# should be reconsider in future TODO
Level = [
    ('1', 'Gold'),
    ('2', 'Silver'),
    ('3', 'Bronz'),
]

class BaseModel (models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Profile (BaseModel):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    picture = models.ImageField(blank=True, null=True)
    id_cart = models.ImageField(blank=True, null=True)
    country = models.ForeignKey('Country', on_delete=models.CASCADE, blank=True, null=True)
    city = models.ForeignKey('City', on_delete=models.CASCADE, blank=True, null=True)
    phone = PhoneNumberField()
    birthday = models.DateField(blank=True, null=True)
    favorite_gift = models.CharField(max_length=50, blank=True)
    level = models.CharField(max_length=1, choices=Level)
    score = models.DecimalField(default=0.0, max_digits=3, decimal_places=1)
    scores_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)
    follower_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

class Social(BaseModel):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=10, choices=SOCIAL)
    social_id = models.CharField(max_length=20)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)
        

class Score(BaseModel):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='owner')
    reciever = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='score_receiver')
    score = models.PositiveIntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])

    def __str__(self):
        return "%s --> %s" % (self.owner, self.reciever)

    def save(self, *args, **kwargs):
        scores_count = self.reciever.scores_count
        self.reciever.score = (self.reciever.score * scores_count + self.score)/(scores_count + 1)
        self.reciever.scores_count += 1
        self.reciever.save()
        super().save(*args, **kwargs)


class CommentUser(BaseModel):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="user_give_comment")
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="user_receive_comment")
    comment = models.TextField()
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return "%s --> %s" % (self.owner, self.receiver)
    
    def save(self, *args, **kwargs):
        check_duplicate = CommentUser.objects.filter(owner=self.owner, receiver=self.receiver)
        if not check_duplicate:
            self.owner.comment_count += 1
            self.owner.save()
            super().save(*args, **kwargs)
        else:
            raise ValidationError("It's done before. thank you again") # should be changed


class Follow(BaseModel):
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="following")

    def __str__(self):
        return "%s --> %s" % (self.follower, self.following)

    def save(self, *args, **kwargs):
        # if self.follower != self.following:
        self.follower.following_count += 1
        self.follower.save()
        self.following.refresh_from_db()
        self.following.follower_count += 1
        self.following.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # if self.follower != self.following:
        self.follower.following_count -= 1
        self.follower.save()
        self.following.refresh_from_db()
        self.following.follower_count -= 1
        self.following.save()
        super().delete(*args, **kwargs)


class Country(BaseModel):
    name = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def city_list(self):
        return list(Country.objects.city.all())


class City(BaseModel):
    name = models.CharField(max_length=20)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="city")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
