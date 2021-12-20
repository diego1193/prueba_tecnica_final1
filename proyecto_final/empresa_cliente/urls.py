from django.urls import path, include, re_path
from .views import RegisterClienteViews, ReadClientesViews, ReadClientesViewsIndividual, UpdateClienteView, DeleteClienteViews

urlpatterns = [
    path('registerCliente', RegisterClienteViews.as_view()),
    path('readAllCliente', ReadClientesViews.as_view()),
    re_path(r'^readIndCliente/(?P<nit>[\w-]+)$', ReadClientesViewsIndividual.as_view()),
    path('uploadCliente', UpdateClienteView.as_view()),
    re_path(r'^deleteCliente/(?P<nit>[\w-]+)$', DeleteClienteViews.as_view())
]