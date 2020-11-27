from django.urls import path
from .views import weather, menu, image, service

urlpatterns = [
    path('weather', weather.WeatherView.as_view()),
    path('menu/list', menu.get_menu),
    path('menu/user', menu.UserMenu.as_view()),
    # path('image', image.image),
    # path('imagetext', image.image_text),
    path('image', image.ImageView.as_view()),
    path('image/list', image.ImageListView.as_view()),
    path('cropId', service.cropId),
    path('joke', service.joke),
]