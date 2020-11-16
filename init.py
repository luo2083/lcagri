import django
import hashlib
import json
import logging
import os
import yaml

from backend import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from apis.models import App
def init_app_data():
    old_apps = App.objects.all()
    path = os.path.join(settings.BASE_DIR, 'app.yaml')
    with open(path, 'r', encoding='utf-8') as f:
        apps = yaml.load(f, Loader=yaml.FullLoader)
        published = apps.get('published')
        for item in published:
            item = item.get('app')
            src = item.get('category') + item.get('application')
            appid = hashlib.md5(src.encode('utf8')).hexdigest()
            if len(old_apps.filter(appid=appid)) == 1:
                print('already exists, appid:', appid)
                app = old_apps.filter(appid=appid)[0]
            else:
                app = App()
                print('not exists, appid:', appid)
            app.appid = appid
            app.name = item.get('name')
            app.application = item.get('application')
            app.url = item.get('url')
            app.published_date = item.get('published_date')
            app.category = item.get('category')
            app.desc = item.get('desc')
            app.save()

if __name__ == '__main__':
    init_app_data()
