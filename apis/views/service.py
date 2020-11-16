import json
import os
import random
from django.http import JsonResponse
from backend import settings
from thirdparty import juhe
from utils.auth import already_authorized, get_user
from utils.response import CommonResponseMixin, ReturnCode

all_constellations = ['白羊座', '金牛座', '双子座', '巨蟹座', '狮子座', '处女座', '天秤座', '天蝎座', '射手座', '摩羯座', '水瓶座', '双鱼座']
all_jokes = []
def constellation(request):
    response = []
    if already_authorized(request):
        user = get_user(request)
        constellations = json.loads(user.focus_constellations)
    else:
        constellations = all_constellations
    for c in constellations:
        data = juhe.constellation(c)
        response.append(data)
    response = CommonResponseMixin.wrap_json_response(data=response, code=ReturnCode.SUCCESS)
    return JsonResponse(data=response, safe=False)

def joke(request):
    global all_jokes
    if not all_jokes:
        all_jokes = json.load(open(os.path.join(settings.BASE_DIR, 'jokes.json'), 'r'))
    limits = 10
    joke_sample = random.sample(all_jokes, limits)
    response = CommonResponseMixin.wrap_json_response(data=joke_sample)
    return JsonResponse(data=response, safe=False)





