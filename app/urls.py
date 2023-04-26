from . import views
from django.urls import path

urlpatterns=[
    path("login",views.login,name='login'),
    path("register",views.register,name='register'),
    path("adddoctor",views.add_doctor,name='adddoctor'),
    path("",views.index,name='index'),
    path("stages",views.stages,name='stages'),
    path("result", views.stages,name='result'),
    path("about", views.about, name='about'),
    path("upload",views.upload,name='upload'),
    path("pdfresult", views.upload,name='pdfresult')
]