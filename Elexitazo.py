"""
   @author Sebastian Montoya Rosario
   Fecha de creación: 8/08/2023
   Funcionalidad: Este programa pide los datos del usuario para un almacén, luego le pregunta cuantos
   productos desea comprar y le da el total de la compra.
"""
import json
import sys
import time
import datetime
import re
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Cargar los datos desde el archivo JSON
with open("Productos.json", "r") as json_file1:
    datos = json.load(json_file1)

with open("canasta_familiar.json", "r") as json_file2:
    canasta = json.load(json_file2)

with open("productos5%.json", "r") as json_file3:
    percente5 = json.load(json_file3)

with open("productos19%.json") as json_file4:
    percent19 = json.load(json_file4)

select_User = {}
listaproductos = []
user_canastafam = []
user_iva5 = []
user_iva19 = []
solic_datos = ["nombre completo: ", "edad: ",
               "número telefónico: ",
               "dirección de vivienda: ", "e-mail: ",
               "contraseña: "]
datos_User = []
nombres_User = []
global opcion_categoria
subcategoria_seleccionada_global = None
categoria_seleccionada_global = None
global opcion_producto
subtotal = int(0)
total = int(0)


def check_num(mensaje):
    """
    Esta función evalúa si los Strings contienen válores numéricos o no, si el string es de solo números arroja 'True',
    de lo contrario arroja 'False' para que una condición no se cumpla
    :param mensaje:
    """
    while True:
        try:
            valor = input(mensaje)
            valornum = int(valor)  # Intenta convertir el valor a un número entero
            return valornum  # Si no se produce una excepción, el valor es numérico
        except ValueError:
            print("Debes seleccionar una opción válida.")
            continue  # Si se produce una excepción, el valor no es numérico


def cadena_llena(mensaje):
    while True:
        usuario_input = input(mensaje)
        if usuario_input:
            break
        else:
            print("No has ingresado ningún dato. Por favor, intenta de nuevo.")
    return usuario_input


def check_mail(mensaje):
    patron_correo = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    while True:
        correo = input(mensaje)
        if re.match(patron_correo, correo):
            print("E-mail válido.")
            return correo
        else:
            print("Debes escribir una dirección de correo electrónico válida.")
            continue


def check_edad(mensaje):
    for i in range(4):
        edad = check_num(mensaje)
        if edad <= 17 or edad >= 100:
            print("Debes ser mayor de edad para acceder.")
        else:
            return edad
        if i == 3:
            print("""Has intentado muchas veces acceder siendo menor de edad, acceso denegado.
            Programa creado por: Sebastian Montoya Rosario.""")


def borrar_compra():
    print("Vaciando el carrito de compras.")
    listaproductos.clear()


def recopilar_Datos():
    """
        Esta función lee la información del usuario y la guarda en la lista 'datos_user[]'
        :return lista datos_User:
    """
    nombre = cadena_llena(solic_datos[0])
    datos_User.extend(nombre.split())
    for i in range(len(solic_datos) - 1, 0, -1):
        if i == 5:
            datos_User.append(check_edad(f"Escriba su {solic_datos[len(solic_datos) - i]}"))
        elif i == 6 or i == 4:
            datos_User.append(check_num(f"Escriba su {solic_datos[len(solic_datos) - i]}"))
        elif i == 2:
            datos_User.append(check_mail(f"Escriba su {solic_datos[len(solic_datos) - i]}"))
        elif i == 7:
            datos_User.append(f"Cree una {solic_datos[len(solic_datos) - i]}")
        else:
            datos_User.append(cadena_llena(f"Escriba su {solic_datos[len(solic_datos) - i]}"))
    editar_Datos()


def es_fecha_valida(dia, mes, año):
    try:
        fecha = datetime
        return True
    except ValueError:
        return False


def leer_fecha(mensaje):
    while True:
        fecha_str = input(mensaje)
        try:
            dia, mes, año = map(int, fecha_str.split('/'))
            if es_fecha_valida(dia, mes, año):
                return datetime
            else:
                print("Fecha no válida. Intente de nuevo.")
        except ValueError:
            print("Formato de fecha incorrecto. Use dd/mm/yyyy")


