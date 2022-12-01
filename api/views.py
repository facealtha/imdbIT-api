from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Movie, Favorite
from django.contrib.auth.models import User
from .serializers import MovieSerializer, FavoriteSerializer, UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)

    # This is a decorator for the method below, so that
    # the response is true when a specific movie is
    # provided.
    @action(detail=True, methods=['POST'])
    def favorite_movie(self, request, pk=None):
        movie = get_object_or_404(Movie, pk=pk)
        user = request.user

        if request.method == "POST":
            if Favorite.objects.filter(movie=movie, user=user).exists():
                favorite = Favorite.objects.get(movie=movie, user=user)
                favorite.delete()
                message = {'message: ': 'Unfavorited.'}
                return Response(message, status=status.HTTP_200_OK)
            else:
                favorite = Favorite.objects.create(movie=movie, user=user)
                favorite.save()
                message = {'message: ', 'Favorited.'}
                return Response(message, status=status.HTTP_200_OK)
        else:
            message = {'message: ': 'There was some error.'}
            return Response(message, status.HTTP_400_BAD_REQUEST)



class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        message = {'message': 'You cant update a favorite like this.'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        message = {'message': 'You cant create a favorite like this.'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

