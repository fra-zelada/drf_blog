from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


from .models import Comment, Image, Post

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id' , 'username', 'email', 'first_name', 'last_name')

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'  # Esto incluirá todos los campos, incluido secure_url

class CommentSerializer(serializers.ModelSerializer):
    author_details = UserSerializer(source = 'author', read_only=True)  # Usa el serializador UserSerializer para representar al autor
    class Meta:
        model = Comment
        fields = ('id','text','post', 'author','author_details', "created_at")

class PostSerializer(serializers.ModelSerializer):
    """Post Serializer"""
    comments = CommentSerializer(many=True, read_only=True)
    author_details = UserSerializer(source = 'author', read_only=True)  # Usa el serializador UserSerializer para representar al autor
    class Meta:
        model = Post
        fields = ("id","description", "title", "comments", "image",  "author_details", "created_at")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        image = instance.image
        if image:
            representation['image'] = {
                'asset_id': image.asset_id,
                'secure_url': image.secure_url
            }
        return representation

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Agrega reclamaciones personalizadas
        token['username'] = user.username  # Ejemplo: Agregar el nombre del usuario como reclamación personalizada
        token['email'] = user.email  # Ejemplo: Agregar el nombre del usuario como reclamación personalizada
        token['first_name'] = user.first_name  # Ejemplo: Agregar el nombre del usuario como reclamación personalizada
        token['last_name'] = user.last_name  # Ejemplo: Agregar el nombre del usuario como reclamación personalizada

        # Puedes agregar más reclamaciones personalizadas aquí
        # token['custom_claim'] = ...

        return token


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )


        user.set_password(validated_data['password'])
        user.save()

        return user