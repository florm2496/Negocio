def actualizar_stock(productos,cantidades,señal):
    
    for p,c in zip(productos,cantidades):
        if señal=='ventas':
            p.stock = p.stock - c
            p.save()  

        elif señal=='ingresos':
            p.stock = p.stock + c
            p.save()  
