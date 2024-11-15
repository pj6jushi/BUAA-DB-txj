# txj/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('user/login/', views.UserLogin.as_view(), name='user-login'),
    path('user/register/', views.UserRegister.as_view(), name='user-register'),
    path('user/forget/', views.UserForget.as_view(), name='user-forget'),
    path('user/photo/', views.UserPhoto.as_view(), name='user-photo'),
    path('user/history/upload/', views.UserHistoryUpload.as_view(), name='user-history-upload'),
    path('user/history/query/', views.UserHistoryQuery.as_view(), name='user-history-query'),
    path('user/comment/', views.UserComment.as_view(), name='user-comment'),

    path('movie/query/', views.MovieQuery.as_view(), name='movie-query'),
    path('movie/upload/', views.MovieUpload.as_view(), name='movie-upload'),
    path('movie/modify/', views.MovieModify.as_view(), name='movie-modify'),
    path('movie/heat/', views.MovieHeat.as_view(), name='movie-heat'),
    path('movie/cover/', views.MovieCover.as_view(), name='movie-cover'),
    path('movie/brief/', views.MovieBrief.as_view(), name='movie-brief'),
    path('movie/date/', views.MovieDate.as_view(), name='movie-date'),
    path('movie/type/', views.MovieType.as_view(), name='movie-type'),
    path('movie/duration/', views.MovieDuration.as_view(), name='movie-duration'),
    path('movie/actors/', views.MovieActor.as_view(), name='movie-actors'),

    path('actor/query/', views.ActorQuery.as_view(), name='actor-query'),
    path('actor/upload/', views.ActorUpload.as_view(), name='actor-upload'),
    path('actor/inmovie/', views.ActorInMovie.as_view(), name='actor-in-movie'),
    path('actor/modify/', views.ActorModify.as_view(), name='actor-modify'),
    path('actor/name/', views.ActorName.as_view(), name='actor-name'),
    path('actor/photo/', views.ActorPhoto.as_view(), name='actor-photo'),
    path('actor/gender/', views.ActorGender.as_view(), name='actor-gender'),
    path('actor/nationality/', views.ActorNationality.as_view(), name='actor-nationality'),
    path('actor/birthdate/', views.ActorBirthdate.as_view(), name='actor-birthdate'),
    path('actor/movies/', views.ActorMovie.as_view(), name='actor-movies'),
]
