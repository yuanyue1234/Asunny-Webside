from django.contrib import admin
from .models import SiteProfile

@admin.register(SiteProfile)
class SiteProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'last_updated')
    # Django Admin 对 JSONField 默认提供了不错的编辑界面
    # 如果需要更复杂的 JSON 编辑器，可以考虑集成第三方库如 django-jsoneditor

    def get_queryset(self, request):
        # 确保Admin中只加载/显示一个实例 (pk=1)
        qs = super().get_queryset(request)
        # 如果还没有实例，允许创建一个
        if not qs.filter(pk=1).exists() and not SiteProfile.objects.exists():
            # SiteProfile.objects.create(pk=1, profile_data={}) # 如果需要自动创建
            pass
        return qs.filter(pk=SiteProfile.get_solo().pk) # 总是加载单例

    def has_add_permission(self, request):
        # 如果已经存在一个实例，则不允许通过Admin再添加新的
        return not SiteProfile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # 通常不允许删除这个唯一的配置项
        return False 