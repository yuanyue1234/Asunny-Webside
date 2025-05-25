from django.db import models


# Create your models here.
class lyb(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    content = models.TextField()
    posttime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "d_lyb"  # 留言板

class NavItem(models.Model):
    text = models.CharField(max_length=100)
    url = models.CharField(max_length=200)

    def __str__(self):
        return self.text