def editar_Datos():
    """
        En esta función el usuario podrá editar la información de su cuenta
        :return datos_User:
    """
    print(f"Longitud de lista dato user: {len(datos_User)}")
    while True:
        print("Confirme sus datos: ")
        if len(datos_User) == 8:
            for i in range(len(solic_datos) - 1, 0, -1):
                if i == 5:
                    print(
                        f"""Primer nombre: {datos_User[len(datos_User) - 8]} 
Primer apellido: {datos_User[len(datos_User) - 7]}
Segundo apellido: {datos_User[len(datos_User) - 6]}""")
                else:
                    print(f"""{solic_datos[len(solic_datos) - i]} {datos_User[len(datos_User) - i]}""")
        else:
            for i in range(len(solic_datos) - 1, 0, -1):
                if i == 5:
                    print(
                        f"""Primer nombre: {datos_User[len(datos_User) - 9]} 
Segundo nombre: {datos_User[len(datos_User) - 8]} 
Primer apellido: {datos_User[len(datos_User) - 7]}
Segundo apellido: {datos_User[len(datos_User) - 6]}""")
                else:
                    print(f"{solic_datos[len(solic_datos) - i]} {datos_User[len(datos_User) - i]}")
        opc_editar = check_num("Escribe 1 para editar algún dato ó 2 para confirmar los datos: ")
        if opc_editar == 1:
            print("1. Editar nombre\n2. Editar numero de documento\n3. Editar edad\n4. Editar numero de teléfono\n5. "
                  "Editar dirección\n6. Editar E-mail\n7. Editar contraseña\n8. Volvér atrás")
            opc_editar = check_num("Elige una opción: ")
        if opc_editar == 1:
            if len(datos_User) == 9:
                print("""1. Editar primer nombre.
2. Editar primer apellido.
3. Editar segundo apellido.""")
                opc_editar = check_num("Elige una opción para editar un dato: ")
                if opc_editar == 1:
                    datos_User[0] = input("Escribe tu primer nombre: ")
                    continue
                elif opc_editar == 2:
                    datos_User[1] = input("Escribe tu primer apellido: ")
                    continue
                elif opc_editar == 3:
                    datos_User[2] = input("Escribe tu segundo apellido: ")
                    continue
            elif len(datos_User) == 10:
                print("""1. Editar primer nombre.
2. Editar segundo nombre.
3. Editar primer apellido.
4. Editar segundo nombre.""")
                opc_editar = check_num("Elige una opción para editar un dato: ")
                if opc_editar == 1:
                    datos_User[0] = input("Escribe tu primer nombre: ")
                    continue
                elif opc_editar == 2:
                    datos_User[1] = input("Escribe tu segundo nombre: ")
                    continue
                elif opc_editar == 3:
                    datos_User[2] = input("Escribe tu primer apellido: ")
                    continue
                elif opc_editar == 4:
                    datos_User[3] = input("Escribe tu segundo apellido: ")
                    continue
            elif opc_editar == 2:
                datos_User.insert(len(datos_User) - 6, input(solic_datos[1]))
                continue
            elif opc_editar == 3:
                datos_User.insert(len(datos_User) - 5, input(solic_datos[2]))
                continue
            elif opc_editar == 4:
                datos_User.insert(len(datos_User) - 4, input(solic_datos[3]))
                continue
            elif opc_editar == 5:
                datos_User.insert(len(datos_User) - 3, input(solic_datos[4]))
                continue
            elif opc_editar == 6:
                datos_User.insert(len(datos_User) - 2, input(solic_datos[5]))
                continue
            elif opc_editar == 7:
                datos_User.insert(len(datos_User) - 1, input(solic_datos[6]))
                continue
        elif opc_editar == 2:
            print("Datos confírmados.")
            break

        else:
            print("Numero de opción incorrecta.")
            continue


