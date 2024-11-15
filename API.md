# API设计

## 新增用户(TEMPLATE)

1. **接口名**：add_user
2. **请求形式**：post

```json
前端发送数据：
{
	id:int, //用户 id
	name:string //用户名
}

前端期望返回数据：
{
	state:int, //状态
    error:string //错误信息
}
```

## 用户User

### 登录（已实现并进行接口测试）

1. **接口名**：user_login
2. **请求形式**：post
3. **url**: /user/login/

```json
前端发送数据：
{
	email:string, //用户邮箱
	password:string //密码
}

前端期望返回数据：
{
	state:int, //状态
	error:string, //错误信息
    Uid:int //用户id
}
```

登录成功时
```python
return Response({
	'state': 1,
	'error': '',
	'Uid': user.uid
})
```
用户（邮箱）不存在时：
```python
return Response({
	'state': 0,
	'error': 'User not found'
}, status=status.HTTP_400_BAD_REQUEST)
# status.HTTP_400_BAD_REQUEST即为400
```
密码错误时：
```python
return Response({
	'state': 0,
	'error': 'Wrong password'
}, status=status.HTTP_400_BAD_REQUEST)
```

### 注册（已实现并进行接口测试）

1. **接口名**：user_register
2. **请求形式**：post
3. **url**: /user/register/

```json
前端发送数据：
{
    name:string, //用户名
	email:string, //用户邮箱
	password:string //密码
}

前端期望返回数据：
{
	state:int, //状态
	error:string, //错误信息
    Uid:int //用户id
}
```

邮箱已注册时：
```python
return Response({
	'state': 0,
	'error': 'Email is already registered'
}, status=400)
```

注册成功时：
```python
return Response({
	'state': 1,
	'error': '',
	'Uid': user.uid
})
```

注册时引发其他错误导致失败：
```python
except ValidationError as e:
	return Response({
		'state': 0,
		'error': str(e)
	}, status=status.HTTP_400_BAD_REQUEST)
```

### 修改密码（已实现并进行接口测试）

1. **接口名**：user_forget
2. **请求形式**：post
3. **url**: /user/forget/

```json
前端发送数据：
{
	email:string, //用户邮箱
	password:string, //密码
    confirm:string //确认密码
}

前端期望返回数据：
{
	state:int, //状态
	error:string //错误信息
}
```

确认密码不一致时：
```python
return Response({
	'state': 0,
	'error': 'Passwords do not match'
}, status=400)
```

修改成功时：
```python
return Response({
	'state': 1,
	'error': ''
})
```

用户不存在时
```python
return Response({
	'state': 0,
	'error': 'User not found'
}, status=status.HTTP_400_BAD_REQUEST)
```

### 上传头像（已实现并进行接口测试）

1. **接口名**：user_photo
2. **请求形式**：post
3. **url**: /user/photo/

```json
前端发送数据：
{
    Uid:int, //用户id
	photoUrl:string //头像url
}

前端期望返回数据：
{
	state:int, //状态
	error:string //错误信息
}
```

上传成功
```python
return Response({
	'state': 1,
	'error': ''
})
```

用户不存在
```python
return Response({
	'state': 0,
	'error': 'User not found'
}, status=400)
```

### 上传观看历史（已实现并进行接口测试）

1. **接口名**：user_history_upload
2. **请求形式**：post
3. **url**: /user/history/upload/

```json
前端发送数据：
{
	Uid:int, //用户id
    Mid:int, //电影id
    time:Date //观看日期，形式为："2024-11-15 12:00:00"
}

前端期望返回数据：
{
	state:int, //状态
	error:string //错误信息
}
```

上传成功
```python
return Response({
	'state': 1,
	'error': '',
})
```

用户不存在
```python
return Response({
	'state': 0,
	'error': 'User not found'
}, status=400)
```

电影不存在
```python
return Response({
	'state': 0,
	'error': 'Movie not found'
}, status=status.HTTP_400_BAD_REQUEST)
```

### 查询观看历史（已实现并进行接口测试）

1. **接口名**：user_history_query
2. **请求形式**：post
3. **url**: /user/history/query/

```json
前端发送数据：
{
	Uid:int //用户id
}

前端期望返回数据：
{
	state:int, //状态
	error:string, //错误信息
    history:[{
        Mid:int, //电影id
        time:Date //观看日期
    }]
}
```

