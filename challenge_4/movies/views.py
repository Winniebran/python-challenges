from rest_framework.views import APIView, Response, Request, status
from .serializers import MovieSerializer, MovieOrderSerializer
from .models import Movie
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from movies.permissions import IsAdminOrReadOnly
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination


class MovieView(APIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]

    def get(self, request: Request) -> Response:
        movies = Movie.objects.all().order_by('id')

        result_page = self.paginate_queryset(movies, request, view=self)
        movie_serializer = MovieSerializer(result_page, many=True)
        return self.get_paginated_response(movie_serializer.data)

    def post(self, request: Request) -> Response:
        movie_serializer = MovieSerializer(data=request.data)
        movie_serializer.is_valid(raise_exception=True)
        movie_serializer.save(user=request.user)

        return Response(movie_serializer.data, status.HTTP_201_CREATED)


class MovieDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]

    def get(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)
        movie_serializer = MovieSerializer(movie)

        return Response(movie_serializer.data, status.HTTP_200_OK)

    def delete(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)
        self.check_object_permissions(request, movie)
        movie.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class MovieOrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)

        order_serializer = MovieOrderSerializer(data=request.data)
        order_serializer.is_valid(raise_exception=True)
        order_serializer.save(user=request.user, movie=movie)

        return Response(order_serializer.data, status.HTTP_201_CREATED)
