# txj/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('user/login/', views.UserLogin.as_view(), name='user_login'),
    path('user/register/', views.UserRegister.as_view(), name='user_register'),
    path('user/forget/', views.UserForget.as_view(), name='user_forget'),
    path('user/photo/', views.UserPhoto.as_view(), name='user_photo'),
    path('user/history/upload/', views.UserHistoryUpload.as_view(), name='user_history_upload'),
    path('user/history/query/', views.UserHistoryQuery.as_view(), name='user_history_query'),
    path('user/comment/', views.UserComment.as_view(), name='user_comment'),

    path('movie/query/', views.MovieQuery.as_view(), name='movie_query'),
    path('movie/upload/', views.MovieUpload.as_view(), name='movie_upload'),
    path('movie/modify/', views.MovieModify.as_view(), name='movie_modify'),
    path('movie/heat/', views.MovieHeat.as_view(), name='movie_heat'),
    path('movie/cover/', views.MovieCover.as_view(), name='movie_cover'),
    path('movie/brief/', views.MovieBrief.as_view(), name='movie_brief'),
    path('movie/date/', views.MovieDate.as_view(), name='movie_date'),
    path('movie/type/', views.MovieType.as_view(), name='movie_type'),
    path('movie/duration/', views.MovieDuration.as_view(), name='movie_duration'),
    path('movie/actor/', views.MovieActor.as_view(), name='movie_actor'),

    path('actor/query/', views.ActorQuery.as_view(), name='actor_query'),
    path('actor/upload/', views.ActorUpload.as_view(), name='actor_upload'),
    path('actor/inmovie/', views.ActorInMovie.as_view(), name='actor_in_movie'),
    path('actor/modify/', views.ActorModify.as_view(), name='actor_modify'),
    path('actor/name/', views.ActorName.as_view(), name='actor_name'),
    path('actor/photo/', views.ActorPhoto.as_view(), name='actor_photo'),
    path('actor/gender/', views.ActorGender.as_view(), name='actor_gender'),
    path('actor/nationality/', views.ActorNationality.as_view(), name='actor_nationality'),
    path('actor/birthdate/', views.ActorBirthdate.as_view(), name='actor_birthdate'),
    path('actor/movie/', views.ActorMovie.as_view(), name='actor_movie'),
]