成功查询，且有历史记录：
```python
return Response({
	'state': 1,
	'error': '',
	'history': history_list
})
```

成功查询，但没有历史记录：
```python
return Response({
	'state': 1,
	'error': 'No history found',
	'history': history_list
})
```

### 查看评论（待测试，完成评论接口后测试）

1. **接口名**：user_comment
2. **请求形式**：post
3. **url**: /user/comment/

```json
前端发送数据：
{
	Uid:int //用户id
}

前端期望返回数据：
{
	state:int, //状态
	error:string, //错误信息
    comments:[{
        Cid:int //评论id
    }]
}
```

成功查询，且有评论
```python
return Response({
	'state': 1,
	'error': '',
	'comments': comment_list
})
```

成功查询，但没有评论
```python
return Response({
	'state': 1,
	'error': 'No comments found',
	'comments': comment_list
})
```

用户不存在
```python
return Response({
	'state': 0,
	'error': 'User not found'
}, status=status.HTTP_400_BAD_REQUEST)
```

## 电影Movie

### 搜索

1. **接口名**：movie_query
2. **请求形式**：get

```json
前端发送数据：
{
	keywords:string, //关键字
}

前端期望返回数据：
{
    data:[{
        Mid:int, //电影id
	}]
}
```

### 上传电影

1. **接口名**：movie_upload
2. **请求形式**：post

```json
前端发送数据：
{
	name:string, //电影名
    date:Date, //上映时间
    brief:string, //简介
    type:string, //类型
    coverUrl:string, //封面图片
    duration:int //时长
}

前端期望返回数据：
{
	state:int, //状态
	error:string //错误信息
}
```

上传成功：
```
return Response({
	'state': 1,
	'error': ''
})
```

上传失败：
```
except ValidationError as e:
	return Response({
		'state': 0,
		'error': str(e)
	}, status=status.HTTP_400_BAD_REQUEST)
```

### 修改电影

1. **接口名**：movie_modify
2. **请求形式**：post

```json
前端发送数据：
{
    Mid:int, //电影id
	name:string, //电影名
    date:Date, //上映时间
    brief:string, //简介
    type:string, //类型
    coverUrl:string, //封面图片
    duration:int //时长
}

前端期望返回数据：
{
	state:int, //状态
	error:string //错误信息
}
```

修改成功：
```
return Response({
	'state': 1,
	'error': ''
})
```

电影不存在
```
return Response({
	'state': 0,
	'error': 'Movie not found'
}, status=status.HTTP_400_BAD_REQUEST)
```

修改失败
```
return Response({
	'state': 0,
	'error': str(e)
}, status=status.HTTP_400_BAD_REQUEST)
```

### 获取热度(评论数)

1. **接口名**：movie_heat
2. **请求形式**：post

```json
前端发送数据：
{
	Mid:int //电影id
}

前端期望返回数据：
{
	state:int, //状态
	error:string, //错误信息
    heat:int //热度
}
```

获取成功
```
return Response({
	'state': 1,
	'error': '',
	'heat': heat
})
```

电影不存在
```
return Response({
	'state': 0,
	'error': 'Movie not found'
}, status=status.HTTP_400_BAD_REQUEST)
```

### 获取评分 todo

1. **接口名**：movie_score
2. **请求形式**：post

```json
前端发送数据：
{
	Mid:int //电影id
}

前端期望返回数据：
{
	state:int, //状态
	error:string, //错误信息
    score:float //评分
}
```



### 获取封面

1. **接口名**：movie_cover
2. **请求形式**：post

```json
前端发送数据：
{
	Mid:int //电影id
}

前端期望返回数据：
{
	state:int, //状态
	error:string, //错误信息
    coverUrl:string //封面
}
```

获取成功
```
return Response({
	'state': 1,
	'error': '',
	'coverUrl': movie.coverpath  # 获取封面 URL，为字符串
})
```

电影不存在
```
return Response({
	'state': 0,
	'error': 'Movie not found'
}, status=status.HTTP_400_BAD_REQUEST)
```

### 获取简介

1. **接口名**：movie_brief
2. **请求形式**：post

```json
前端发送数据：
{
	Mid:int //电影id
}

前端期望返回数据：
{
	state:int, //状态
	error:string, //错误信息
    brief:string //简介
}
```

