from django.shortcuts import render, redirect
import os
import requests
import re
#import pdfplumber
from gtts import gTTS
from urllib.request import Request, urlopen
from  . Chat.chat_bot import Chatting
from PyPDF2 import PdfWriter, PdfReader
from io import BytesIO
# Create your views here.

from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np
from . models import *
import os


def add_doctor(request):
    if request.method == 'POST':
        lname=request.POST['docname']
        lemail=request.POST['email']
        lphone=request.POST['phnumber']
        laddress=request.POST['add']
        data=Doctor(dname=lname,demail=lemail,dphone=lphone,daddress=laddress)
        data.save()
        teext='Doctor Added'
        return render(request,'adddoctor.html',{"text":teext})
    return render(request, "adddoctor.html")

# Create your views here.

def login(request):
    if request.method=='POST':
        lemail=request.POST['email']
        lpassword=request.POST['psw']

        d=Register.objects.filter(remail=lemail,rpassword=lpassword).exists()
        print(d)
        if d:
            return render (request,"upload.html")

    return render(request,'login.html')

def register(request):
    if request.method=='POST':
        email=request.POST['useremail']
        password=request.POST['psw']
        conpassword=request.POST['conpassword']
        print(email,password,conpassword)
        if password==conpassword:
            a=Register(remail=email,rpassword=password)
            a.save()
            msg="succesfully registered"
            return render(request,'login.html',{"message":msg})
        else:
            msg='Register failed!!'
            return render(request,'register.html')

        
    return render(request,'register.html')


          
    
def index(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")


def stages(request):
    if request.method=='POST':
        Classes=[]
        paths=os.listdir('app/data/')
        for i in paths:
            Classes.append(i)
        File=request.FILES['brain']
        s=Brain(image=File)
        s.save()
        path1='app/static/saved/' + s.Imagename()

        model=load_model('app/models/CNN_1.h5',compile=False)
        x1=image.load_img(path1,target_size=(128,128))
        x1=image.img_to_array(x1)
        x1=np.expand_dims(x1,axis=0)
        x1/=255
        result= model.predict(x1)        
        # a = classes[]
        b = np.argmax(result)
        results=Classes[b]
        print(results)
        results=results.upper()

        
        
        from random import randint
        # count = Doctor.objects.count()
        # print(count)
        dc = Doctor.objects.all().order_by('?')[:4]
        print(dc)

        return render(request,"result.html",{"message":results,"DOC":dc,"path":'/static/saved/' + s.Imagename()})
    return render(request,"stages.html")


def upload(request):
    if request.method=='POST':
        pdfs=request.FILES['pdf']
        """ p=Pdf(image=pdfs)
        p.save() """
        
        #newly added code-----------------
        reader=PdfReader(pdfs)
        pdfFile=reader
        #memoryFile=BytesIo(resp)
        #pdfFile = PdfReader(memoryFile)
        final_measurements = {}
        for i in range(len(pdfFile.pages)):
            pageObj = pdfFile.pages[i]
            data = pageObj.extract_text()
            wbc1=re.search(r'(\bHaemoglobin\b).+(\b\d+\.\d+)',data)
            hemoglobin = re.search(r'(\bHemoglobin\b).+(\b\d+\.\d+)',data)
            rbc_count = re.search(r'(\bRBC\b).+(\b\d+\.\d+)',data)
            rdw = re.search(r'(\b(RDW)\b).+(\b\d+\.\d+)',data)
            tlc = re.search(r'(\b(TLC)\b).+(\b\d+\.\d+)',data)

            # Differential Leucocyte Count (DLC)
            lymph = re.search(r'(\bLymphocytes\b).+(\b\d+\.\d+)',data)
            mono = re.search(r'(\bMonocytes\b).+(\b\d+\.\d+)',data)

            platelet_count = re.search(r'(\bPlatelet Count\b).+(\b\d+\.\d+)',data)

            if hemoglobin:
                final_measurements['hemoglobin'] = hemoglobin.groups()[-1]
            if rbc_count:
                final_measurements['rbc_count'] = rbc_count.groups()[-1]
            if rdw:
                final_measurements['rdw'] = rdw.groups()[-1]
            if tlc:
                final_measurements['tlc'] = tlc.groups()[-1]
            if lymph:
                final_measurements['lymph'] = lymph.groups()[-1]
            if mono:
                final_measurements['mono'] = mono.groups()[-1]
            if platelet_count:
                final_measurements['plc'] = platelet_count.groups()[-1]
            if wbc1:#added
                final_measurements['Haemoglobin'] = wbc1.groups()[-1]
            
            try:
                wb=float(final_measurements['hemoglobin'])
            except:
                wb=float(final_measurements['Haemoglobin'])

        #end of newly added code------------
        
        
        if wb>= 16:
            text= "Chance of Acute Lymphoblastic Leukemia is Positve"
            return render(request,"pdfresult.html",{'pdfr':text})
        else:		  
            text="Chance of Acute Lymphoblastic Leukemia is Negative"
            return render(request,"mytest.html",{'pdfr':text})
        
        return render(request,"pdfresult.html",{'pdfr':text})

    return render (request,"upload.html")


def Chatbot(request):
    Chatting()
    print("Chatting")
    return render (request,"stages.html")


