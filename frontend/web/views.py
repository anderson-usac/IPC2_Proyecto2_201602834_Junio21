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

#-----listassecundarias-----------
listaNombre=[] #nombre cl 
listaApellido=[] #apellido cl
listaEdad=[] #edad cl
listaFechacump=[] #cumpleaños cl
listaFechaprimera=[] #primra compra cl
listanombremjcl=[] #mejor cl
listafucp=[] #fecha ultima compra
listacantcomp=[] #compras cantidad
listagasto=[] #total gastado
listajuegosvem=[] #nombre juegos vendidos
listafechaultimac=[] #fecha ultima compra
listacopias=[] #copias vendidas
listastock=[] #lista stock
listanomj=[] #juegos
listaplat=[] #plataformas
listalanz=[] #fecha lanz
listaclasif=[] #clasif de juego
listastockjuego=[] #stocks
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
                listaNombre.append(''.join(nom))
                apellidos=f.get('Apellido')
                ape=re.findall('[a-zA-ZáéíóúñÑ]',apellidos)
                listaApellido.append(''.join(ape))
                edad=f.get('Edad')
                ed=re.findall('[0-9]',edad)
                listaEdad.append(''.join(ed))
                fechanac=f.get('FechaCumpleaños')
                fnac=re.findall('^([0-9]{2}/)([0-1][0-9]{1}/)([0-9]{4})$',fechanac)
                listaFechacump.append(''.join(fnac[0]))
                fechapc=f.get('FechaPrimeraCompra')
                fpc=re.findall('^([0-9]{2}/)([0-1][0-9]{1}/)([0-9]{4})$',fechapc)
                listaFechaprimera.append(''.join(fpc[0]))
        doccsv2=request.FILES['document2']
        mejorescscsv=doccsv2.name
        with open(mejorescscsv,newline='',encoding='utf-8') as m:
            datamejcl=csv.DictReader(m,delimiter=';',skipinitialspace=True)
            
            for cl in datamejcl:
                nombrecl=cl.get('Nombre')
                mejcl=re.findall('[a-zA-ZáéíóúñÑ]',nombrecl)
                listanombremjcl.append(''.join(mejcl))
                fechaucp=cl.get('FechaUtlimaCompra')
                fucp=re.findall('^([0-9]{2}/)([0-1][0-9]{1}/)([0-9]{4})$',fechaucp)
                listafucp.append(''.join(fucp[0]))
                cantc=cl.get('CantidadComprada')
                cantidadcomp=re.findall('[0-9]',cantc)
                listacantcomp.append(''.join(cantidadcomp))
                gasto=cl.get('CantidadGastada')
                totalgasto=re.findall('[0-9.]+',gasto)
                listagasto.append(''.join(totalgasto))
        doccsv3=request.FILES['document3']
        juegosven=doccsv3.name
        with open (juegosven,newline='',encoding='utf-8')as v:
            dataven=csv.DictReader(v,delimiter=';',skipinitialspace=True)
            for jv in dataven:
                nomjven=jv.get('Nombre')
                listajuegosvem.append(''.join(nomjven))
                fechacomp=jv.get('FechaUltimaCompra')
                fultimacom=re.findall('^([0-9]{2}/)([0-1][0-9]{1}/)([0-9]{4})$',fechacomp)
                listafechaultimac.append(''.join(fultimacom[0]))
                copias=jv.get('CopiasVendidas')
                copiasven=re.findall('[0-9]',copias)
                listacopias.append(''.join(copiasven))
                cant=jv.get('Stock')
                stock=re.findall('[0-9]',cant)
                listastock.append(''.join(stock))
        doccsv4=request.FILES['document4']
        juegos=doccsv4.name
        with open(juegos,newline='',encoding='utf-8')as j:
            juegosdata=csv.DictReader(j,delimiter=';',skipinitialspace=True)
            for jd in juegosdata:
                nombrej=jd.get('Nombre')
                listanomj.append(''.join(nombrej))
                plaraforma=jd.get('Plataforma')
                listaplat.append(''.join(plaraforma))
                alanz=jd.get('AñoLanzamiento')
                lanzamiento=re.findall('[0-9]{4}',alanz)
                listalanz.append(''.join(lanzamiento))
                clas=jd.get('Clasificación')
                clasif=re.findall('[EMT]',clas)
                listaclasif.append(''.join(clasif))
                cants=jd.get('Stock')
                stockj=re.findall('[0-9]',cants)
                listastockjuego.append(''.join(stockj))
        
        listacl.append(Clientes(listaNombre,listaApellido,listaEdad,listaFechacump,listaFechaprimera))
        listamjcl.append(MejoresCl(listanombremjcl,listafucp,listacantcomp,listagasto))
        listajven.append(Juegosven(listajuegosvem,listafechaultimac,listacopias,listastock))
        listajuegos.append(Juegos(listanomj,listaplat,listalanz,listaclasif,listastockjuego))

        xml_doc=minidom.Document()
        root=xml_doc.createElement('CHET')

        for i in listacl:
            varn=' '.join(i.nombre)
            cliente_e=xml_doc.createElement('nombre')
            cliente_e.appendChild(xml_doc.createTextNode(i.nombre))
            root.appendChild(cliente_e)
        xml_f=root.toprettyxml(indent='\t',encoding='utf-8')    
        
        url=endpoint.format('/datos')
        requests.post(url,xml_f)
        return redirect('index')