def iniciar_Sesion():
    """
        Esta función válida los datos del usuario para poder ingresar al exitazo
    """
    if len(datos_User) == 0:
        print("Aún no tienes una cuenta. \nRedireccionando al regístro de datos.")
        recopilar_Datos()
    else:
        while True:
            confirmar_mail = input("Escribe tu correo Electrónico: ")
            confirmar_password = input("Escribe la contraseña: ")
            if confirmar_mail == datos_User[len(datos_User) - 2] and confirmar_password == datos_User[
                len(datos_User) - 1]:
                print("Inicio de sesión exitoso...")
                break
            else:
                print("Los datos no coinciden.")
                continue


def mostrar_categoria(datos):
    """
        Al llamar esta función se muestran las categorias creadas en el archivo JSON
        :param datos:
    """
    # Mostrar categorías y permitir al usuario elegir una
    print("Categorías disponibles:")
    categorias = datos["categorias"]

    for i, categoria in enumerate(categorias, start=1):
        print(f"{i}. {categoria['nombre']}")
    print("9. Salir")

    while True:
        categoria_seleccionada = check_num("Elige una categoria: ")
        if categoria_seleccionada <= 8:
            categoria_seleccionada = categorias[categoria_seleccionada - 1]
            return categoria_seleccionada
        elif categoria_seleccionada == 9:
            main()
        else:
            print("Debes seleccionar una opción válida.")
            continue


def mostrar_subcategorias(categoria_seleccionada):
    """
    Esta función al ser llamada muestra las subcategorias según la categoria que selecciono el usuario
    :param categoria_seleccionada:
    """
    global categoria_seleccionada_global
    if categoria_seleccionada is None:
        if categoria_seleccionada_global is None:
            print("No se ha seleccionado una subcategoría.")
            return
        else:
            categoria_seleccionada = categoria_seleccionada_global
    else:
        # Si se proporciona una subcategoría, actualizamos la variable global.
        categoria_seleccionada_global = categoria_seleccionada
    # Mostrar subcategorías dentro de la categoría seleccionada
    subcategorias = categoria_seleccionada["subcategorias"]
    print("Subcategorías disponibles:")

    for i, subcategoria in enumerate(subcategorias, start=1):
        print(f"{i}. {subcategoria['nombre']}")
    print("5. Ir al carrito\n6. Volver atrás\n7. Salir")
    while True:
        subcategoria_seleccionada = check_num("Elige una subcategoria: ")
        if 1 <= subcategoria_seleccionada <= len(subcategorias):
            subcategoria_seleccionada = subcategorias[subcategoria_seleccionada - 1]
            return subcategoria_seleccionada
        elif subcategoria_seleccionada == 5:
            mostrar_carrito()
        elif subcategoria_seleccionada == 6:
            categoria_seleccionada = mostrar_categoria(datos)
            subcategoria_seleccionada = mostrar_subcategorias(categoria_seleccionada)
            mostrar_productos(subcategoria_seleccionada, categoria_seleccionada)
            break
        elif subcategoria_seleccionada == 7:
            main()
            break
        else:
            print("Debes seleccionar una opción válida.")
            continue


def mostrar_productos(subcategoria_seleccionada, categoria_seleccionada):
    """
    Esta función al ser llamada muestra los productos según la categoría que seleccionó el usuario
    :param subcategoria_seleccionada:
    :param categoria_seleccionada:
    """
    global subcategoria_seleccionada_global, categoria_seleccionada_global
    # Si subcategoria_seleccionada es None, significa que no se proporcionó una subcategoría en esta llamada.
    # En ese caso, usamos la subcategoría previamente seleccionada.
    if subcategoria_seleccionada is None:
        if subcategoria_seleccionada_global is None:
            print("No se ha seleccionado una subcategoría.")
            return
        else:
            subcategoria_seleccionada = subcategoria_seleccionada_global
    else:
        # Si se proporciona una subcategoría, actualizamos la variable global.
        subcategoria_seleccionada_global = subcategoria_seleccionada

    # Imprimir la subcategoría seleccionada
    print(f"Productos de {subcategoria_seleccionada['nombre']}:")
    productos = subcategoria_seleccionada['Productos']

    for i, producto in enumerate(productos, start=1):
        print(f"{i}. {producto['nombre']} - {producto['descripcion']} - ${producto['precio']}")

    print("7. Volver atrás\n8. Volver a mostrar las categorias\n9. Salir")
    comprar_productos(subcategoria_seleccionada, categoria_seleccionada)


