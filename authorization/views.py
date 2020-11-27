import json
from django.http import JsonResponse
from django.views import View
from .models import User
from utils.auth import c2s, already_authorized
from utils.response import CommonResponseMixin, ReturnCode


def test_session(request):
    request.session['message'] = 'test django session ok'
    response = CommonResponseMixin.wrap_json_response(code=ReturnCode.SUCCESS)
    return JsonResponse(data=response, safe=False)

def get_staus(request):
    if already_authorized(request):
        data = {"is_authorized": 1}
    else:
        data = {"is_authorized": 0}
    response = CommonResponseMixin.wrap_json_response(data=data, code=ReturnCode.SUCCESS)
    return JsonResponse(data=response, safe=False)

def logout(request):
    request.session.clear()
    response = {}
    response['result_code'] = 0
    response['message' ] = 'logout success'
    return JsonResponse(data=response, safe=False)

class UserView(View, CommonResponseMixin):
    def get(self, request):
        if not already_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.SUCCESS)
            return JsonResponse(data=response, safe=False)

        open_id = request.session.get('open_id')
        user = User.objects.get(open_id=open_id)
        data = {}
        data['focus'] = {}
        print('user.focus_cities is:', user.focus_cities)
        print('user.focus_cropIds is:', user.focus_cropIds)
        data['focus']['city'] = json.loads(user.focus_cities)
        data['focus']['cropId'] = json.loads(user.focus_cropIds)
        print('data is:', data)
        response = self.wrap_json_response(data=data, code=ReturnCode.SUCCESS)
        return JsonResponse(data=response,safe=False)


    def post(self, request):
        if not already_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.UNAUTHORIZED)
            return JsonResponse(response, safe=False)
        open_id = request.session.get('open_id')
        user = User.objects.get(open_id=open_id)
        # got str object
        received_body = request.body.decode('utf-8')
        received_body = eval(received_body)

        cities = received_body.get('city')
        cropIds = received_body.get('cropId')
        if cities == None: cities = []
        if cropIds == None: cropIds = []

        user.focus_cities = json.dumps(cities)
        user.focus_cropIds = json.dumps(cropIds)
        user.save()
        message = 'modify user info success.'
        response = CommonResponseMixin.wrap_json_response(code=ReturnCode.SUCCESS, message=message)
        return JsonResponse(response, safe=False)

def __authorize_by_code(request):
    post_data = request.body.decode('utf-8')
    post_data = json.loads(post_data)
    code = post_data.get('code').strip()
    app_id = post_data.get('appId').strip()
    nickname = post_data.get('nickname').strip()

    response = {}
    if not code or not app_id:
        response['message'] = 'authorized failed,need entire authorization data'
        response['code'] = ReturnCode.BROKEN_AUTHORIZED_DATA
        return JsonResponse(data=response, safe=False)

    data = c2s(app_id, code)
    openid = data.get('openid')
    print('get oppid:', openid)

    request.session['open_id'] = openid
    request.session['is_authorized'] = True

    if not User.objects.filter(open_id=openid):
        new_user = User(open_id=openid,nickname=nickname)
        print('new_user open_id:%s,nickname: %s' %(openid, nickname))
        new_user.save()
    response = CommonResponseMixin.wrap_json_response(code=ReturnCode.SUCCESS, message='authorize success')
    return JsonResponse(data=response, safe=False)
def authorize(request):
    return __authorize_by_code(request)

def test_session2(request):
    print('request.session is:',request.session.items())
    response = CommonResponseMixin.wrap_json_response(code=ReturnCode.SUCCESS)
    return JsonResponse(data=response, safe=False)
