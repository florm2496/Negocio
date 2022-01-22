from django.urls import path
from .views import Estadisticas,ConfiguracionesAPIView





urlpatterns=[
    path('estadisticas/',Estadisticas.as_view(),name='estadisticas'),
    path('configuraciones/',ConfiguracionesAPIView.as_view() , name='configs'),
   
]