def comprar_productos(subcategoria_seleccionada, categoria_seleccionada):
    global listaproductos

    while True:
        opcion_producto = check_num("Elige el producto que quieres comprar: ")
        if opcion_producto < 7:
            # Camino que tomara el programa cuando el usuario compre un producto
            producto_seleccionado = subcategoria_seleccionada['Productos'][opcion_producto - 1]
            print(
                f"Has seleccionado: {producto_seleccionado['nombre']} - {producto_seleccionado['descripcion']} - ${producto_seleccionado['precio']}")
            opcion_select = check_num("""1. Añadir al carrito y volver atrás
2. Añadir y ver mi carrito de compras
3. Volver atrás
Selecciona una opción: """)
            if opcion_select == 1 or opcion_select == 2:
                cantidad_producto = check_num("¿Cuantos items de este producto deseas?: ")

                # Crear un nuevo diccionario para el producto seleccionado
                select_User = {
                    "Nombre: ": producto_seleccionado['nombre'],
                    "Precio Unitario: ": producto_seleccionado['precio'],
                    "Precio total: ": cantidad_producto * producto_seleccionado['precio']
                }

                # Agregar select_User a la lista de productos
                listaproductos.append(select_User)

                if opcion_select == 1:
                    mostrar_productos(subcategoria_seleccionada, categoria_seleccionada)
                elif opcion_select == 2:
                    mostrar_carrito()
                break
            elif opcion_select == 3:
                mostrar_productos(subcategoria_seleccionada, categoria_seleccionada)
                break
        elif opcion_producto == 7:
            subcategoria_seleccionada = mostrar_subcategorias(categoria_seleccionada)
            mostrar_productos(subcategoria_seleccionada, categoria_seleccionada)
            break
        elif opcion_producto == 8:
            categoria_seleccionada = mostrar_categoria(datos)
            subcategoria_seleccionada = mostrar_subcategorias(categoria_seleccionada)
            mostrar_productos(subcategoria_seleccionada, categoria_seleccionada)
            break
        elif opcion_producto == 9:
            main()
            break
        else:
            print("Elige una opción válida.")
            continue


def mostrar_carrito():
    """
        En esta función se muestran todos los productos que el usuario ha seleccionado para comprar,
        luego de mostrárselas le da la opcion de seguir comprando, ir al sistema de pago o eliminar algun producto, cada
        opción lo llevará a la función correspondiente.
    """
    print("Carrito de compras:")
    if len(listaproductos) == 0:
        print("Carrito de compras vacío, debes comprar productos. Redireccionando las categorias...")
        time.sleep(1)
        mostrar_categoria(datos)
    else:
        print("Índice  Producto  Precio Unitario  Precio Total")
        k = 0
        for i, producto in enumerate(listaproductos, 1):
            k += 1
            print(
                f"{i}. {producto['Nombre: ']} - Precio: {producto['Precio Unitario: ']} - Precio Total: {producto['Precio total: ']}")
        while True:
            print("\n1. Seguir comprando.\n2. Pagar ahora.\n3. Eliminar algún producto.\n4. Vaciar carrito.")
            opcion = check_num("Elige una opción: ")
            if opcion == 1:
                mostrar_productos(subcategoria_seleccionada_global, categoria_seleccionada_global)
                break
            elif opcion == 2:
                print("Ingresando a la sección de pago... ")
                time.sleep(1)
                pago_User()
                break
            elif opcion == 3:
                eliminar_producto(subcategoria_seleccionada_global, categoria_seleccionada_global)
                break
            elif opcion == 4:
                print("""Perderás todos tus productos seleccionado, ¿estás seguro de vaciar el carrito de compras?
                                \n1. Si\n2. No""")
                opcion = check_num("Elige una opción: ")
                if opcion == 1:
                    borrar_compra()
                    print("Carrito vacío. Volviendo a la sección principal...")
                    time.sleep(0.5)
                    menu(datos)
                    break
                else:
                    continue
            else:
                print("Debes seleccionar una opción válida.")


