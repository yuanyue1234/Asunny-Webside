from django.db import models


# Create your models here.
class lyb(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    counter = models.TextField()
    posttime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "d_lyb"  # 留言板
