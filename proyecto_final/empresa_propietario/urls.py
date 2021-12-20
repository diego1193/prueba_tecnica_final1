from django.urls import path, include, re_path
from .views import RegisterEmpresaView, ReadEmpresaProViews, ReadEmpresaProViewsIndiviual, UpdateEmpresaProView, DeleteEmpresaProViewsIndiviual

urlpatterns = [
    path('registerEmpresa', RegisterEmpresaView.as_view()),
    path('readAllEmpresa', ReadEmpresaProViews.as_view()),
    re_path(r'^readIndEmpresa/(?P<nit>[\w-]+)$', ReadEmpresaProViewsIndiviual.as_view()),
    path('uploadEmpresa', UpdateEmpresaProView.as_view()),
    re_path(r'^deleteEmpresa/(?P<nit>[\w-]+)$', DeleteEmpresaProViewsIndiviual.as_view())
]