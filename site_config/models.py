from django.db import models
from django.contrib.auth.models import User
import json # 用于加载初始数据

# 尝试从 profile.js 获取默认数据
DEFAULT_PROFILE_DATA = {}
# 注意：直接在模型文件中执行文件读取和解析以下载默认值，
# 仅适用于开发阶段或一次性设置。更好的做法是通过管理命令或数据迁移来加载。
# 这里为了简化，我们假设 profile.js 的内容可以被某种方式加载进来。
# 理想情况下，这个默认值应该是一个Python字典，或者在数据迁移中设置。
# 例如：
# DEFAULT_PROFILE_DATA = {
#   "name": "默认名称",
#   "email": "default@example.com",
#   "avatar": "", 
#   "socialLinks": [], 
#   "interests": [], 
#   "works": [] 
# }

class SiteProfile(models.Model):
    """
    存储站点级别的配置信息，通常由超级管理员管理。
    我们设计为系统中只存在一个该模型的实例。
    """
    # 关联到创建或最后修改此配置的管理员，可选
    # 如果严格限定只有一个超级管理员能改，并且系统中只有一条记录，这个字段可以省略
    # 或者用一个更简单的标识如 last_modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'is_staff': True})
    
    profile_data = models.JSONField(default=dict) # 使用 dict 作为默认值以确保是合法的JSON
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        # 尝试从 profile_data 中获取 name，如果存在的话
        name = self.profile_data.get('name', 'Site Profile')
        return f"{name} (Last Updated: {self.last_updated.strftime('%Y-%m-%d %H:%M')})"

    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configurations"

    def save(self, *args, **kwargs):
        # 确保系统中只有一个 SiteProfile 实例
        if not self.pk and SiteProfile.objects.exists():
            # 如果这是一个新对象并且已经有一个对象存在，则阻止保存
            # 或者，可以选择更新现有对象而不是创建新对象
            # raise ValidationError("Only one SiteProfile instance is allowed.")
            # 这里我们选择获取并更新现有实例，或如果不存在则创建
            existing = SiteProfile.objects.first()
            if existing:
                self.pk = existing.pk # 强制更新现有记录
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        """获取唯一的 SiteProfile 实例，如果不存在则创建一个空的。"""
        obj, created = cls.objects.get_or_create(pk=1) # 假设我们总是使用 pk=1
        if created:
            # 如果是新创建的，可以考虑从 profile.js 加载初始数据
            # 这里我们暂时不自动加载，管理员可以通过 Admin 界面首次填充
            pass 
        return obj 