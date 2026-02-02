# 个人项目云端部署指南

> **重要提示**：本文档列出了所有需要适配云服务器的配置项，请在部署前仔细检查每个文件。

---

## 📋 目录

1. [后端配置（Django）](#后端配置)
2. [前端配置（Vue 3 + Vite）](#前端配置)
3. [数据库配置](#数据库配置)
4. [静态文件处理](#静态文件处理)
5. [Web服务器配置（Nginx示例）](#web服务器配置)
6. [部署步骤](#部署步骤)

---

## 🔧 后端配置

### 1. Django Settings 配置
**文件位置**：`myproject/myproject/settings.py`

#### 需要修改的配置项：

```python
# ⚠️ 第12行：生产环境必须更改
SECRET_KEY = 'django-insecure-quc)_!+(vgrc2j%o=pf&k4i%j17o3=m(&y!r&omduuozuhb-#d'
# 改为：SECRET_KEY = '你的复杂随机密钥'

# ⚠️ 第14行：生产环境必须设为False
DEBUG = True
# 改为：DEBUG = False

# ⚠️ 第16行：生产环境需要指定具体域名
ALLOWED_HOSTS = ['*']
# 改为：ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com', '服务器IP']
```

#### 数据库配置（第70-83行）：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'myproject',          # ⚠️ 改为生产数据库名
        'USER': 'root',               # ⚠️ 改为生产数据库用户名
        'PASSWORD': 'root',           # ⚠️ 改为生产数据库密码
        'HOST': '127.0.0.1',          # ⚠️ 如果数据库在同一服务器保持，否则改为数据库IP
        'PORT': '3306',               # MySQL默认端口
    }
}
```

#### CORS 配置（第114-119行）：

```python
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True  # ⚠️ 生产环境建议改为False
# 改为：CORS_ORIGIN_ALLOW_ALL = False

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",     # ⚠️ 删除开发环境地址
    "http://127.0.0.1:5173",     # ⚠️ 删除开发环境地址
    # ⚠️ 添加生产前端地址：
    # "https://yourdomain.com",
    # "https://www.yourdomain.com",
]
```

---

## 🎨 前端配置

### 1. Vite 配置文件
**文件位置**：`web/vite.config.js`

#### 需要修改的内容（仅用于本地开发）：

```javascript
// 第13-33行：server.proxy 配置仅用于开发环境
server: {
  proxy: {
    '/api': {
      target: 'http://127.0.0.1:8000',  // ⚠️ 仅开发环境使用
      changeOrigin: true,
    },
    '/movies': {
      target: 'http://127.0.0.1:8000',  // ⚠️ 仅开发环境使用
      changeOrigin: true,
    },
  }
}
// 注意：生产环境构建后不需要这个配置，由Nginx处理代理
```

### 2. Axios API 配置
**文件位置**：`web/src/utils/axios.js`

#### 需要修改的内容（第6行）：

```javascript
const instance = axios.create({
  baseURL: '/api/is',  // ⚠️ 开发环境使用相对路径
  // 生产环境需要改为后端API的完整地址：
  // baseURL: 'https://api.yourdomain.com/api/is',
  // 或者保持相对路径，由Nginx代理处理
  timeout: 5000
})
```

**建议**：保持使用相对路径 `/api/is`，在Nginx配置反向代理到后端。

### 3. Vue Router 配置
**文件位置**：`web/src/router/index.js`

#### 需要修改的内容（第68行和第72行）：

```javascript
// ⚠️ 第68行：开发环境的硬编码地址
window.location.href = 'http://127.0.0.1:8000/movies/';
// 改为：window.location.href = '/movies/';

// ⚠️ 第72行：开发环境的硬编码地址
window.location.href = 'http://127.0.0.1:8000/movies/chart/';
// 改为：window.location.href = '/movies/chart/';
```

**完整的修改后代码**：

```javascript
router.beforeEach((to, from, next) => {
  if (to.path === '/movies') {
    window.location.href = '/movies/';  // ✅ 使用相对路径
    return;
  }
  if (to.path === '/movies/chart') {
    window.location.href = '/movies/chart/';  // ✅ 使用相对路径
    return;
  }
  // ... 其余代码保持不变
})
```

---

## 🗄️ 数据库配置

### 生产环境MySQL准备

1. **创建数据库**：
```sql
CREATE DATABASE myproject CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. **创建用户并授权**（可选，也可以使用root）：
```sql
CREATE USER 'django_user'@'localhost' IDENTIFIED BY 'strong_password';
GRANT ALL PRIVILEGES ON myproject.* TO 'django_user'@'localhost';
FLUSH PRIVILEGES;
```

3. **更新 `settings.py` 中的数据库配置**（见上文后端配置部分）

4. **运行迁移**：
```bash
cd myproject
python manage.py makemigrations
python manage.py migrate
```

---

## 📁 静态文件处理

### 1. Django 静态文件配置
**文件位置**：`myproject/myproject/settings.py`

```python
# 第106-110行：通常不需要修改，确认即可
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    BASE_DIR / 'staticfiles',
]
```

### 2. 收集静态文件

```bash
# 在 myproject 目录下运行
python manage.py collectstatic
```

这会将所有静态文件收集到 `myproject/static/` 目录。

### 3. 前端构建

```bash
# 在 web 目录下运行
npm run build
```

这会生成 `web/dist/` 目录，包含所有生产环境的前端文件。

---

## 🌐 Web服务器配置（Nginx示例）

### Nginx 配置文件示例

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # 前端静态文件
    location / {
        root /path/to/personaldemo/web/dist;
        try_files $uri $uri/ /index.html;
    }

    # Django 后端 API
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Django 后端页面（movies等）
    location /movies/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Django 静态文件
    location /static/ {
        alias /path/to/personaldemo/myproject/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Django 媒体文件（如果有）
    location /media/ {
        alias /path/to/personaldemo/myproject/media/;
        expires 30d;
    }
}
```

---

## 🚀 部署步骤

### 步骤1：准备服务器环境

```bash
# 安装Python 3.12+
sudo apt update
sudo apt install python3.12 python3.12-venv python3-pip

# 安装MySQL
sudo apt install mysql-server

# 安装Nginx
sudo apt install nginx

# 安装Node.js（用于构建前端）
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
```

### 步骤2：上传代码到服务器

```bash
# 使用git或scp上传代码
git clone <your-repo-url> /var/www/personaldemo
# 或
scp -r ./personaldemo user@server:/var/www/
```

### 步骤3：配置后端

```bash
cd /var/www/personaldemo/myproject

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 修改 settings.py（见上文配置清单）
# 修改数据库配置、SECRET_KEY、DEBUG、ALLOWED_HOSTS等

# 运行迁移
python manage.py makemigrations
python manage.py migrate

# 收集静态文件
python manage.py collectstatic

# 创建超级用户（可选）
python manage.py createsuperuser
```

### 步骤4：配置前端

```bash
cd /var/www/personaldemo/web

# 安装依赖
npm install

# 修改 router/index.js（移除硬编码的127.0.0.1:8000）

# 构建生产版本
npm run build
```

### 步骤5：配置Django进程（使用Gunicorn）

```bash
# 安装Gunicorn
pip install gunicorn

# 测试运行
gunicorn --bind 127.0.0.1:8000 myproject.wsgi:application
```

### 步骤6：配置Systemd服务

创建 `/etc/systemd/system/personaldemo.service`：

```ini
[Unit]
Description=Personal Demo Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/personaldemo/myproject
Environment="PATH=/var/www/personaldemo/myproject/venv/bin"
ExecStart=/var/www/personaldemo/myproject/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/var/www/personaldemo/myproject/myproject.sock \
          myproject.wsgi:application

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl start personaldemo
sudo systemctl enable personaldemo
sudo systemctl status personaldemo
```

### 步骤7：配置Nginx

```bash
# 创建Nginx配置文件
sudo nano /etc/nginx/sites-available/personaldemo

# 粘贴上文Nginx配置内容，修改路径和域名

# 启用配置
sudo ln -s /etc/nginx/sites-available/personaldemo /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重启Nginx
sudo systemctl restart nginx
```

### 步骤8：配置HTTPS（可选但推荐）

```bash
# 安装Certbot
sudo apt install certbot python3-certbot-nginx

# 获取SSL证书
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# 自动续期
sudo certbot renew --dry-run
```

---

## ✅ 部署前检查清单

- [ ] **settings.py**：`SECRET_KEY` 已更改
- [ ] **settings.py**：`DEBUG = False`
- [ ] **settings.py**：`ALLOWED_HOSTS` 已设置生产域名
- [ ] **settings.py**：数据库配置已更新
- [ ] **settings.py**：`CORS_ALLOWED_ORIGINS` 已添加生产域名
- [ ] **router/index.js**：已移除硬编码的 `127.0.0.1:8000`
- [ ] **前端已构建**：`npm run build` 完成
- [ ] **静态文件已收集**：`python manage.py collectstatic` 完成
- [ ] **数据库已迁移**：`python manage.py migrate` 完成
- [ ] **Nginx配置正确**：路径和域名已更新
- [ ] **Systemd服务已启动**：`gunicorn` 服务运行中
- [ ] **防火墙已配置**：开放80、443端口

---

## 🔍 常见问题排查

### 1. 前端无法连接后端API
- 检查 Nginx 的 `/api/` location 配置
- 确认 Gunicorn 服务正在运行
- 查看浏览器控制台的网络请求地址

### 2. 静态文件404
- 确认 `python manage.py collectstatic` 已执行
- 检查 Nginx 的 `/static/` alias 路径是否正确

### 3. 跨域问题
- 检查 `settings.py` 中的 `CORS_ALLOWED_ORIGINS`
- 确认前端域名已添加到允许列表

### 4. 电影页面跳转错误
- 确认 `router/index.js` 中的硬编码地址已修改
- 检查 Nginx 的 `/movies/` 代理配置

---

## 📞 技术支持

如有问题，请检查：
1. Django日志：`/var/www/personaldemo/myproject/logs/`
2. Nginx日志：`/var/log/nginx/error.log`
3. Systemd日志：`sudo journalctl -u personaldemo -f`

---

**文档版本**：v1.0
**最后更新**：2025-01-25
**作者**：Claude Code
