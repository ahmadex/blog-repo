from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.contrib.auth.models import User
from blog_post.models import BlogUser, BlogPost, Reaction, Comment
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={"input_type": "password"}, validators=[])
    role = serializers.CharField()
    email = serializers.EmailField(required=True,
                                   validators=[
            UniqueValidator(queryset=User.objects.all(), message="This Email already exists.")
        ])

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'password']

    def validate_password(self, value):
        """
        Validate_password to validate the password.
        """
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def create(self, validated_data):
        """
        Create User and Blog User with role.
        """
        role = validated_data.pop('role', BlogUser.UserRole.READER)
        if role not in [BlogUser.UserRole.AUTHOR, BlogUser.UserRole.READER]:
            raise serializers.ValidationError({"Error": "Please select a valid role."})
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        BlogUser.objects.create(user=user, role=role)
        return user

     

class BlogPostSerializer(serializers.ModelSerializer):

    title =  serializers.CharField(validators=[
            UniqueValidator(queryset=BlogPost.objects.select_related("author"), message="This title already exists.")
        ]
    )

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'author', "views", 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    
    def create(self, validated_data):
        """
        Create Post and assign author as current user.
        """
        user = validated_data.pop("user")
        validated_data['author'] = user.bloguser
        post = BlogPost(**validated_data)
        post.save()
        return post
    

class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ['id', 'user', 'post', 'reaction', 'created_at']
        read_only_fields = ['user', 'created_at']



class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ["id", "post", "content", "user"]


class PostStatesSerializer(serializers.ModelSerializer):

    no_of_likes = serializers.SerializerMethodField()
    no_of_comments = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = ["id", "title", "no_of_likes", "no_of_comments", "views"]

    def get_no_of_likes(self, obj):
        return obj.reactions.filter(reaction=Reaction.ReactionChoices.LIKE).count()

    def get_no_of_comments(self, obj):
        if obj.comments:
            return obj.comments.count()