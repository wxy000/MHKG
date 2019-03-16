# 新建django工程
django-admin startproject Django
## 新建app
python manage.py startapp [appname]
## 同步数据表
python manage.py makemigrations
python manage.py migrate
## 创建管理员
python manage.py createsuperuser
## 运行django
python manage.py runserver 0.0.0.0:8000
## 后台运行django
nohup python manage.py runserver 0.0.0.0:8000
# 新建scrapy工程
scrapy startproject MyCrawler
# 新建爬虫文件
scrapy genspider [爬虫名] [被爬网站]
## 运行爬虫
scrapy crawl [爬虫名]