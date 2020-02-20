from rest_framework import serializers
from natural_keys import NaturalKeyModelSerializer
from .models import Profile, Social, Score, CommentUser, Country, City, Follow

class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = "__all__"

class ProfileSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    class Meta:
        model = Profile
        fields = ['id', 'user', 'picture', 'id_cart',
                  'country', 'city', 'birthday', 'is_approved']

    # def validate_picture(self,value):
    #     raise serializers.ValidationError("maximum size")
    #     return value


class SocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Social
        fields = ['user', 'title', 'social_id', 'is_approved']


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ['owner', 'receiver', 'score']


class CommentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentUser
        fields = ['owner', 'receiver', 'comment', 'is_approved']




class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['name', 'country']


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['follower', 'following']

 