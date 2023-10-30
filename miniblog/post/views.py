import cloudinary
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import get_user

from miniblog import settings

from .models import Comment, Image, Post
from .serializers import CommentSerializer, PostSerializer, RegisterSerializer, UserSerializer

from rest_framework.generics import (ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView , ListCreateAPIView, RetrieveAPIView)
# from rest_framework import (viewsets, status)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer  # Importa el serializador predeterminado
from rest_framework_simplejwt.views import TokenViewBase


from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken






class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, )

    def create(self, request, *args, **kwargs):
        # Obtén el usuario actual autenticado como autor
        author = self.request.user

        # Obtén la imagen de la solicitud POST
        image = request.data.get('image')

        # Sube la imagen a Cloudinary
        try:
            upload_result = cloudinary.uploader.upload(image)
            secure_url = upload_result.get('secure_url')
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Crea una instancia de Image para la imagen
        image_instance = Image.objects.create(asset_id=upload_result['asset_id'], secure_url=secure_url)

        # Crea una instancia de Post y asocia la imagen y el author
        data = {
        'title': request.data.get('title'),
        'description': request.data.get('description'),
        'image': image_instance.id,
        }

        # No incluyas el campo 'author' en los datos de entrada, se establecerá automáticamente como el usuario autenticado

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=author)  # Asigna el autor a la instancia de Post
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostListAPIView(ListAPIView):
    """"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer




class PostRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    def get_permissions(self):
        if self.request.method == 'GET':
            # Permitir acceso no autenticado solo para GET (recuperación)
            return []
        else:
            # Requiere autenticación para otros métodos (update, destroy, etc.)
            # return [IsAuthenticated()]
            return []



# Listar todos los comentarios
class CommentListCreateAPIView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    # parser_classes = (FormParser, )
    def create(self, request, *args, **kwargs):
            # Obtener el usuario de la sesión actual
            user = request.user
            # Agregar el usuario al objeto Comment antes de serializarlo
            comment_data = request.data.copy()
            comment_data['author'] = user.id

            serializer = self.get_serializer(data=comment_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# Recuperar, actualizar y eliminar un comentario específico
class CommentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        # Obtiene el access token y el refresh token de la respuesta
        access_token = response.data['access']
        refresh_token = response.data['refresh']

        # Configura la cookie para el refresh token como HttpOnly
        response.set_cookie(
            key='refresh_token',
            value=str(refresh_token),
            expires=None,  # Opcional: configura la expiración si es necesario
            secure=True,    # Configura en True en entornos de producción con HTTPS
            httponly=True,  # Configura en True para habilitar HttpOnly solo para el refresh token
            samesite='Lax',  # Configura según tus necesidades de SameSite
        )

        # Retorna tanto el access token como el refresh token en la respuesta
        return Response({'access_token': access_token, 'refresh_token': refresh_token})

# Ejemplo de github

class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None
    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh_token')
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            raise InvalidToken('No valid token found in cookie \'refresh_token\'')

class CookieTokenObtainPairView(TokenObtainPairView):

    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            # No establezcas max_age o establécelo en None para hacer la cookie de sesión
            response.set_cookie('refresh_token', response.data['refresh'], httponly=True, samesite=None, domain=settings.SIMPLE_JWT['DOMAIN'])
            # response['Access-Control-Allow-Origin'] = '192.168.1.108:5173'
            del response.data['refresh']
        access_token = response.data.get('access')

        if access_token:
            try:
                # Intenta decodificar el token de acceso
                decoded_token = AccessToken(access_token)
                # Obtiene el ID del usuario desde el token
                id = decoded_token['user_id']
                username = decoded_token['username']
                email = decoded_token['email']
                first_name = decoded_token['first_name']
                last_name = decoded_token['last_name']

                response_data = {
                    'user': {
                        'id': id,
                        'username': username,
                        'email': email,
                        'first_name': first_name,
                        'last_name': last_name,
                        'access_token': access_token,
                        # Agrega otros campos de usuario si los deseas
                    }
                }
                response.data['user'] = response_data

            except Exception as e:
                # Maneja cualquier error que pueda ocurrir al decodificar el token
                return Response({'error_message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return super().finalize_response(request, response, *args, **kwargs)


class CookieTokenRefreshView(TokenRefreshView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            cookie_max_age = 3600 * 24 * 14 # 14 days
            response.set_cookie('refresh_token', response.data['refresh'], max_age=cookie_max_age, httponly=True)
            del response.data['refresh']
        return super().finalize_response(request, response, *args, **kwargs)
    serializer_class = CookieTokenRefreshSerializer

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Llama al método create del serializador para crear el usuario
        user = serializer.create(serializer.validated_data)

        # Genera el token de acceso
        refresh = RefreshToken.for_user(user)

        # Agrega los datos del usuario y el token de acceso al diccionario response_data
        response_data = {
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'access_token': str(refresh.access_token),
                # Agrega otros campos de usuario si los deseas
            }
        }

        # Configura la cookie
        cookie_max_age = 3600 * 24 * 14  # 14 days
        response = JsonResponse(response_data)
        response.set_cookie('refresh_token', str(refresh), max_age=cookie_max_age, httponly=True)

        return response

class MyLoginView(APIView):
    def post(self, request):
        serializer = TokenObtainPairSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                refresh = RefreshToken.for_user(user)

                # Serializa los datos del usuario utilizando UserSerializer
                user_data = UserSerializer(user).data

                # Agrega los datos del usuario y el token de acceso a la respuesta JSON
                response_data = {
                    'user': user_data,
                    'access_token': str(refresh.access_token),
                    # Agrega otros campos de respuesta si los deseas
                }

                # Configura la cookie
                cookie_max_age = 3600 * 24 * 14  # 14 days
                response = JsonResponse(response_data)
                response.set_cookie('refresh_token', str(refresh), max_age=cookie_max_age, httponly=True)

                return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request):
        response = JsonResponse({"message": "Refresh token revoked"})
        response.delete_cookie("refresh_token")
        return response
