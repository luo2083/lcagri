import json
import os
import yaml

from django.http import JsonResponse
from django.views import View

from authorization.models import User
from apis.models import App

from utils.response import ReturnCode,CommonResponseMixin
from utils.auth import already_authorized, get_user
from backend import settings
def init_app_data():
    data_file = os.path.join(settings.BASE_DIR, 'app.yaml')
    with open(data_file, 'r', encoding='utf-8') as f:
        apps = yaml.load(f)
        return  apps

def get_menu(request):
    # global_apps_data = init_app_data()
    # published_apps_data = global_apps_data.get('published')
    # response = CommonResponseMixin.wrap_json_response(data=published_apps_data, code=ReturnCode.SUCCESS)
    # return JsonResponse(data=response, safe=False)
    query_set = App.objects.all()
    all_app = []
    for app in query_set:
        all_app.append(app.to_dict())
    print(all_app)
    response = CommonResponseMixin.wrap_json_response(data=all_app)
    return JsonResponse(data=response, safe=False)
class UserMenu(View, CommonResponseMixin):
    def get(self, request):
        if not already_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.UNAUTHORIZED)
            return JsonResponse(data=response,safe=False)
        open_id = request.session.get('open_id')
        user = User.objects.get(open_id=open_id)
        menu_list = user.menu.all()

        user_menu = []
        for app in menu_list:
            user_menu.append(app.to_dict())
        response = self.wrap_json_response(data=user_menu,code=ReturnCode.SUCCESS)
        return JsonResponse(response, safe=False)

    def post(self, request):
        if not already_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.UNAUTHORIZED)
            return JsonResponse(data=response,safe=False)
        user = get_user(request)
        post_menu = json.loads(request.body.decode('utf-8'))
        print(post_menu)
        post_menu = post_menu.get('data')
        focus_menu = []
        for item in post_menu:
            item = App.objects.get(appid=item.get('appid'))
            focus_menu.append(item)
        user.menu.set(focus_menu)
        user.save()
        response = self.wrap_json_response(code=ReturnCode.SUCCESS)
        return JsonResponse(response, safe=False)

