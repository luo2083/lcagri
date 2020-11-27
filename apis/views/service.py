import json
import os
import random
from django.http import JsonResponse
from backend import settings
from thirdparty import juhe
from utils.auth import already_authorized, get_user
from utils.response import CommonResponseMixin, ReturnCode

all_cropIds = ['水稻', '葡萄', '柑橘']
all_jokes = []
def cropId(request):
    response = []
    if already_authorized(request):
        user = get_user(request)
        cropIds = json.loads(user.focus_cropIds)

    else:
        cropIds = all_cropIds

    response = CommonResponseMixin.wrap_json_response(data=cropIds, code=ReturnCode.SUCCESS)
    return JsonResponse(data=response, safe=False)

def joke(request):
    global all_jokes
    if not all_jokes:
        all_jokes = json.load(open(os.path.join(settings.BASE_DIR, 'jokes.json'), 'r'))
    limits = 10
    joke_sample = random.sample(all_jokes, limits)
    response = CommonResponseMixin.wrap_json_response(data=joke_sample)
    return JsonResponse(data=response, safe=False)





