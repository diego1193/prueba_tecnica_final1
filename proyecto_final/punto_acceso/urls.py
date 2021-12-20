from django.urls import path, include, re_path
from .views import RegisterPuntoAccesoViews, ReadPuntosAccesoViews, ReadPuntoAccesoIndividualViews, UpdatePuntoAccesoViews, DeletePuntoAccesoView

urlpatterns = [
    path('registerPuntoAccceso', RegisterPuntoAccesoViews.as_view()),
    path('readAllPuntoAcceso', ReadPuntosAccesoViews.as_view()),
    re_path(r'^readPuntoAcessoInd/(?P<company>[\w-]+)$', ReadPuntoAccesoIndividualViews.as_view()),
    path('updatePuntoAcceso', UpdatePuntoAccesoViews.as_view()),
    path('deletePuntoAccesoView', DeletePuntoAccesoView.as_view())
]