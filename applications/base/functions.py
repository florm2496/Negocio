from django.db.models import Q,Count



def estado_clientes(cuentas,clientes):
    clientes_aldia=[]
    clientes_morosos=[]

    for cliente in clientes:

        nombre_cliente=f'{cliente.nombre} {cliente.apellido}'

        cuentas_aldia=cuentas.filter(Q(estado='activa') & Q(estado='pagada') and Q(solicitante__id=cliente.id)).aggregate(cantidad=Count('id'))

        cuentas_totales=cuentas.filter(solicitante__id=cliente.id).aggregate(cantidad=Count('id'))

        if cuentas_totales['cantidad'] != 0 :
        
            if cuentas_totales['cantidad'] == cuentas_aldia['cantidad']:

                clientes_aldia.append(nombre_cliente)
            else:

                clientes_morosos.append(nombre_cliente)

    return clientes_aldia,clientes_morosos