def generar_factura(datos_User, listaproductos):
    # Crear un archivo PDF para la factura
    c = canvas.Canvas("factura.pdf", pagesize=letter)

    # Configurar el tamaño y la posición de la factura
    ancho_pagina, alto_pagina = letter
    margen = 50
    ancho_factura = ancho_pagina - 2 * margen
    alto_factura = alto_pagina - 2 * margen
    c.translate(margen, margen)

    # Detalles de los usuarios
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, alto_factura - 50, "Información de Usuarios:")

    # Mostrar los detalles de usuarios
    c.setFont("Helvetica", 12)
    y = alto_factura - 70
    for usuario in range(len(solic_datos) - 1):
        if usuario == 0:
            c.drawString(100, y, f"s{datos_User[0]} {datos_User[1]} {datos_User[2]}")
            continue
        if usuario == 5:
            break
        c.drawString(100, y,
                     f"{solic_datos[usuario]} {datos_User[len(datos_User) - usuario - 1]}")

        y -= 20

    # Detalles de los productos
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, y - 30, "Productos:")

    # Mostrar los detalles de productos
    c.setFont("Helvetica", 12)
    y -= 50
    c.drawString(50, y, "Nombre producto    Precio unitario    Precio total")
    for producto in listaproductos:
        c.drawString(100, y, f"{producto['Nombre: ']} ${producto['Precio Unitario: ']}  ${producto['Precio total: ']}")
        y += 10

    # Guardar el PDF y cerrar el archivo
    c.save()


def eliminar_producto(subcategoria, categoria):
    """
        En esta función el usuario puede eliminar un producto que ya haya seleccionado
    :param subcategoria:
    :param categoria:
    :return opcion:
    """
    k = 0
    while True:
        # Muestra los productos que el cliente seleccionó principalmente
        for i, producto in enumerate(listaproductos, 1):
            print(
                f"{i}. {producto['Nombre: ']} - Precio: {producto['Precio Unitario: ']} - Precio Total: {producto['Precio total: ']}")

        # Pedir al usuario que seleccione un número
        numero_seleccionado = check_num("Seleccione el número del producto que desea eliminar: ")

        # Verificar si el número seleccionado es válido
        if 1 <= numero_seleccionado <= len(listaproductos):
            # Eliminar el producto seleccionado de la lista
            producto_eliminado = listaproductos.pop(numero_seleccionado - 1)
            print(f"Se ha eliminado el producto {producto_eliminado['Nombre: ']} de la lista.")

        elif numero_seleccionado < 1:
            print("Número no válido. No se ha eliminado ningún producto.")
        print("1. Eliminar más productos.\n2. Ver mis productos.\n3. Pagar ahora.")
        opcion = check_num("Elige una opción: ")
        if opcion == 1:
            continue
        elif opcion == 2:
            mostrar_carrito()
            break
        elif opcion == 3:
            pago_User()
            break
        else:
            print("Debes elegir una opción válida.")
            continue
    return opcion


def pago_User():
    """
    Esta función muestra la factura al usuario
    """
    global listaproductos
    if len(listaproductos) == 0:
        print("No hay productos que comprar... volviendo a la sección de compras")
        time.sleep(1)
        mostrar_productos(subcategoria_seleccionada_global, categoria_seleccionada_global)


    else:
        for producto in listaproductos:
            nombre_producto = producto['Nombre: ']
            precio_total = producto['Precio total: ']
            if nombre_producto in canasta:
                user_canastafam.append(precio_total)
                print(f"cambio exitoso a la canasta familiar. {user_canastafam}")
            elif nombre_producto in percente5:
                user_iva5.append(precio_total)
                print(f"cambio exitoso al porcentaje del 5%. {user_iva5}")
            elif nombre_producto in percent19:
                user_iva19.append(precio_total)
                print(f"Cambio exitoso a la categoria del 19%. {user_iva19}")
            else:
                print("producto no encontrado.")
        print("calculando tu pago...")
        mostrar_Factura()


