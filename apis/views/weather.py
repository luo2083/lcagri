import json
from django.http import JsonResponse, HttpResponse
from django.views import View

from authorization.models import User
from thirdparty import juhe
from utils.response import CommonResponseMixin, ReturnCode
from utils.auth import already_authorized
class WeatherView(View, CommonResponseMixin):
    def get(self, request):
        if not already_authorized(request):
            response = self.wrap_json_response(data={}, code=ReturnCode.UNAUTHORIZED)
        else:
            open_id = request.session.get('open_id')
            user = User.objects.filter(open_id=open_id)[0]
            cities = json.loads(user.focus_cities)
            data = []
            for item in cities:
                city = item.get('city')
                response = juhe.weather(city)
                data.append(response)
            response = self.wrap_json_response(data=data, code=ReturnCode.SUCCESS)
            return JsonResponse(data=response, safe=False)

    def post(self, request):
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        cities = received_body.get('cities')
        data = []
        for item in cities:
            city = item.get('city')
            response = juhe.weather(city)
            data.append(response)
        data = self.wrap_json_response(data=data)
        return JsonResponse(data=data, safe=False)