from django.contrib import admin
from .models import SiteProfile # 确保导入 SiteProfile

@admin.register(SiteProfile)
class SiteProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'last_updated')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # 确保我们总是处理 pk=1 的单例
        # 如果单例尚不存在，get_solo() 会创建它
        return qs.filter(pk=SiteProfile.get_solo().pk)

    def has_add_permission(self, request):
        # 由于 get_solo() 会自动创建实例，这里总是返回 False 避免通过 Admin 创建多个
        # 或者，如果 SiteProfile.objects.count() >= 1，则返回 False
        return not SiteProfile.objects.exists() # 只有在还没有任何记录时才允许添加第一个

    def has_delete_permission(self, request, obj=None):
        # 通常不允许删除这个唯一的配置项
        return False

# 移除了原始的 # Register your models here.
