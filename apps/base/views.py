from datetime import datetime

# from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from apps.usuario.api.serializer import *

from apps.usuario.models import Usuario

# Create your views here.
class Login(ObtainAuthToken):
    def crear_token(self, user):
        return Token.objects.get_or_create(user=user)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            usuario = authenticate(
                username = username,
                password = password
            )

            if usuario:
                if usuario.is_active:
                    token, created = self.crear_token(usuario)
                    usuario_serializer = UsuarioSerializer(usuario, many = True)
                    if created:
                        return Response({
                            'token': token.key,
                            'usuario': usuario_serializer.data,
                            'mensaje': 'Bienvenido a NOUS, es un placer tenerte de vuelta!'
                        }, status=status.HTTP_201_CREATED)
                    else:
                        sessions = Session.objects.filter(expire_date__gte=datetime.now())
                        if sessions:
                            for session in sessions:
                                session_data = session.get_decoded()
                                if usuario.id == int(session_data.get('_auth_user_id')):
                                    session.delete()
                        token.delete()
                        token = Token.objects.create(user=usuario)
                        return Response({
                            'token': token.key,
                            'usuario': usuario_serializer.data,
                            'mensaje': 'Bienvenido a NOUS, es un placer tenerte de vuelta!'
                        }
                else:
                    return Response('error': 'El usuario esta inhabilitado para usar el sistema', status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({'mensaje':'Bienvenido a NOUS, es un placer tenerte de vuelta!'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Usuario o contraseña incorrectos!'}, status=status.HTTP_400_BAD_REQUEST)