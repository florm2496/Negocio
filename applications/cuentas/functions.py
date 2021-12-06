import datetime as dt
import pytz
utc=pytz.UTC

from applications.cuentas.models import Cuentas,Cuotas

def update_dues(listacuentas):
    for c in listacuentas:
        cuotas = Cuotas.objects.filter(cuenta__numero_cuenta=c.numero_cuenta,vencida=False)
        cuotas_impagas=Cuotas.objects.filter(cuenta__numero_cuenta=c.numero_cuenta,estado='impaga')
        if cuotas_impagas.count() > 0:
             for cuota in cuotas:

                venc=cuota.fecha_vencimiento
                if venc <=  utc.localize(dt.datetime.now()):
                    cuota.vencida = True
                
                    """inicialmente , el saldo sera igual al importe de la cuota , cada vez que se efectue 
                    un pago se descontara del saldo, y si la cuota vence y no esta saldada se aplicara un 
                    recargo al saldo
                    
                    """
                    if cuota.estado == 'impaga':
                        cuota.recargo = cuota.saldo * 0.20
                        #i.saldo = i.saldo + i.recargo 
                    cuota.save()
        
        else:
            c.estado='pagada'
            c.save()


           

def get_cuentas(listacuentas,cuenta):
    update_dues(listacuentas)
    if cuenta is None:
        cuentas=Cuentas.objects.all()
    else:
        cuentas=Cuentas.objects.get(numero_cuenta=cuenta)
    return cuentas


def generar_fechas(fecha_venci,cuotas):
    fechas_venc=[]

    fecha_actual=fecha_venci
    #ahora=dt.datetime.today()
    for c in range(cuotas):

        if c!=0:
            mes=fecha_actual.month
            año=fecha_actual.year
            dia=fecha_actual.day
            
            if mes == 12:
                mes=1
                año=año+1
                fecha_actual=dt.datetime(año,mes,dia)
            else:
                mes=mes+1
                fecha_actual=dt.datetime(año,mes,dia)

        fechas_venc.append(fecha_actual)
        
        
        
        
    return fechas_venc

