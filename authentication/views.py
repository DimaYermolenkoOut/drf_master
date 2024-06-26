import jwt
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings

from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import RegisterSerializer, VerifyEmailSerializer, LoginSerializer, \
    PasswordResetSerializer, SetNewPasswordSerializer, PasswordTokenCheckAPISerializer
from .utils import Util
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, smart_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
# from social_django.utils import load_strategy, load_backend
# from social_core.exceptions import MissingBackend
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        user_data['token'] = str(token)

        current_site = get_current_site(request)
        relative_link = reverse('email-verify')
        absurl = 'http://' + current_site.domain + relative_link + "?token=" + str(token)
        email_body = 'Hi ' + user.username + ' Use link below to verify your email \n' + absurl
        data = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': 'Verify your email',
        }

        Util.send_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    serializer_class = VerifyEmailSerializer

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestPasswordResetEmailView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request):
        # data = {'request': request, 'data': request.data}
        serializer = self.serializer_class(data=request.data)
        email = request.data.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)

            current_site = get_current_site(request=request).domain
            relative_link = reverse('password-reset-confirm',
                                    kwargs={'uidb64': uidb64, 'token': token})
            absurl = 'http://' + current_site + relative_link
            email_body = 'Hello \n Use link below to reset your password  \n' + absurl
            data = {
                'email_body': email_body,
                'to_email': user.email,
                'email_subject': 'Reset your password',
            }
            Util.send_email(data)

        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = PasswordTokenCheckAPISerializer
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({'success': True, 'message': 'Credentials Valid', 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)

#
# class GoogleLogin(APIView):
#     def post(self, request):
#         token_id = request.data['tokenId']
#
#         try:
#             strategy = load_strategy(request)
#             backend = load_backend(strategy=strategy, name='google-oauth2', redirect_uri=None)
#
#             user = backend.do_auth(token_id)
#
#             if user and user.is_active:
#                 refresh = RefreshToken.for_user(user)
#                 return Response({
#                     'refresh': str(refresh),
#                     'access': str(refresh.access_token),
#                 }, status=status.HTTP_200_OK)
#
#         except MissingBackend:
#             return Response({'error': 'Ошибка авторизации.'}, status=status.HTTP_400_BAD_REQUEST)
#
#         return Response({'error': 'Ошибка авторизации.'}, status=status.HTTP_400_BAD_REQUEST)