获取成功
```
return Response({
	'state': 1,
	'error': '',
	'brief': movie.brief  # 获取电影简介
})
```

电影不存在
```
return Response({
	'state': 0,
	'error': 'Movie not found'
}, status=status.HTTP_400_BAD_REQUEST)
```

### 获取上映时间

1. **接口名**：movie_date
2. **请求形式**：post

```json
前端发送数据：
{
	Mid:int //电影id
}

前端期望返回数据：
{
	state:int, //状态
	error:string, //错误信息
    date:Date //名称
}
```

获取成功
```
return Response({
	'state': 1,
	'error': '',
	'date': movie.date  # 获取电影上映日期
})
```

电影不存在
```
return Response({
	'state': 0,
	'error': 'Movie not found'
}, status=status.HTTP_400_BAD_REQUEST)
```

### 获取类型

1. **接口名**：movie_type
2. **请求形式**：post

```json
前端发送数据：
{
	Mid:int //电影id
}

前端期望返回数据：
{
	state:int, //状态
	error:string, //错误信息
    type:string //类型
}
```

获取成功
```
return Response({
	'state': 1,
	'error': '',
	'type': movie.type  # 获取电影类型
})
```

电影不存在
```
return Response({
	'state': 0,
	'error': 'Movie not found'
}, status=status.HTTP_400_BAD_REQUEST)
```

### 获取时长

1. **接口名**：movie_duration
2. **请求形式**：post

```json
前端发送数据：
{
	Mid:int //电影id
}

前端期望返回数据：
{
	state:int, //状态
	error:string, //错误信息
    duration:int //时长
}
```

获取成功
```
return Response({
	'state': 1,
	'error': '',
	'duration': movie.duration  # 获取电影时长
})
```

电影不存在
```
return Response({
	'state': 0,
	'error': 'Movie not found'
}, status=status.HTTP_400_BAD_REQUEST)
```

### 获取评论 todo

1. **接口名**：movie_comment
2. **请求形式**：post

```json
前端发送数据：
{
	Mid:int //电影id
}

前端期望返回数据：
{
	state:int, //状态
	error:string, //错误信息
    comments:[{
        Cid:int //评论id
    }]
}
```

### 获取导演 todo

1. **接口名**：movie_director
2. **请求形式**：post

```json
前端发送数据：
{
	Mid:int //电影id
}

前端期望返回数据：
{
	state:int, //状态
	error:string, //错误信息
    directors:[{
        Did:int //导演id
    }]
}
```

### 获取演员

1. **接口名**：movie_actor
2. **请求形式**：post

```json
前端发送数据：
{
	Mid:int //电影id
}

前端期望返回数据：
{
	state:int, //状态
	error:string, //错误信息
    actors:[{
        Aid:int, //演员id
        isStarring:boolean //是否主演
    }]
}
```

### 获取标签 todo

1. **接口名**：movie_tag
2. **请求形式**：post

```json
前端发送数据：
{
	Mid:int //电影id
}

前端期望返回数据：
{
	state:int, //状态
	error:string, //错误信息
    tags:[{
        tag:string //标签内容
    }]
}
```

## 演员actor

### 搜索

1. **接口名**：actor_query
2. **请求形式**：get

```json
前端发送数据：
{
	keywords:string, //关键字
}

前端期望返回数据：
{
    data:[{
        Aid:int //演员id
	}]
}
```

### 上传演员

1. **接口名**：actor_upload
2. **请求形式**：post

```json
前端发送数据：
{
	name:string, //演员名
    photoUrl:string, //照片url
    gender:char, //性别
    nationality:string, //国籍
    birthdate:Date //生日
}

前端期望返回数据：
{
	state:int, //状态
	error:string //错误信息
}
```

### 修改演员

1. **接口名**：actor_modify
2. **请求形式**：post

```json
前端发送数据：
{
    Aid:int, //演员id
	name:string, //演员名
    photoUrl:string, //照片url
    gender:char, //性别
    nationality:string, //国籍
    birthdate:Date //生日
}

前端期望返回数据：
{
	state:int, //状态
	error:string //错误信息
}
```

### 演员参演电影

1. **接口名**：actor_in_movie
2. 请求形式：post

