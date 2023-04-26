from django.db import models

# Create your models here.
import os 


class Doctor(models.Model):
    dname = models.CharField(max_length=100)
    demail = models.EmailField(max_length=100)
    dphone = models.CharField(max_length=20)
    daddress = models.CharField(max_length=200)

    

class Pdf(models.Model):
    image=models.FileField(upload_to="app/static/pdfs")


class Brain(models.Model):
    image=models.ImageField(upload_to="app/static/saved")

    def Imagename(self):
        return os.path.basename(self.image.name)
    

class Register(models.Model):
    remail=models.EmailField(max_length=50)
    rpassword=models.CharField(max_length=50)