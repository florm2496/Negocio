import datetime as dt
import pytz
utc=pytz.UTC

from applications.cuentas.models import Cuentas,Cuotas

def update_dues(listacuentas):
    for c in listacuentas:
        cuotas = Cuotas.objects.filter(cuenta__numero_cuenta=c.numero_cuenta,vencida=False)
        for i in cuotas:
            venc=i.fecha_vencimiento
            if venc <=  utc.localize(dt.datetime.now()):
                i.vencida = True
            
                """inicialmente , el saldo sera igual al importe de la cuota , cada vez que se efectue 
                  un pago se descontara del saldo, y si la cuota vence y no esta saldada se aplicara un 
                  recargo al saldo
                
                """
                if i.estado == 'impaga':
                    i.recargo = i.saldo * 0.20
                    #i.saldo = i.saldo + i.recargo 
                i.save()

def get_cuentas(listacuentas,cuenta):
    update_dues(listacuentas)
    if cuenta is None:
        cuentas=Cuentas.objects.all()
    else:
        cuentas=Cuentas.objects.get(numero_cuenta=cuenta)
    return cuentas


def generar_fechas(fecha_venci,cuotas):
    fechas_venc=[]

    inicio=dt.datetime(fecha_venci.year,fecha_venci.month,1,23,59,59)
    #ahora=dt.datetime.today()
    for c in range(cuotas):

        if c!=0:
            fecha = inicio + dt.timedelta(30)
        else:
            fecha = inicio
  
        fechas_venc.append(fecha)
        inicio=fecha
        
        
        
    return fechas_venc

def actualizarstock(productos,cantidades):
    
    for p,c in zip(productos,cantidades):
        
        p.stock = p.stock - c
        p.save()        