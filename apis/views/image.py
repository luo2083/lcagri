import os
import hashlib

from django.http import Http404, JsonResponse, HttpResponse, FileResponse
from django.views import View
from backend import settings
from utils.response import CommonResponseMixin, ReturnCode


class ImageListView(View, CommonResponseMixin):
    def get(self, request):
        image_files = os.listdir(settings.IMAGES_DIR)
        print(image_files)
        response_data = []
        for image_file in image_files:
            response_data.append(
                {
                    "name": image_file,
                    "md5": image_file[:-4]
                }
            )
        response_data = self.wrap_json_response(data=response_data)
        return JsonResponse(data=response_data, safe=False)

class ImageView(View, CommonResponseMixin):
    def get(self, request):
        md5 = request.GET.get('md5')
        imgfile = os.path.join(settings.IMAGES_DIR, md5 + '.jpg')
        print(imgfile)
        if os.path.exists(imgfile):
            data = open(imgfile, 'rb').read()
            # return HttpResponse(data, content_type='image/jpg')
            return FileResponse(open(imgfile, 'rb'), content_type='image/jpg')
        else:
            return Http404()
    def post(self, request):
        files = request.FILES
        response = []
        for key, value in files.items():
            content = value.read()
            md5 = hashlib.md5(content).hexdigest()
            path = os.path.join(settings.IMAGES_DIR, md5 + '.jpg')
            with open(path, 'wb') as f:
                f.write(content)
            response.append({
                "name": key,
                "md5": md5
            })
        print('response is: ', response)
        message = 'post method success'
        response = self.wrap_json_response(data=response,code=ReturnCode.SUCCESS, message=message)

        return JsonResponse(data=response, safe=False)


    def delete(self, request):
        md5 = request.GET.get('md5')
        filename = md5 + '.jpg'
        path = os.path.join(settings.IMAGES_DIR, filename)
        if os.path.exists(path):
            os.remove(path)
            message = 'delete method success'
        else:
            message = 'image %s not exists' % filename
        data = self.wrap_json_response(message=message)
        return JsonResponse(data=data, safe=False)
def image_text(request):
    if request.method == 'GET':
        md5 = request.GET.get('md5')
        imgfile = os.path.join(settings.IMAGES_DIR, md5 + '.jpg')
        if not os.path.exists(imgfile):
            return CommonResponseMixin.wrap_json_response(code=ReturnCode.RESOURCES_NOT_EXISTS)
        else:
            response_data = {}
            response_data["name"] = md5 + '.jpg'
            response_data["url"] = "/service/image?md5=%s" %(md5)
            data = CommonResponseMixin.wrap_json_response(data=response_data)
            return JsonResponse(data=data, safe=False)