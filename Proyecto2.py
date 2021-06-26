from flask import Flask,request,Response
from flask_cors import CORS


app=Flask(__name__)
cors=CORS(app,resources={r'/*':{'origin':'*'}}) #ips externas



@app.route('/')
def index():
    return 'Hola Mundo'

@app.route('/datos',methods=['GET'])
def GET_datos():
    files=open('prueba.txt')
    
    return Response(status=200,response=files.read(),content_type='text/plain')

@app.route('/datos',methods=['POST'])
def POST_datos():
    file=request.data.decode('utf-8')
    files=open('prueba.txt','w')
    files.write(file)
    files.close()
    return Response(status=204)
if __name__=="__main__":
    app.run(debug=True)