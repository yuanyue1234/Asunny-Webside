# 基于Django和 vue3 的综合个人网站管理系统-豆瓣电影分析与个人网站的设计与实现

## 项目概述

本项目是一个基于Django框架开发的综合性Web应用系统，主要包含豆瓣Top250电影数据分析展示系统和个人网站功能。系统采用前后端分离的架构设计，后端使用Django REST Framework提供API接口，前端使用HTML、CSS、JavaScript和Bootstrap构建用户界面。项目整合了数据可视化、用户认证、留言互动等多种功能，为用户提供全面的Web应用体验。

## 核心功能模块

### 1. 豆瓣电影数据分析系统

- 展示豆瓣Top250电影数据
- 提供电影搜索和分页浏览功能
- 多维度电影数据可视化分析
- 电影详情展示

### 2. 个人网站功能

- 留言板系统
- 用户注册与登录
- 站点配置管理
- 导航项管理
- 集成电影模块访问入口

### 3. 电影模块 (movies)

**路径**: `myproject/movies/`

**功能**:
- 展示豆瓣Top250电影数据
- 提供电影搜索功能
- 电影数据可视化分析
- 支持分页浏览

**主要文件**:
- `models.py`: 定义Movie模型，包含电影的基本信息
- `views.py`: 包含三个主要视图函数：
  - `index()`: 电影列表展示和搜索功能
  - `chart()`: 数据可视化功能，包含多种图表
  - `index2()`: 测试页面
- `urls.py`: 定义URL路由
- `templates/movies/`: 包含前端模板文件

**数据可视化图表**:
1. 不同国家的电影数量饼图
2. 电影评分分布散点图
3. 不同年代电影数量柱状图和折线图
4. 电影标签统计柱状图和词云图
5. 评分总数量饼图和Top20电影评分柱状图
6. 国家年代评分分布3D柱状图

## 技术栈

- **后端框架**：Django 5.0.14, Django REST Framework 3.16.0
- **数据库**：MySQL 8.0
- **前端技术**：HTML5, CSS3, JavaScript, Bootstrap 5.3.0, jQuery 3.6.0
- **数据可视化**：pyecharts 2.0.8, ECharts
- **身份验证**：JWT (djangorestframework_simplejwt 5.5.0)
- **其他工具**：django-cors-headers 4.7.0, requests 2.31.0

## 项目结构

```
myproject/
├── myproject/                  # 项目核心配置目录
│   ├── __init__.py
│   ├── asgi.py                 # ASGI配置
│   ├── settings.py             # 项目设置
│   ├── urls.py                 # 主URL配置
│   └── wsgi.py                 # WSGI配置
├── movies/                     # 电影模块
│   ├── __init__.py
│   ├── admin.py                # 管理界面配置
│   ├── apps.py                 # 应用配置
│   ├── data/                   # 电影数据JSON文件
│   ├── migrations/             # 数据库迁移文件
│   ├── models.py               # 电影数据模型
│   ├── urls.py                 # URL路由配置
│   └── views.py                # 视图函数 (677行)
├── lyb/                        # 留言板模块
│   ├── __init__.py
│   ├── admin.py                # 管理界面配置
│   ├── apps.py                 # 应用配置
│   ├── management/             # 管理命令
│   ├── migrations/             # 数据库迁移文件
│   ├── models.py               # 留言板数据模型
│   ├── serializers.py          # REST框架序列化器
│   ├── tests.py                # 测试文件
│   ├── urls.py                 # URL路由配置
│   └── views.py                # 视图函数
├── site_config/                # 站点配置模块
│   ├── __init__.py
│   ├── admin.py                # 管理界面配置
│   ├── apps.py                 # 应用配置
│   ├── migrations/             # 数据库迁移文件
│   ├── models.py               # 站点配置数据模型
│   ├── serializers.py          # REST框架序列化器
│   ├── tests.py                # 测试文件
│   ├── urls.py                 # URL路由配置
│   └── views.py                # 视图函数
├── templates/                  # HTML模板目录
│   └── movies/                 # 电影模块模板
│       ├── chart.html          # 数据可视化页面
│       ├── index.html          # 电影列表页面
│       └── index2.html         # 测试页面
├── static/                     # 静态文件目录
│   └── movies/                 # 电影模块静态文件
├── import_movies.py            # 电影数据导入脚本
├── manage.py                   # Django命令行工具
├── requirements.txt            # 项目依赖
└── db.sqlite3                  # SQLite数据库文件(开发用)
```

## 模块说明

### 1. 留言板模块 (lyb)

**路径**: `myproject/lyb/`

**功能**:
- 用户留言发布和展示
- 用户注册和登录
- 导航项管理

**主要文件**:
- `models.py`: 定义两个模型：
  - `lyb`: 存储留言信息
  - `NavItem`: 存储导航项信息
