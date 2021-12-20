from django.urls import path, include
from .views import RegisterUserProView, LoginUserProView, LogoutUserProView, ReadProViews, UpdateProView, ReadProViewsIndividual,EliminarCuentaViews

urlpatterns = [
    path('registerPropietario', RegisterUserProView.as_view()),
    path('loginPropietario', LoginUserProView.as_view()),
    path('readPropietarioAll', ReadProViews.as_view()),
    path('logoutPropietario', LogoutUserProView.as_view()),
    path('uploadPropietario', UpdateProView.as_view()),
    path('readPropietario', ReadProViewsIndividual.as_view()),
    path('eliminarProietario', EliminarCuentaViews.as_view())
]