```json
前端发送数据：
{
	Aid:int, //演员id
	Mid:int, //电影id
	isStarring:bool //是否主演
}

前端期望返回数据：
{
	state:int, //状态
	error:string //错误信息
}
```

### 获取姓名

1. **接口名**：actor_name
2. **请求形式**：post

```json
前端发送数据：
{
	Aid:int //演员id
}

前端期望返回数据：
{
	state:int, //状态
	error:string, //错误信息
    name:string //姓名
}
```

### 获取照片

1. **接口名**：actor_photo
2. **请求形式**：post

```json
前端发送数据：
{
	Aid:int //演员id
}

前端期望返回数据：
{
	state:int, //状态
	error:string, //错误信息
    photoUrl:string //照片url
}
```

### 获取性别

1. **接口名**：actor_gender
2. **请求形式**：post

```json
前端发送数据：
{
	Aid:int //演员id
}

前端期望返回数据：
{
	state:int, //状态
	error:string, //错误信息
    gender:char //性别
}
```

### 获取国籍

1. **接口名**：actor_nationality
2. **请求形式**：post

```json
前端发送数据：
{
	Aid:int //演员id
}

前端期望返回数据：
{
	state:int, //状态
	error:string, //错误信息
    nationality:string //国籍
}
```

### 获取生日

1. **接口名**：actor_birthdate
2. **请求形式**：post

```json
前端发送数据：
{
	Aid:int //演员id
}

前端期望返回数据：
{
	state:int, //状态
	error:string, //错误信息
    birthdate:Date //生日
}
```

### 获取参演电影

1. **接口名**：actor_movie
2. **请求形式**：post

```json
前端发送数据：
{
	Aid:int //演员id
}

前端期望返回数据：
{
	state:int, //状态
	error:string, //错误信息
    movies:[{
        Mid:mid //电影id
    }]
}
```

## 导演director

### 搜索

1. **接口名**：director_query
2. **请求形式**：get

```json
前端发送数据：
{
	keywords:string, //关键字
}

前端期望返回数据：
{
    data:[{
        Did:int //导演id
	}]
}
```

### 上传导演

1. **接口名**：director_upload
2. **请求形式**：post

```json
前端发送数据：
{
	name:string, //导演名
    photoUrl:string, //照片url
    gender:char, //性别
    nationality:string, //国籍
    birthdate:Date //生日
}

前端期望返回数据：
{
	state:int, //状态
	error:string //错误信息
}
```

### 导演执导电影

1. **接口名**：director_movie
2. 请求形式：post

```json
前端发送数据：
{
	Did:int, //导演id
	Mid:int //电影id
}

前端期望返回数据：
{
	state:int, //状态
	error:string //错误信息
}
```

### 修改导演

1. **接口名**：director_modify
2. **请求形式**：post

```json
前端发送数据：
{
    Did:int, //导演id
	name:string, //导演名
    photoUrl:string, //照片url
    gender:char, //性别
    nationality:string, //国籍
    birthdate:Date //生日
}

前端期望返回数据：
{
	state:int, //状态
	error:string //错误信息
}
```

### 获取姓名

1. **接口名**：director_name
2. **请求形式**：post

```json
前端发送数据：
{
	Did:int //导演id
}

前端期望返回数据：
{
	state:int, //状态
	error:string, //错误信息
    name:string //姓名
}
```

### 获取照片

1. **接口名**：director_photo
2. **请求形式**：post

```json
前端发送数据：
{
	Did:int //导演id
}

前端期望返回数据：
{
	state:int, //状态
	error:string, //错误信息
    photoUrl:string //照片url
}
```

### 获取性别

1. **接口名**：director_gender
2. **请求形式**：post

```json
前端发送数据：
{
	Did:int //导演id
}

前端期望返回数据：
{
	state:int, //状态
	error:string, //错误信息
    gender:char //性别
}
```

### 获取国籍

1. **接口名**：director_nationality
2. **请求形式**：post

```json
前端发送数据：
{
	Did:int //导演id
}

前端期望返回数据：
{
	state:int, //状态
	error:string, //错误信息
    nationality:string //国籍
}
```

### 获取生日

1. **接口名**：director_birthdate
2. **请求形式**：post

```json
前端发送数据：
{
	Did:int //导演id
}

前端期望返回数据：
{
	state:int, //状态
	error:string, //错误信息
    birthdate:Date //生日
}
```