- `views.py`: 包含多个API视图：
  - `LybrViewSet`: 留言板CRUD操作
  - `register_user()`: 用户注册
  - `login_user()`: 用户登录，返回JWT令牌
  - `NavItemListAPIView`: 获取导航项列表
  - `get_user_info()`: 获取当前登录用户信息
- `serializers.py`: REST框架序列化器
- `urls.py`: 定义API路由

**技术亮点**:
- 采用JWT认证机制，保障用户账户安全
- 实现RESTful API，便于前后端分离开发

### 2. 站点配置模块 (site_config)

**路径**: `myproject/site_config/`

**功能**:
- 站点级别的配置管理
- 单例模式的站点配置

**主要文件**:
- `models.py`: 定义`SiteProfile`模型，使用单例模式存储站点配置
- `views.py`: 提供`SiteProfileAPIView`用于获取和更新站点配置
- `serializers.py`: REST框架序列化器
- `admin.py`: 自定义管理界面
- `urls.py`: 定义API路由

## API接口

### 留言板API

- `GET /api/is/lyb/`: 获取所有留言
- `POST /api/is/lyb/`: 创建新留言
- `GET /api/is/lyb/{id}/`: 获取特定留言
- `PUT /api/is/lyb/{id}/`: 更新特定留言
- `DELETE /api/is/lyb/{id}/`: 删除特定留言
- `POST /api/is/register/`: 用户注册
- `POST /api/is/login/`: 用户登录
- `GET /api/is/navitems/`: 获取导航项列表
- `GET /api/is/user/info/`: 获取当前登录用户信息
- `POST /api/is/token/refresh/`: 刷新JWT令牌

### 站点配置API

- `GET /api/is/site/profile/`: 获取站点配置
- `PUT /api/is/site/profile/`: 更新站点配置(仅管理员)

### 电影模块页面

- `GET /movies/`: 电影列表页面
- `GET /movies/chart/`: 电影数据可视化页面
- `GET /movies/index2/`: 测试页面

## 数据模型

### Movie模型
```python
class Movie(models.Model):
    douban_id = models.CharField(max_length=10, unique=True)  # 豆瓣ID
    title = models.CharField(max_length=255)  # 电影标题
    img = models.URLField()  # 电影封面图 URL
    href = models.URLField()  # 电影链接
    quote = models.TextField()  # 电影引用（或简介）
    score = models.FloatField()  # 评分
    year = models.CharField(max_length=10)  # 年份
    countries = models.CharField(max_length=255)  # 国家，以逗号分隔
    genres = models.CharField(max_length=255)  # 类型/属性，以逗号分隔
```

### lyb模型
```python
class lyb(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    content = models.TextField()
    posttime = models.DateTimeField(auto_now_add=True)
```

### NavItem模型
```python
class NavItem(models.Model):
    text = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
```

### SiteProfile模型
```python
class SiteProfile(models.Model):
    profile_data = models.JSONField(default=dict)
    last_updated = models.DateTimeField(auto_now=True)
```

## 安装与部署

### 环境要求
- Python 3.8+
- MySQL 8.0+
- 操作系统: Windows 10/11, Linux, macOS

### 安装步骤

1. 克隆项目代码
```bash
git clone <repository-url>
cd myproject
```

2. 创建并激活虚拟环境
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置数据库
编辑 `myproject/settings.py` 文件，配置数据库连接信息：
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'myproject',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}
```

5. 执行数据库迁移
```bash
python manage.py makemigrations
python manage.py migrate
```

6. 导入数据

电影数据
```bash
python import_movies.py
```
创建管理员账户
```bash
python manage.py createsuperuser
```
导入站点配置数据
127.0.0.1:8000/admin/
还有nav

7. 启动开发服务器
```bash
python manage.py runserver
```

8. 访问系统
在浏览器中访问 http://127.0.0.1:8000/movies/ 查看电影列表页面。

## 项目特点

1. **模块化设计**: 系统分为电影展示、留言板、站点配置三个主要模块，各模块功能独立，便于维护和扩展。

2. **数据可视化**: 使用pyecharts和ECharts实现丰富的数据可视化效果，包括饼图、柱状图、折线图、散点图、词云图和3D柱状图。

3. **响应式设计**: 前端页面采用Bootstrap框架，实现响应式布局，适配不同设备。

4. **RESTful API**: 使用Django REST Framework构建规范的RESTful API，便于前后端分离和第三方集成。

5. **JWT认证**: 采用JWT(JSON Web Token)实现用户认证，提高系统安全性。

6. **单例模式**: 站点配置模块采用单例模式，确保全局配置的一致性。

7. **懒加载技术**: 电影列表页面实现图片懒加载，提高页面加载速度和用户体验。

## 未来展望

1. 添加用户评论和评分功能
2. 实现更多数据分析和可视化功能
3. 优化移动端体验
4. 添加电影推荐系统
5. 集成社交媒体分享功能

## 作者
阿晴_asunny-袁越
