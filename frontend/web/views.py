#from django.conf.urls import url
from django.shortcuts import render,redirect
import requests
import csv
import re
from xml.etree import ElementTree as ET
from xml.dom import minidom

from requests.models import encode_multipart_formdata, parse_url
from werkzeug.wrappers import response

listaNombre=[]
listaApellido=[]
listaEdad=[]
listaFechacump=[]
listaFechaprimera=[]
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
        filecsv = doccsv.name
        with open(filecsv,newline='',encoding='utf-8')as f:
            datascsv=csv.DictReader(f,delimiter=',',skipinitialspace=True)
            for f in datascsv:
                nombre=f.get('Nombre')
                nom=re.findall('[a-zA-ZáéíóúñÑ]',nombre)
                listaNombre.append(''.join(nom))
                apellidos=f.get('Apellido')
                ape=re.findall('[a-zA-ZáéíóúñÑ]',apellidos)
                listaApellido.append(''.join(ape))
                edad=f.get('Edad')
                ed=re.findall('[0-9]',edad)
                listaEdad.append(''.join(ed))
                fechanac=f.get('Fecha de cumpleaños')
                fnac=re.findall('^([0-9]{2}/)([0-1][0-9]{1}/)([0-9]{4})$',str(fechanac))
                listaFechacump.append(fnac)
                fechapc=f.get('Fecha primera compra')
                fpc=re.findall('^([0-9]{2}/)([0-1][0-9]{1}/)([0-9]{4})$',str(fechapc))
                listaFechaprimera.append(fpc)
        print('Nom:',listaNombre)
        print('Ape:',listaApellido)
        print('Edad:',listaEdad)
        print('fecha1_',listaFechacump)
        print('fecha2:',listaFechaprimera)    
        url=endpoint.format('/datos')
        requests.post(url,filecsv)
        return redirect('index')
