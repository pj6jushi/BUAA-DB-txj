# txj/views.py
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from django.db.models import Q
from django.core.exceptions import ValidationError


class UserLogin(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email)
            if user.passwords == password:  # 简化起见，直接比较密码，实际应加密处理
                return Response({
                    'state': 1,
                    'error': '',
                    'Uid': user.uid
                })
            else:
                return Response({
                    'state': 0,
                    'error': 'Wrong password'
                }, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({
                'state': 0,
                'error': 'User not found'
            }, status=status.HTTP_400_BAD_REQUEST)


class UserRegister(APIView):
    def post(self, request):
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')

        # 检查邮箱是否已注册
        if User.objects.filter(email=email).exists():
            return Response({
                'state': 0,
                'error': 'Email is already registered'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 创建新用户
        try:
            user = User.objects.create(
                name=name,
                email=email,
                passwords=password
            )
            return Response({
                'state': 1,
                'error': '',
                'Uid': user.uid
            })
        except ValidationError as e:
            return Response({
                'state': 0,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class UserForget(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        confirm = request.data.get('confirm')

        # 确保密码和确认密码一致
        if password != confirm:
            return Response({
                'state': 0,
                'error': 'Passwords do not match'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            user.passwords = password
            user.save()
            return Response({
                'state': 1,
                'error': ''
            })
        except User.DoesNotExist:
            return Response({
                'state': 0,
                'error': 'User not found'
            }, status=status.HTTP_400_BAD_REQUEST)


class UserPhoto(APIView):
    def post(self, request):
        uid = request.data.get('Uid')
        photo_url = request.data.get('photoUrl')

        try:
            user = User.objects.get(uid=uid)
            user.photopath = photo_url
            user.save()
            return Response({
                'state': 1,
                'error': ''
            })
        except User.DoesNotExist:
            return Response({
                'state': 0,
                'error': 'User not found'
            }, status=status.HTTP_400_BAD_REQUEST)


class UserHistoryUpload(APIView):
    def post(self, request):
        uid = request.data.get('Uid')
        mid = request.data.get('Mid')
        time = request.data.get('time')

        try:
            user = User.objects.get(uid=uid)
            movie = Movie.objects.get(mid=mid)
            # history = History.objects.create(uid=user, mid=movie, time=time)
            history, created = History.objects.update_or_create(
                uid=user,  # 根据用户ID
                mid=movie,  # 根据电影ID
                defaults={'time': time}  # 更新观看时间
            )
            return Response({
                'state': 1,
                'error': '',
            })
        except User.DoesNotExist:
            return Response({
                'state': 0,
                'error': 'User not found'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Movie.DoesNotExist:
            return Response({
                'state': 0,
                'error': 'Movie not found'
            }, status=status.HTTP_400_BAD_REQUEST)


class UserHistoryQuery(APIView):
    def post(self, request):
        uid = request.data.get('Uid')

        try:
            history = History.objects.filter(uid=uid).values('mid', 'time')
            history_list = list(history)  # 将查询结果转为列表
            return Response({
                'state': 1,
                'error': '',
                'history': history_list
            })
        except History.DoesNotExist:
            return Response({
                'state': 0,
                'error': 'No history found'
            }, status=status.HTTP_400_BAD_REQUEST)


class UserComment(APIView):
    def post(self, request):
        uid = request.data.get('Uid')

        try:
            comments = Comment.objects.filter(uid=uid).values('cid')
            comment_list = list(comments)  # 将查询结果转为列表
            return Response({
                'state': 1,
                'error': '',
                'comments': comment_list
            })
        except Comment.DoesNotExist:
            return Response({
                'state': 0,
                'error': 'No comments found'
            }, status=status.HTTP_400_BAD_REQUEST)


class MovieQuery(APIView):
    def get(self, request):
        keywords = request.GET.get('keywords', '')

        # 使用 Q 对象进行模糊查询，匹配名称、简介和类型字段
        if keywords:
            movies = Movie.objects.filter(
                Q(name__icontains=keywords) |
                Q(brief__icontains=keywords) |
                Q(type__icontains=keywords)
            ).values('mid')  # 只返回电影的 ID
        else:
            movies = Movie.objects.none()  # 如果没有关键字，则返回空列表

        movie_list = list(movies)  # 转换查询结果为列表
        return Response({
            'data': movie_list
        })


class MovieUpload(APIView):
    def post(self, request):
        name = request.data.get('name')
        date = request.data.get('date')
        brief = request.data.get('brief')
        type = request.data.get('type')
        cover_url = request.data.get('coverUrl')
        duration = request.data.get('duration')

        try:
            # 创建新电影记录
            movie = Movie.objects.create(
                name=name,
                date=date,
                brief=brief,
                type=type,
                coverpath=cover_url,
                duration=duration
            )
            return Response({
                'state': 1,
                'error': ''
            })
        except ValidationError as e:
            return Response({
                'state': 0,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class MovieModify(APIView):
    def post(self, request):
        mid = request.data.get('Mid')
        name = request.data.get('name')
        date = request.data.get('date')
        brief = request.data.get('brief')
        type = request.data.get('type')
        cover_url = request.data.get('coverUrl')
        duration = request.data.get('duration')

        try:
            # 获取要修改的电影对象
            movie = Movie.objects.get(mid=mid)
            movie.name = name
            movie.date = date
            movie.brief = brief
            movie.type = type
            movie.coverpath = cover_url
            movie.duration = duration
            movie.save()

            return Response({
                'state': 1,
                'error': ''
            })
        except Movie.DoesNotExist:
            return Response({
                'state': 0,
                'error': 'Movie not found'
            }, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({
                'state': 0,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class MovieHeat(APIView):
    def post(self, request):
        mid = request.data.get('Mid')

        try:
            movie = Movie.objects.get(mid=mid)
            heat = Comment.objects.filter(mid=mid).count()  # 获取该电影的评论数量
            return Response({
                'state': 1,
                'error': '',
                'heat': heat
            })
        except Movie.DoesNotExist:
            return Response({
                'state': 0,
                'error': 'Movie not found'
            }, status=status.HTTP_400_BAD_REQUEST)


class MovieCover(APIView):
    def post(self, request):
        mid = request.data.get('Mid')

        try:
            movie = Movie.objects.get(mid=mid)
            return Response({
                'state': 1,
                'error': '',
                'coverUrl': movie.coverpath  # 获取封面 URL
            })
        except Movie.DoesNotExist:
            return Response({
                'state': 0,
                'error': 'Movie not found'
            }, status=status.HTTP_400_BAD_REQUEST)


class MovieBrief(APIView):
    def post(self, request):
        mid = request.data.get('Mid')

        try:
            movie = Movie.objects.get(mid=mid)
            return Response({
                'state': 1,
                'error': '',
                'brief': movie.brief  # 获取电影简介
            })
        except Movie.DoesNotExist:
            return Response({
                'state': 0,
                'error': 'Movie not found'
            }, status=status.HTTP_400_BAD_REQUEST)


class MovieDate(APIView):
    def post(self, request):
        mid = request.data.get('Mid')

        try:
            movie = Movie.objects.get(mid=mid)
            return Response({
                'state': 1,
                'error': '',
                'date': movie.date  # 获取电影上映日期
            })
        except Movie.DoesNotExist:
            return Response({
                'state': 0,
                'error': 'Movie not found'
            }, status=status.HTTP_400_BAD_REQUEST)


class MovieType(APIView):
    def post(self, request):
        mid = request.data.get('Mid')

        try:
            movie = Movie.objects.get(mid=mid)
            return Response({
                'state': 1,
                'error': '',
                'type': movie.type  # 获取电影类型
            })
        except Movie.DoesNotExist:
            return Response({
                'state': 0,
                'error': 'Movie not found'
            }, status=status.HTTP_400_BAD_REQUEST)


class MovieDuration(APIView):
    def post(self, request):
        mid = request.data.get('Mid')

        try:
            movie = Movie.objects.get(mid=mid)
            return Response({
                'state': 1,
                'error': '',
                'duration': movie.duration  # 获取电影时长
            })
        except Movie.DoesNotExist:
            return Response({
                'state': 0,
                'error': 'Movie not found'
            }, status=status.HTTP_400_BAD_REQUEST)



class MovieActor(APIView):
    def post(self, request):
        mid = request.data.get('Mid')

        # 查找该电影的所有演员
        actors_in_movie = Actorinmovie.objects.filter(mid=mid)

        if not actors_in_movie:  # 如果查询集为空
            return Response({
                'state': 0,
                'error': 'No actors found for this movie'
            }, status=status.HTTP_404_NOT_FOUND)

        # 获取所有演员及是否主演的信息
        actor_data = [
            {
                'Aid': actor_in_movie.aid.aid,
                'isStarring': bool(actor_in_movie.isstarring)
            }
            for actor_in_movie in actors_in_movie
        ]

        return Response({
            'state': 1,
            'error': '',
            'actors': actor_data
        })


class ActorQuery(APIView):
    def get(self, request):
        keywords = request.GET.get('keywords', '')

        # 使用 Q 对象进行模糊查询，匹配演员名、国籍、性别字段
        if keywords:
            actors = Actor.objects.filter(
                Q(name__icontains=keywords) |
                Q(nationality__icontains=keywords) |
                Q(gender__icontains=keywords)
            ).values('aid')  # 只返回演员的 ID
        else:
            actors = Actor.objects.none()  # 如果没有关键字，则返回空列表

        actor_list = list(actors)  # 转换查询结果为列表
        return Response({
            'data': actor_list
        })


class ActorUpload(APIView):
    def post(self, request):
        name = request.data.get('name')
        photo_url = request.data.get('photoUrl')
        gender = request.data.get('gender')
        nationality = request.data.get('nationality')
        birthdate = request.data.get('birthdate')

        try:
            # 创建新演员记录
            actor = Actor.objects.create(
                name=name,
                photopath=photo_url,
                gender=gender,
                nationality=nationality,
                birthdate=birthdate
            )
            return Response({
                'state': 1,
                'error': ''
            })
        except ValidationError as e:
            return Response({
                'state': 0,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class ActorInMovie(APIView):
    def post(self, request):
        aid = request.data.get('Aid')
        mid = request.data.get('Mid')
        is_starring = request.data.get('isStarring')

        try:
            # 检查演员和电影是否存在
            actor = Actor.objects.get(aid=aid)
            movie = Movie.objects.get(mid=mid)

            # 检查是否已有参演记录
            if Actorinmovie.objects.filter(aid=aid, mid=mid).exists():
                return Response({
                    'state': 1,
                    'error': ''
                })

            # 创建新的参演记录
            Actorinmovie.objects.create(
                aid=actor,
                mid=movie,
                isstarring=1 if is_starring else 0
            )

            return Response({
                'state': 1,
                'error': ''
            })
        except Actor.DoesNotExist:
            return Response({
                'state': 0,
                'error': 'Actor not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Movie.DoesNotExist:
            return Response({
                'state': 0,
                'error': 'Movie not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({
                'state': 0,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class ActorModify(APIView):
    def post(self, request):
        aid = request.data.get('Aid')
        name = request.data.get('name')
        photo_url = request.data.get('photoUrl')
        gender = request.data.get('gender')
        nationality = request.data.get('nationality')
        birthdate = request.data.get('birthdate')

        try:
            # 获取要修改的演员对象
            actor = Actor.objects.get(aid=aid)
            actor.name = name
            actor.photopath = photo_url
            actor.gender = gender
            actor.nationality = nationality
            actor.birthdate = birthdate
            actor.save()

            return Response({
                'state': 1,
                'error': ''
            })
        except Actor.DoesNotExist:
            return Response({
                'state': 0,
                'error': 'Actor not found'
            }, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({
                'state': 0,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class ActorName(APIView):
    def post(self, request):
        aid = request.data.get('Aid')

        try:
            actor = Actor.objects.get(aid=aid)
            return Response({
                'state': 1,
                'error': '',
                'name': actor.name
            })
        except Actor.DoesNotExist:
            return Response({
                'state': 0,
                'error': 'Actor not found'
            }, status=status.HTTP_400_BAD_REQUEST)


class ActorPhoto(APIView):
    def post(self, request):
        aid = request.data.get('Aid')

        try:
            actor = Actor.objects.get(aid=aid)
            return Response({
                'state': 1,
                'error': '',
                'photoUrl': actor.photopath
            })
        except Actor.DoesNotExist:
            return Response({
                'state': 0,
                'error': 'Actor not found'
            }, status=status.HTTP_400_BAD_REQUEST)


class ActorGender(APIView):
    def post(self, request):
        aid = request.data.get('Aid')

        try:
            actor = Actor.objects.get(aid=aid)
            return Response({
                'state': 1,
                'error': '',
                'gender': actor.gender
            })
        except Actor.DoesNotExist:
            return Response({
                'state': 0,
                'error': 'Actor not found'
            }, status=status.HTTP_400_BAD_REQUEST)


class ActorNationality(APIView):
    def post(self, request):
        aid = request.data.get('Aid')

        try:
            actor = Actor.objects.get(aid=aid)
            return Response({
                'state': 1,
                'error': '',
                'nationality': actor.nationality
            })
        except Actor.DoesNotExist:
            return Response({
                'state': 0,
                'error': 'Actor not found'
            }, status=status.HTTP_400_BAD_REQUEST)


class ActorBirthdate(APIView):
    def post(self, request):
        aid = request.data.get('Aid')

        try:
            actor = Actor.objects.get(aid=aid)
            return Response({
                'state': 1,
                'error': '',
                'birthdate': actor.birthdate
            })
        except Actor.DoesNotExist:
            return Response({
                'state': 0,
                'error': 'Actor not found'
            }, status=status.HTTP_400_BAD_REQUEST)


class ActorMovie(APIView):
    def post(self, request):
        aid = request.data.get('Aid')

        # 查找该演员参演的电影
        movies = Actorinmovie.objects.filter(aid=aid).select_related('mid')

        if not movies:  # 如果查询集为空
            return Response({
                'state': 0,
                'error': 'No movies found for the actor'
            }, status=status.HTTP_404_NOT_FOUND)

        # 返回电影id
        movie_data = [{'Mid': actor_movie.mid.mid} for actor_movie in movies]

        return Response({
            'state': 1,
            'error': '',
            'movies': movie_data
        })

# TODO 电影：获取评分 评论 导演 演员 标签