from django.urls import path, re_path
from .views import RegisterUserEmpleadoView, ValidacionUserViews, SendEmailValidacionView, LoginUserEmpleado, UploadUserEmpleado, DeleteUserView


urlpatterns = [
    path('registerEmpleado', RegisterUserEmpleadoView.as_view()), 
    re_path(r'^validacionEmpleado/(?P<correo>[\w-]+)$', ValidacionUserViews.as_view()),
    path('sendEmailValidacionEmpleado', SendEmailValidacionView.as_view()),
    path('loginEmpleado', LoginUserEmpleado.as_view()),
    path("uploadEmpleado", UploadUserEmpleado.as_view()),
    re_path(r'^deleteEmpleado/(?P<cedula>[\w-]+)$', DeleteUserView.as_view())
]
