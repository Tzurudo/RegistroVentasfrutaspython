import csv
import os
import curses
import time

ARCHIVO = 'almacen_frutas.csv'
CAMPOS = ['Nombre', 'Cantidad', 'Unidad', 'Fecha', 'Origen', 'Costo', 'Proveedor']

# Dibujo ASCII del logo
logo = [
    
    "███████    █████████    ██      ██  █████████  ████████  ██████     ██████",
    "███████    █████████    ██      ██  █████████  ████████     ████   ████",
    "██         ██      ██   ██      ██    █████    ██             ███ ███ ",
    "██████     █████████    ██      ██    █████    ███████          ███",
    "██         ██    ██     ██      ██    █████    ███████         █████",
    "██         ██     ██    ██      ██    █████    ██            ███   ███",
    "██         ██      ██    ████████     █████    ████████     ████     ████",
    "██         ██      ███   ████████     █████    ████████  ██████       ███████"
]

fruta_animada = [

[
    "   🍓   ",
    "   🍍   ",
    "   🍉   ",
    "   🍇   ",
    "   🍊   ",
    "   🍎   ",
    "   🍌   ",
],
[
    "   🍍   ",
    "   🍉   ",
    "   🍇   ",
    "   🍓   ",
    "   🍊   ",
    "   🍎   ",
    "   🍒   ",
],
[
    "   🍉   ",
    "   🍇   ",
    "   🍓   ",
    "   🍍   ",
    "   🍎   ",
    "   🍌   ",
    "   🍑   ",
],
[
    "   🍇   ",
    "   🍓   ",
    "   🍍   ",
    "   🍉   ",
    "   🍊   ",
    "   🍒   ",
    "   🍓   ",
]

    
]

# Funciones de almacenamiento
def cargar_datos():
    if not os.path.exists(ARCHIVO):
        return []
    with open(ARCHIVO, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def guardar_datos(datos):
    with open(ARCHIVO, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=CAMPOS)
        writer.writeheader()
        writer.writerows(datos)

def nuevo_registro():
    os.system('clear')
    datos = cargar_datos()
    nombre = input("Nombre de la fruta: ").strip()
    fruta_existente = next((f for f in datos if f['Nombre'].lower() == nombre.lower()), None)

    if fruta_existente:
        print("La fruta ya existe. Solo puedes actualizar cantidad, fecha y proveedor.")
        fruta_existente['Cantidad'] = input("Nueva cantidad: ").strip()
        fruta_existente['Fecha'] = input("Nueva fecha de ingreso (YYYY-MM-DD): ").strip()
        fruta_existente['Proveedor'] = input("Nuevo proveedor: ").strip()
    else:
        nueva = {
            'Nombre': nombre,
            'Cantidad': input("Cantidad de fruta: ").strip(),
            'Unidad': input("Unidades (kg, unidades, etc): ").strip(),
            'Fecha': input("Fecha de ingreso (YYYY-MM-DD): ").strip(),
            'Origen': input("Lugar de origen: ").strip(),
            'Costo': input("Costo: ").strip(),
            'Proveedor': input("Proveedor: ").strip()
        }
        datos.append(nueva)
        print("Fruta registrada exitosamente.")

    guardar_datos(datos)
    input("\nPresiona ENTER para volver al menú...")

def actualizar_registro():
    os.system('clear')
    datos = cargar_datos()
    nombre = input("Nombre de la fruta a actualizar: ").strip()
    fruta = next((f for f in datos if f['Nombre'].lower() == nombre.lower()), None)
    if fruta:
        print("Solo puedes actualizar: cantidad, fecha y proveedor.")
        fruta['Cantidad'] = input(f"Nueva cantidad (actual: {fruta['Cantidad']}): ").strip()
        fruta['Fecha'] = input(f"Nueva fecha (actual: {fruta['Fecha']}): ").strip()
        fruta['Proveedor'] = input(f"Nuevo proveedor (actual: {fruta['Proveedor']}): ").strip()
        guardar_datos(datos)
        print("Fruta actualizada.")
    else:
        print("Fruta no encontrada.")
    input("\nPresiona ENTER para volver al menú...")

def consultar_registros():
    os.system('clear')
    datos = cargar_datos()
    if not datos:
        print("No hay registros.")
    else:
        for fruta in datos:
            print("-" * 40)
            for campo in CAMPOS:
                print(f"{campo}: {fruta[campo]}")
        print("-" * 40)
    input("\nPresiona ENTER para volver al menú...")

def eliminar_producto():
    os.system('clear')
    datos = cargar_datos()
    nombre = input("Nombre de la fruta a eliminar: ").strip()
    nueva_lista = [f for f in datos if f['Nombre'].lower() != nombre.lower()]
    if len(nueva_lista) != len(datos):
        guardar_datos(nueva_lista)
        print("Fruta eliminada.")
    else:
        print("Fruta no encontrada.")
    input("\nPresiona ENTER para volver al menú...")

def menu_interactivo(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

    opciones = ['Nuevo registro', 'Actualizar registro', 'Consultar registros', 'Eliminar producto', 'Salir']
    seleccion = 0
    frame = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        # Mostrar logo
        for i, linea in enumerate(logo):
            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(i+1, 50, linea)
            stdscr.attroff(curses.color_pair(2))

        # Mostrar fruta animada a la derecha
        fruta = fruta_animada[frame % len(fruta_animada)]
        for j, linea in enumerate(fruta):
            stdscr.addstr(12 + j, w 
            -60, linea)
            stdscr.addstr(12 + j, 60, linea)

        # Mostrar menú
        for i, opcion in enumerate(opciones):
            x = w // 2 - len(opcion) // 2
            y = len(logo) + 5 + i
            if i == seleccion:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, opcion)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, opcion)

        stdscr.refresh()
        time.sleep(0.2)
        frame += 1

        stdscr.timeout(100)
        tecla = stdscr.getch()

        if tecla == curses.KEY_UP and seleccion > 0:
            seleccion -= 1
        elif tecla == curses.KEY_DOWN and seleccion < len(opciones) - 1:
            seleccion += 1
        elif tecla in [10, 13]:
            curses.endwin()
            if seleccion == 0:
                nuevo_registro()
            elif seleccion == 1:
                actualizar_registro()
            elif seleccion == 2:
                consultar_registros()
            elif seleccion == 3:
                eliminar_producto()
            elif seleccion == 4:
                break
            stdscr.clear()
            curses.curs_set(0)

if __name__ == '__main__':
    curses.wrapper(menu_interactivo)
