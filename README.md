# 使用步骤
1. 安装依赖包
```
pip install django
pip install pymysql
pip install django-cors-headers
```
2. 本地安装好mysql数据库（后续会转为连接GaussDB），创建名为txj的数据库；在mysite文件夹下的settings.py文件中配置数据库连接信息，连接至数据库。
3. 进行数据库迁移，生成数据库表，执行以下命令：
```
python manage.py makemigrations
python manage.py migrate
```
（如果出现报错，可能是编码格式的问题，在编辑器中检查txj文件夹下models.py文件的编码格式，更改为UTF-8）
4. 运行项目，执行以下命令：
```
python manage.py runserver
```