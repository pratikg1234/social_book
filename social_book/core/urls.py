from django.urls import path
from . import views
urlpatterns = [
    #views is the views.py in same directory
    path('',views.index,name='index')

]