### 获取执导电影

1. **接口名**：director_name
2. **请求形式**：post

```json
前端发送数据：
{
	Did:int //电影id
}

前端期望返回数据：
{
	state:int, //状态
	error:string, //错误信息
    movies:[{
        Mid:mid //电影id
    }]
}
```

## 评论Comment

### 评论

1. **接口名**：comment_release
2. **请求形式**：post

```json
前端发送数据：
{
	Uid:int, //用户id
    Mid:int, //电影id
    content:string, //评论内容
    score:int //评分
}

前端期望返回数据：
{
	state:int, //状态
	error:string //错误信息
}
```

### 回复

1. **接口名**：comment_reply
2. **请求形式**：post

```json
前端发送数据：
{
    Cid:int, //回复评论id
	Uid:int, //用户id
    Mid:int, //电影id
    comment:string, //评论内容
    score:int //评分
}

前端期望返回数据：
{
	state:int, //状态
	error:string //错误信息
}
```

### 点赞

1. **接口名**：comment_likes
2. **请求形式**：post

```json
前端发送数据：
{
	Cid:int //评论id
}

前端期望返回数据：
{
	state:int, //状态
	error:string //错误信息
}
```

### 获取回复

1. **接口名**：comment_reply_query
2. **请求形式**：post

```json
前端发送数据：
{
	Cid:int //评论id
}

前端期望返回数据：
{
	state:int, //状态
	error:string, //错误信息
    replys:[{
        Cid:int //回复i
    }]
}
```

### 获取回复对象

1. **接口名**：comment_reply2whom
2. **请求形式**：post

```json
前端发送数据：
{
	Cid:int //评论id
}

前端期望返回数据：
{
	state:int, //状态
	error:string, //错误信息
    Reply2Id:int //回复的评论id
}
```

### 获取评论内容

1. **接口名**：comment_content
2. **请求形式**：post

```json
前端发送数据：
{
	Cid:int //评论id
}

前端期望返回数据：
{
	state:int, //状态
	error:string, //错误信息
    content:string //评论内容
}
```

### 获取评论者

1. **接口名**：comment_user
2. **请求形式**：post

```json
前端发送数据：
{
	Cid:int //评论id
}

前端期望返回数据：
{
	state:int, //状态
	error:string, //错误信息
    Uid:int //发布者id
}
```

### 获取评论所在电影

1. **接口名**：comment_movie
2. **请求形式**：post

```json
前端发送数据：
{
	Cid:int //评论id
}

前端期望返回数据：
{
	state:int, //状态
	error:string, //错误信息
    Mid:int //电影id
}
```

### 获取评分

1. **接口名**：comment_score
2. **请求形式**：post

```json
前端发送数据：
{
	Cid:int //评论id
}

前端期望返回数据：
{
	state:int, //状态
	error:string, //错误信息
    score:int //评分
}
```

### 获取评论时间

1. **接口名**：comment_time
2. **请求形式**：post

```json
前端发送数据：
{
	Cid:int //评论id
}

前端期望返回数据：
{
	state:int, //状态
	error:string, //错误信息
    time:DateTime //评论时间
}
```

### 获取点赞数

1. **接口名**：comment_get_likes
2. **请求形式**：post

```json
前端发送数据：
{
	Cid:int //评论id
}

前端期望返回数据：
{
	state:int, //状态
	error:string, //错误信息
    likes:int //点赞数
}
```

## 标签Tag

### 打标签

1. **接口名**：tag_release
2. **请求形式**：post

```json
前端发送数据：
{
	Mid:int, //电影id
    tag:string //标签内容
}

前端期望返回数据：
{
	state:int, //状态
	error:string //错误信息
}
```

### 获取热度

1. **接口名**：tag_heat
2. **请求形式**：post

```json
前端发送数据：
{
	Mid:int, //电影id
    tag:string //标签内容
}

前端期望返回数据：
{
	state:int, //状态
	error:string, //错误信息
    heat:int //热度
}
```

### 搜索

1. **接口名**：tag_query
2. **请求形式**：post

```json
前端发送数据：
{
    tag:string //标签内容
}

前端期望返回数据：
{
	state:int, //状态
	error:string, //错误信息
    Movies:[{
        Mid:int, //电影id
    }]
}
```

