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
            response = []
            for key in cities:
                item = key.get('area')
                item = item[:-1]
                data = juhe.weather(item)
                data['province'] = key.get('province')
                data['city'] = key.get('city')
                data['area'] = key.get('area')
                response.append(data)
            data = self.wrap_json_response(data=response)
            print('Return get response is:', data)
            return JsonResponse(data=data, safe=False)

    def post(self, request):
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        print('Received_body is:', received_body)
        cities = received_body.get('cities')
        print('Cities is: ', cities)
        data = []
        for key in cities:
            item = key.get('area')
            item = item[:-1]
            print('Return city is:', item)
            response = juhe.weather(item)
            print('Return response is: ',response)
            response['province'] = key.get('province')
            response['city'] = key.get('city')
            response['area'] = key.get('area')
            data.append(response)
        data = self.wrap_json_response(data=data)
        print('Return data is: ', data)
        return JsonResponse(data=data, safe=False)