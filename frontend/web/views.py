#from django.conf.urls import url
from django.shortcuts import render,redirect
import requests

endpoint= 'http://localhost:5000/{}'
# Create your views here.
def index(request):
    if request.method=='GET':
        url=endpoint.format('/datos')
        data=requests.get(url)
        context={'data':data.text,}
        return render(request,'index.html',context)
    elif request.method=='POST':
        doc=request.FILES['document']
        data=doc.read()
        url=endpoint.format('/datos')
        requests.post(url,data)
        return redirect('index')