from django.urls import path , include
from . import views
urlpatterns = [
 
 path('signup/', views.signup, name='signup'),
 path('update/<str:email>', views.update, name='update'),
 path('delete/<str:email>', views.delete, name='delete'),
 path('getall/', views.getall, name='getall'),
 path('setpassword/<str:token>/', views.setpassword, name='setpassword'),
 path('login/', views.login, name='login'),
 path('showdatacurrentlastmonth/', views.showdatacurrentlastmonth, name='logshowdatacurrentlastmonthin')
]