def mostrar_Factura():
    subtotal_canasta, total_canasta = calcular_pago(1, user_canastafam)
    subtotal_5, total_5 = calcular_pago(0.05, user_iva5)
    subtotal_19, total_19 = calcular_pago(0.19, user_iva19)
    subtotal = subtotal_19 + subtotal_5 + subtotal_canasta
    total = total_19 + total_5 + total_canasta
    print("\n----- Factura de Compra -----\n")

    # Mostrar productos comprados por el usuario
    print("Productos comprados:")
    for i, producto in enumerate(listaproductos, start=1):
        nombre_producto = producto['Nombre: ']
        precio_unitario = producto['Precio Unitario: ']
        precio_total = producto['Precio total: ']

        print(f"{i}. {nombre_producto} - Precio unitario: {precio_unitario} - Precio total: {precio_total}")

    # Mostrar subtotales y totales
    print("\nResumen de Compra:")
    print(f"Subtotal (sin cambios en de IVA): {subtotal}")
    print(f"Total (sujeto a IVA): {total}")
    while True:
        print("1. Efectuar compra.\n2. Comprar más productos.\n3. Eliminar algún producto.\n4. Vaciar carrito.")
        opcion = check_num("Elige una opción: ")
        if opcion == 1:
            print("Ingresando a los medios de pago...")
            # Función que permite al usuario pagar su compra.
            pasarela_pago()
            break
        elif opcion == 2:
            menu(datos)
            break
        elif opcion == 3:
            eliminar_producto(subcategoria_seleccionada_global, categoria_seleccionada_global)
            break
        elif opcion == 4:
            print("""Perderás todos tus productos seleccionado, ¿estás seguro de vaciar el carrito de compras?
                \n1. Si\n2. No""")
            opcion = check_num("Elige una opción: ")
            if opcion == 1:
                borrar_compra()
                print("Carrito vacío. Volviendo a la sección principal.")
                menu(datos)
                break
            elif opcion == 2:
                continue
            else:
                print("Debes elegir una opción válida.")
                continue
        else:
            print("Debes elegir una opción válida.")
            continue


def pasarela_pago():
    if len(datos_User) == 0:
        print("No te has regístrado aún, redireccionando al log-in...")
        time.sleep(1)
        recopilar_Datos()
    print("1. Pago contra-entrega\n2. Pago con tarjeta débito\n3. Pago con tarjeta crédito\n4. Pago con PSE")
    opcion = check_num("Elige la opción con la que desees pagar: ")
    if opcion == 1:
        print("Has seleccionado con pago contra-entrega...")
        editar_Datos()
        generar_factura(datos_User, listaproductos)
        menu(datos)
    elif opcion == 2 or opcion == 3:
        global pago
        if opcion == 2:
            pago = "tarjeta débito"
        elif opcion == 3:
            pago = "tarjeta crédito"
        print(f"Has seleccionado pago con {pago}...")
        numero_tarjeta = check_num("Escribe tu número de tarjeta: ")
        fecha_vencimiento = leer_fecha("Escribe la fecha de vencimiento (dd/mm/yy): ")
        CVV = check_num("Escribe el código de seguridad de la tarjeta: ")
        nombre_titular = input("Escribe el nombre del titular: ")
        print("Datos personales.")
        editar_Datos()
        print("1. Confirmar datos y generar factura\n2. Cancelar compra")
        opc = check_num("Elige un opción: ")
        if opc == 1:
            print("Generando factura en formato pdf...")
            generar_factura(datos_User, listaproductos)
            time.sleep(1)
            print("compra realizada.\n volviendo al menu principal...")
            main()
        elif opc == 2:
            print("Cancelando compra...")
            time.sleep(1)
    elif opcion == 4:
        print("Has seleccionado pago por PSE...")
        nombre_banco = input("Escribe el nombre del banco: ")
        numero_cuenta = check_num("Escribe tu número de cuenta: ")
        print("1. Cuenta de ahorro\n2. Cuenta corriente")
        tipo_cuenta = check_num("Elige una opción de tipo de cuenta: ")
        print("1. Cédula de ciudadanía\n2. NIT")
        tipo_documento = check_num("Elige una opción: ")
        documento = check_num("Escribe tu numero de documento: ")
        print("Datos personales.")
        editar_Datos()
        print("1. Confirmar datos y generar factura\n2. Cancelar compra")
        opc = check_num("Elige un opción: ")
        if opc == 1:
            print("Generando factura en formato pdf...")
            generar_factura(datos_User, listaproductos)
            time.sleep(1)
            menu(datos)
        elif opc == 2:
            print("Cancelando compra...")
            time.sleep(1)


