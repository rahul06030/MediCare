from django.urls import path
from . import views

app_name = "diabities"



urlpatterns = [
	path("", views.homepage, name='homepage'),
	path("train/" , views.trainD, name="train"),
    path('predict/', views.predictD, name='submit_prediction'),
    path('db/', views.view_results, name='results'),
]