import os
import re
from django.core.management.base import BaseCommand
from django.conf import settings
from lyb.models import NavItem # 确保从正确的 app 导入 NavItem

class Command(BaseCommand):
    # 导入导航项从 web/src/data/nav.js 到 NavItem 模型
    help = 'Imports navigation items from web/src/data/nav.js into the NavItem model'

    def handle(self, *args, **options):
        # 构建 nav.js 文件的绝对路径
        # Django 项目的根目录是 settings.BASE_DIR
        # nav.js 相对于项目根目录的路径是 web/src/data/nav.js
        # 注意：这里的假设是 settings.BASE_DIR 指向 'personaldemo/myproject'
        # 如果您的 settings.BASE_DIR 指向 'personaldemo'，则需要调整下面的路径
        
        # 通常 settings.BASE_DIR 是 manage.py 所在的目录，即 'myproject'
        # 而 nav.js 在 'personaldemo/web/src/data/nav.js'
        # 因此，我们需要向上两级到 'personaldemo'，然后再进入 'web/src/data/nav.js'
        
        # 更可靠的方式是确定 'web' 目录相对于 BASE_DIR 的位置
        # 假设 BASE_DIR 是 'personaldemo/myproject'
        # nav_js_path 相对于 BASE_DIR 的上一级目录 (personaldemo)
        project_root_one_level_up = os.path.dirname(settings.BASE_DIR) # 'personaldemo'
        nav_js_path = os.path.join(project_root_one_level_up, 'web', 'src', 'data', 'nav.js')

        if not os.path.exists(nav_js_path):
            self.stdout.write(self.style.ERROR(f'nav.js file not found at {nav_js_path}'))
            self.stdout.write(self.style.NOTICE(f'settings.BASE_DIR is {settings.BASE_DIR}'))
            self.stdout.write(self.style.NOTICE(f'Project root (one level up) is {project_root_one_level_up}'))
            return

        try:
            with open(nav_js_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 修改后的正则表达式
            pattern = re.compile(r"text:\s*['\"]([^'\"]+)['\"],\s*url:\s*['\"]([^'\"]+)['\"]")
            
            matches = pattern.findall(content)
            
            imported_count = 0
            skipped_count = 0
            
            if not matches:
                self.stdout.write(self.style.WARNING('No navigation items found in nav.js. Check the file content and regex pattern.'))
                return

            for text, url in matches:
                # 检查是否已存在相同的导航项
                nav_item, created = NavItem.objects.get_or_create(
                    text=text,
                    url=url
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Successfully imported: {text} ({url})'))
                    imported_count += 1
                else:
                    self.stdout.write(self.style.NOTICE(f'Skipped (already exists): {text} ({url})'))
                    skipped_count += 1
            
            self.stdout.write(f'\\nImport process finished.')
            self.stdout.write(f'Imported: {imported_count}, Skipped: {skipped_count}')

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Error: nav.js file not found at {nav_js_path}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}')) 