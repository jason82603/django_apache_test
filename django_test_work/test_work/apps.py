from django.apps import AppConfig
from background_task import background

class TestWorkConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'test_work'


    # def ready(self):
    #     from .fetch_uv_data import UVFetcher  # 导入你的 UV 数据获取模块
    #     # 调用 UV 数据获取模块中的启动函数
    #     uv_fetcher = UVFetcher()
    #     uv_fetcher.run()