def calcular_pago(iva, lista):
    """
    Esta función calcula el pago del usuario con y sin IVA, con los productos correspondientes a la canasta familiar,
    Productos con el aumento del 5% y el 19%
    :param iva: Tasa de IVA (porcentaje)
    :param lista: Lista de precios de productos
    :return: Subtotal y total con IVA (excepto para la canasta familiar)
    """
    if lista is user_canastafam:
        # La lista de la canasta familiar no tiene IVA
        subtotal = sum(lista)
        total = subtotal
    else:
        subtotal = sum(lista)
        percent_iva = subtotal * iva
        total = subtotal + percent_iva
    return subtotal, total


def menu(datos):
    """
        Con esta función se puede mostrar el menú principal del programa, desde aqui el usuario puede realizar y acceder a
        las funciones principales del programa (inicio de sesión, regístro, Comprar, salir del programa).
        :param datos:
    """
    print("1. Iniciar sesión.\n2. Regístrarte.\n3. Ir a la tienda.\n4. salir del programa ")
    while True:
        opcion_menu = check_num("Ingresa una opción según la acción que quieras realizar: ")

        if opcion_menu == 1:
            print("Ingresando al inicio de sesión...")
            time.sleep(1)
            iniciar_Sesion()
            categoria_seleccionada = mostrar_categoria(datos)
            subcategoria_seleccionada = mostrar_subcategorias(categoria_seleccionada)
            mostrar_productos(subcategoria_seleccionada, categoria_seleccionada)
            break
        elif opcion_menu == 2:
            print("Ingresando al registro de datos...")
            time.sleep(1)
            recopilar_Datos()
            iniciar_Sesion()
            categoria_seleccionada = mostrar_categoria(datos)
            subcategoria_seleccionada = mostrar_subcategorias(categoria_seleccionada)
            mostrar_productos(subcategoria_seleccionada, categoria_seleccionada)
            break
        elif opcion_menu == 3:
            print("Ingresando a la tienda el exitazo...")
            time.sleep(1)
            categoria_seleccionada = mostrar_categoria(datos)
            subcategoria_seleccionada = mostrar_subcategorias(categoria_seleccionada)
            mostrar_productos(subcategoria_seleccionada, categoria_seleccionada)
            break
        elif opcion_menu == 4:
            if len(listaproductos) > 0:
                while True:
                    opcion_menu = check_num(
                        "!Tu carrito esta lleno, si sales perderás tus compras.\n¿Estas seguro de que quieres salir?\n1. Ir al carrito\n2. Seguir comprando\n3. Salir")
                    if opcion_menu == 1:
                        mostrar_carrito()
                        break
                    elif opcion_menu == 2:
                        categoria_Seleccionada = mostrar_categoria(datos)
                        subcategoria_seleccionada = mostrar_subcategorias(categoria_Seleccionada)
                        mostrar_productos(subcategoria_seleccionada, categoria_Seleccionada)
                        break
                    elif opcion_menu == 3:
                        print("Has salido del exitazo, espero que vuelvas pronto.\nCreador: Sebastian Montoya Rosario")
                        sys.exit()
                break
            else:
                print("Has salido del exitazo, espero que vuelvas pronto.\nCreador: Sebastian Montoya Rosario")
                break
        else:
            continue


def main():
    """Contextualizamos al usuario sobre la función del programa."""
    print("""           Bienvenido a almacenes el exitázo.
       \n    Este programa va a requerir de tus datos personales y también
                 la información de los productos que deseas comprar.
       \n     Al final te dirá el total de lo que debes pagar.""")
    time.sleep(1)
    menu(datos)


# Llama a la función principal
if __name__ == "__main__":
    main()
