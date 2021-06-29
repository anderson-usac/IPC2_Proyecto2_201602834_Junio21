#from django.conf.urls import url
from django.shortcuts import render,redirect
import requests
import csv
import re
from xml.etree import ElementTree as ET
from xml.dom import minidom

from requests.models import encode_multipart_formdata, parse_url

endpoint= 'http://localhost:5000/{}'
# Create your views here.
def index(request):
    if request.method=='GET':
        url=endpoint.format('/datos')
        doccsv=requests.get(url)
        context={'doccsv':doccsv.text,}
        return render(request,'index.html',context)
    elif request.method=='POST':
        doccsv = request.FILES['document']
        decoded_file = doccsv.read().decode('UTF-8')
        reader = csv.reader(decoded_file,delimiter=',',skipinitialspace=True)
        for row in reader:  
            print(row,end='')
        
        #     nombre=f.get('Nombre')
        #     nom=re.findall('[a-zA-ZáéíóúñÑ]',nombre)
        #     print(''.join(nom))
        #     apellidos=f.get('Apellido')
        #     ape=re.findall('[a-zA-ZáéíóúñÑ]',apellidos)
        #     edad=f.get('Edad')
        #     ed=re.findall('[0-9]',edad)
        #     fechanac=f.get('Fecha de cumpleaños')
        #     fnac=re.findall('^([0-9]{2}/)([0-1][0-9]{1}/)([0-9]{4})$',fechanac)
        #     fechapc=f.get('Fecha primera compra')
        #     fpc=re.findall('^([0-9]{2}/)([0-1][0-9]{1}/)([0-9]{4})$',fechapc)
            
        url=endpoint.format('/datos')
        requests.post(url,decoded_file)
        return redirect('index')
