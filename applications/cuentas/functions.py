import datetime as dt


def generarfechas(fecha_inicio,fecha_venci,cuotas):
    fechas_inicio=[]
    fechas_venc=[]
    
    #ahora=dt.datetime.today()
    for c in range(cuotas):

        if c!=0:
            inicio=inicio + dt.timedelta(30)
        else:
            inicio= fecha_inicio


        
        mes=inicio.month
        año=inicio.year
        dia=inicio.day
        fecha=dt.datetime(año,mes,dia)
        fechas_inicio.append(fecha)
        fecha_venc=dt.datetime(año,mes,fecha_venci.day)
        fechas_venc.append(fecha_venc)
        
        
        
    return fechas_inicio,fechas_venc
        