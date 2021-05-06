from django.urls import path
from . import views

app_name = "predict"

# urlpatterns = [
#     path('', views.predict, name='prediction_page'),
#     path('predict/', views.predict_chances, name='submit_prediction'),
#     path('results/', views.view_results, name='results'),
# ]

urlpatterns = [
	path("", views.homepage, name='homepage'),
	path("train/" , views.train, name="train"),
    path('heart_disease/', views.predict, name='prediction_page'),
    path('predict/', views.predict_chances, name='submit_prediction'),
    path('db/', views.view_results, name='results'),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_request, name="logout"),
    path("login/", views.login_request, name="login"),
]