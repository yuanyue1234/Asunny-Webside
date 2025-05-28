启动前端：
cd web && npm run dev

启动后端：
先启动数据库

cd myproject && source venv/Scripts/activate &&
python manage.py runserver

更新依赖包:
pip freeze > requirements.txt
---

迁移数据库：
python manage.py makemigrations
python manage.py migrate

---

简历页面
找一些需要用后端的项目融合
