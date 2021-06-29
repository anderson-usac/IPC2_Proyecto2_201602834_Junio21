#from django.conf.urls import url
from django.shortcuts import render,redirect
import requests
import csv
import re

endpoint= 'http://localhost:5000/{}'
# Create your views here.
def index(request):
    if request.method=='GET':
        url=endpoint.format('/datos')
        doccsv=requests.get(url)
        context={'data':doccsv.text,}
        return render(request,'index.html',context)
    elif request.method=='POST':
        doccsv=request.FILES['document'].read()
        datacsv=csv.DictReader(doccsv)
        for f in datacsv:
            nombre=f.get('Nombre')
            nom=re.fullmatch('[a-zA-ZáéíóúñÑ]',nombre)
            apellidos=f.get('Aperllidos')
            ape=re.fullmatch('[a-zA-ZáéíóúñÑ]',apellidos)
            edad=f.get('Edad')
            ed=re.fullmatch('[0-9]',edad)
            fechanac=f.get('Fecha de cumpleaños')
            fnac=re.fullmatch('^(?:3[01]|[12][0-9]|0?[1-9])([\/])(0?[1-9]|1[1-2])\1\d{4}$',fechanac)
            fechapc=f.get('Fecha primera compra')
            fpc=re.fullmatch('^(?:3[01]|[12][0-9]|0?[1-9])([\/])(0?[1-9]|1[1-2])\1\d{4}$',fechapc)
            
        url=endpoint.format('/datos')
        requests.post(url,nom)
        return redirect('index')
