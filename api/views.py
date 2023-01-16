from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from .models import Movie, Rating
from .serializers import MoviesSerializer, RatingSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MoviesSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=["POST"])
    def rate_movie(self, request, pk=None):
        if "stars" in request.data:

            movie = Movie.objects.get(id=pk)
            stars = request.data["stars"]
            user = request.user

            try:
                rating = Rating.objects.get(user=user.id, movie=movie.id)
                rating.stars = stars
                rating.save()
                serilizer = RatingSerializer(rating, many=False)
                response = {"messasge": "Rating updated", "result": serilizer.data}
                return Response(response, status=status.HTTP_200_OK)

            except:
                rating = Rating.objects.create(user=user, movie=movie, stars=stars)
                serilizer = RatingSerializer(rating, many=False)
                response = {"messasge": "Rating created", "result": serilizer.data}
                return Response(response, status=status.HTTP_200_OK)

        else:
            response = {"message": "You need to provide stars"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, )

    def update(self, request, *args, **kwargs):
        response = {"message": "You can't update rating"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        response = {"message": "You can't create rating"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
