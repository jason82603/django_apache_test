import requests
import json
import pytz
import time
from datetime import datetime, timedelta
from .models import UVData
from background_task import background

class UVFetcher:
    def __init__(self):
        self.url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/O-A0005-001"
        self.headers = {
            "Authorization": "CWA-DC02B713-9B83-4906-962F-4B22F2E18C0E"
        }
        self.params = {
            "format": "JSON",
            "StationID": "466920"
        }

    def fetch_data(self):
        response = requests.get(self.url, headers=self.headers, params=self.params)
        data = response.json()

        # 提取需要的数据
        element_name = data["records"]["weatherElement"]["elementName"]
        uv_index = data["records"]["weatherElement"]["location"][0]["UVIndex"]
        date = data["records"]["weatherElement"]["Date"]

        # 添加 StationName 字段
        fetched_data = {
            "StationName": "臺北市",
            "elementName": element_name,
            "UVIndex": uv_index,
            # "Date": date
            "Date": datetime.now(pytz.timezone('Asia/Taipei'))
        }

        return fetched_data

    def job(self):
        print("Fetching data...")
        fetched_data = self.fetch_data()
        print(fetched_data)

        uv_data = UVData.objects.create(
            station_name=fetched_data["StationName"],
            element_name=fetched_data["elementName"],
            uv_index=fetched_data["UVIndex"],
            date=fetched_data["Date"]
        )
        uv_data.save()

        print("Data fetched and saved successfully.")

    def run(self):
        while True:
            # 获取当前时间并添加时区信息
            current_time = datetime.now(pytz.timezone('Asia/Taipei'))
            print(f'current_time: {current_time}')

            # 将目标时间设置为 UTC+08:00 时区且01:00的时间
            target_time = current_time.replace(hour=1, minute=00, second=00, microsecond=0)

            # 如果当前时间已经过了目标时间，则将目标时间推迟到明天
            if current_time > target_time:
                target_time += timedelta(days=1)
            print(f'target_time: {target_time}')
            # 计算需要等待的时间
            wait_time = (target_time - current_time).total_seconds()
            print(f'wait_time: {wait_time}')
            # 等待直到目标时间
            time.sleep(wait_time)
            # 执行任务
            self.job()




