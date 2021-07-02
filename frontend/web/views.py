#from django.conf.urls import url
from django.shortcuts import render,redirect
import requests
import csv
import re
from xml.etree import ElementTree as ET
from xml.dom import minidom

from requests.models import encode_multipart_formdata, parse_url
from werkzeug.wrappers import response

class Clientes:
    def __init__(self, nombre,apellido,edad,fechacump,fechaprim):
        self.nombre=nombre
        self.apellido=apellido
        self.edad=edad
        self.fechacump=fechacump
        self.fechaprim=fechaprim

class MejoresCl:
    def __init__(self,nombre,fechault,cantidadcomp,gastada):
        self.nombre=nombre
        self.fechault=fechault
        self.cantidadcomp=cantidadcomp
        self.gastada=gastada
class Juegosven:
    def __init__(self,nombre,fechault,copiasven,stock):
        self.nombre=nombre
        self.fechault=fechault
        self.copiasven=copiasven
        self.stock=stock
class Juegos:
    def __init__(self,nombre,plataforma,año,clasif,stock):
        self.nombre=nombre
        self.plataforma=plataforma
        self.año=año
        self.clasif=clasif
        self.stock=stock

        
#-------listasprincipales----
listacl=[]
listamjcl=[]
listajven=[]
listajuegos=[]

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
            datascsv=csv.DictReader(f,delimiter=';',skipinitialspace=True)
            for f in datascsv:
                nombre=f.get('Nombre')
                nom=re.findall('[a-zA-ZáéíóúñÑ]',nombre)
                Ncl=(''.join(nom))
                apellidos=f.get('Apellido')
                ape=re.findall('[a-zA-ZáéíóúñÑ]',apellidos)
                Apecl=(''.join(ape))
                edad=f.get('Edad')
                ed=re.findall('[0-9]',edad)
                Edadcl=(''.join(ed))
                fechanac=f.get('FechaCumpleaños')
                fnac=re.findall('^([0-9]{2}/)([0-1][0-9]{1}/)([0-9]{4})$',fechanac)
                Fechacump=(''.join(fnac[0]))
                fechapc=f.get('FechaPrimeraCompra')
                fpc=re.findall('^([0-9]{2}/)([0-1][0-9]{1}/)([0-9]{4})$',fechapc)
                Fechaprim=(''.join(fpc[0]))
                listacl.append(Clientes(Ncl,Apecl,Edadcl,Fechacump,Fechaprim))
        doccsv2=request.FILES['document2']
        mejorescscsv=doccsv2.name
        with open(mejorescscsv,newline='',encoding='utf-8') as m:
            datamejcl=csv.DictReader(m,delimiter=';',skipinitialspace=True)
            
            for cl in datamejcl:
                nombrecl=cl.get('Nombre')
                mejcl=re.findall('[a-zA-ZáéíóúñÑ]',nombrecl)
                nombremjcl=(''.join(mejcl))
                fechaucp=cl.get('FechaUtlimaCompra')
                fucp=re.findall('^([0-9]{2}/)([0-1][0-9]{1}/)([0-9]{4})$',fechaucp)
                Fucp=(''.join(fucp[0]))
                cantc=cl.get('CantidadComprada')
                cantidadcomp=re.findall('[0-9]',cantc)
                Cantcomp=(''.join(cantidadcomp))
                gasto=cl.get('CantidadGastada')
                totalgasto=re.findall('[0-9.]+',gasto)
                Gasto=(''.join(totalgasto))
                listamjcl.append(MejoresCl(nombremjcl,Fucp,Cantcomp,Gasto))
        doccsv3=request.FILES['document3']
        juegosven=doccsv3.name
        with open (juegosven,newline='',encoding='utf-8')as v:
            dataven=csv.DictReader(v,delimiter=';',skipinitialspace=True)
            for jv in dataven:
                nomjven=jv.get('Nombre')
                Juegosvem=(''.join(nomjven))
                fechacomp=jv.get('FechaUltimaCompra')
                fultimacom=re.findall('^([0-9]{2}/)([0-1][0-9]{1}/)([0-9]{4})$',fechacomp)
                Fechaultimac=(''.join(fultimacom[0]))
                copias=jv.get('CopiasVendidas')
                copiasven=re.findall('[0-9]',copias)
                Copias=(''.join(copiasven))
                cant=jv.get('Stock')
                stock=re.findall('[0-9]',cant)
                Stock=(''.join(stock))
                listajven.append(Juegosven(Juegosvem,Fechaultimac,Copias,Stock))
        doccsv4=request.FILES['document4']
        juegos=doccsv4.name
        with open(juegos,newline='',encoding='utf-8')as j:
            juegosdata=csv.DictReader(j,delimiter=';',skipinitialspace=True)
            for jd in juegosdata:
                nombrej=jd.get('Nombre')
                Nomj=(''.join(nombrej))
                plaraforma=jd.get('Plataforma')
                Plat=(''.join(plaraforma))
                alanz=jd.get('AñoLanzamiento')
                lanzamiento=re.findall('[0-9]{4}',alanz)
                Lanz=(''.join(lanzamiento))
                clas=jd.get('Clasificación')
                clasif=re.findall('[EMT]',clas)
                Clasif=(''.join(clasif))
                cants=jd.get('Stock')
                stockj=re.findall('[0-9]',cants)
                Stockjuego=(''.join(stockj))
                listajuegos.append(Juegos(Nomj,Plat,Lanz,Clasif,Stockjuego))
        
        

        xml_doc=minidom.Document()
        root=xml_doc.createElement('CHET')
        

        for i in listacl:
            c=0
            c=c+1
            cliente_e=xml_doc.createElement('cliente'+str(c))
            root.appendChild(cliente_e)
            nombre_e=xml_doc.createElement('nombre')
            nombre_e.appendChild(xml_doc.createTextNode(i.nombre))
            cliente_e.appendChild(nombre_e)

            apellido_e=xml_doc.createElement('apellido')
            apellido_e.appendChild(xml_doc.createTextNode(i.apellido))
            cliente_e.appendChild(apellido_e)

            
            
        xml_f=root.toprettyxml(indent='\t',encoding='utf-8')    
        
        url=endpoint.format('/datos')
        requests.post(url,xml_f)
        return redirect('index')
