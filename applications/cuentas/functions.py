import datetime as dt


def generarfechas(dia_inicio,dia_venc,cuotas):
    fechas_inicio=[]
    fechas_venc=[]
    
    ahora=dt.datetime.today()
    for c in range(cuotas):
        
        inicio= ahora + dt.timedelta(30)
        mes=inicio.month
        año=inicio.year
        print(dia_inicio, mes, año)
        fecha=dt.datetime(año,mes,dia_inicio)
        fechas_inicio.append(fecha)
        fecha_venc=dt.datetime(año,mes,dia_venc)
        fechas_venc.append(fecha_venc)
        
        ahora=inicio
        
    return fechas_inicio,fechas_venc
        