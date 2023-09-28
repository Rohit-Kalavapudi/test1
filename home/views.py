from django.shortcuts import render,HttpResponse
from home.models import Contact
from datetime import datetime
from django.contrib import messages
import pickle
from django.core.files.storage import FileSystemStorage
import tensorflow as tf
from keras.models import load_model
import tensorflow_hub as hub
import numpy as np 
import cv2
import os
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
# from django.shortcuts import render,HttpResponse,redirect
# from django.core.files.storage import FileSystemStorage
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate,logout
# from django.contrib import messages
# from django.contrib.auth import login
from django.shortcuts import render,HttpResponse,redirect
# from eyes.models import Information
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required

# Create your views here.

# user=None    
def index(request):
    return render(request,'index.html')

def predict(img,model):
    img1=mpimg.imread(img)
    img1=cv2.resize(img1,(224,224),3)
    img1=np.array(img1)/255.0
    img1[np.newaxis,...].shape
    prediction=model.predict(img1[np.newaxis,...])
    prediction=np.argmax(prediction)
    # ar=np.array([left])
    # prediction=model.predict()
    # print(prediction)
    if (prediction==0):
        res='no dr'
    elif(prediction==1):
        res= 'mild dr'
    elif(prediction==2):
        res= 'moderate dr'
    elif(prediction==3):
        res= 'severe'
    else:
        res= 'proliferate'  
    return res
def contact(request):
    if(request.method=='POST'):
        name= request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        desc=request.POST.get('desc')
        left=request.FILES.get('left')
        right=request.FILES.get('right')
        model=tf.keras.models.load_model('final.h5', custom_objects={'KerasLayer':hub.KerasLayer})
        res1=predict(left,model)
        res2=predict(right,model)
        fs = FileSystemStorage()
        f1 = fs.save(left.name,left)
        f2 = fs.save(right.name,right)
        f1 = fs.url(left)
        f2 = fs.url(right)
        contact=Contact(name=name,email=email,phone=phone,desc=desc,img1=left,img2=right,res1=res1,res2=res2,date=datetime.today())
        contact.save()
        print(res1)
        print(res2)
        d={'name':name,'email':email,'phone':phone,'desc':desc,'img1':f1,'img2':f2,'res1':res1,'res2':res2,'date':datetime.today(),'ans1':res1,'ans2':res2}
        return render(request,'result.html',d)
    return render(request,'contact.html')


def display(request):
    
    if request.user.is_authenticated:
        d=Contact.objects.all()
        context={
            "obj":d
        }
        return render(request,"display.html",context)
    else:
        return redirect('signin')

# @login_required
    # def display(request):
    #     d = Contact.objects.all()
    #     context = {
    #         "obj": d
    #     }
    #     return render(request, "display.html", context)

def start(request):
    return render(request,'start.html') 
def land(request):
    return render(request,'home.html')
def doctors(request):
    return render(request,'doctors.html')



def update(request,id):
    if(request.method=='POST'):
        
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        desc=request.POST.get('desc')
        date=datetime.now() 
        cr=Contact(id=id,name=name,email=email,phone=phone,desc=desc,date=date)
        cr.save()
        std=Contact.objects.all()   
        return  redirect('index')
def delete(request,id):
    std=Contact.objects.filter(id=id).delete()
    context={
        'std':std,
    }
    return redirect('index') 
def search(request):
    if request.method=='POST':
        search=request.POST.get('query')
        print(search)
        std=Contact.objects.filter(name=search)
        print(std)
        return render(request,'search.html',{'search':search,'obj':std})




def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
 
        myuser = User.objects.create_user(username,email,password)
        print("User successfully created")
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request,"hey your account has been created successfully")
        return redirect('signin')
    return render(request,'signup.html')


def signin(request):
    if request.method == 'POST':
        name = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=name, password=password)
        if user is not None:
            auth_login(request, user)
            # User is authenticated, redirect to the desired page.
            return redirect('display')
        else:
            messages.error(request, 'Bad Credentials')
            return redirect('signin')
    return render(request, 'signin.html')


def signout(request):
    print('hello')
    logout(request)
    print(request.user.is_authenticated)
    return redirect('home')