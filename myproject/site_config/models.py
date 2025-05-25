from django.db import models
from django.contrib.auth.models import User
import json # 用于加载初始数据

class SiteProfile(models.Model):
    """
    存储站点级别的配置信息，通常由超级管理员管理。
    我们设计为系统中只存在一个该模型的实例。
    """
    profile_data = models.JSONField(default=dict) 
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        name = self.profile_data.get('name', 'Site Profile')
        return f"{name} (Last Updated: {self.last_updated.strftime('%Y-%m-%d %H:%M')})"

    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configurations"

    def save(self, *args, **kwargs):
        if not self.pk and SiteProfile.objects.exists():
            existing = SiteProfile.objects.first()
            if existing:
                self.pk = existing.pk 
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        """获取唯一的 SiteProfile 实例，如果不存在则使用 pk=1 创建一个空的。"""
        # 尝试获取 pk=1 的对象，如果不存在则创建它
        # 这样可以避免在 Admin 中因为没有记录而无法显示的问题
        # 并且确保了我们始终操作的是同一个记录
        obj, created = cls.objects.get_or_create(pk=1, defaults={'profile_data': {}})
        return obj

# 移除了原始的 # Create your models here.
