from rest_framework import serializers
from .models import Profile, Social, Score, CommentUser, Country, City, Follow, User


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["name", "country", "is_active"]


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['name', 'country', "is_active"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        field = "__all__"

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    country = CountrySerializer()
    city = CitySerializer()
    
    class Meta:
        model = Profile
        fields = "__all__"

    def validate_size(fieldfile_obj):
        filesize = fieldfile_obj.size
        KB_limit = 1000
        if KB_limit < filesize:
            raise ValidationError("Max File Size is 1 MB")
            # should be translated TODO


class SocialSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Social
        fields = ['id','user', 'title', 'social_id', 'is_approved']


class CommentUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = CommentUser
        fields = ['id','owner', 'receiver', 'comment', 'is_approved']


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id','follower', 'following']
