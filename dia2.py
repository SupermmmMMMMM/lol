import tkinter as tk
from tkinter import messagebox, ttk
import json
from cryptography.fernet import Fernet
import pyautogui
import time
import base64

# Generar la clave para encriptación
def generar_clave():
    clave = Fernet.generate_key()
    with open('clave.key', 'wb') as file:
        file.write(clave)

# Obtener la clave de encriptación
def obtener_clave():
    with open('clave.key', 'rb') as file:
        return file.read()
    

# Guardar las cuentas en un archivo JSON
def guardar_credenciales():
    clave = obtener_clave()
    fernet = Fernet(clave)

    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()

    # Encriptar las credenciales
    usuario_encriptado = fernet.encrypt(usuario.encode())
    contrasena_encriptada = fernet.encrypt(contrasena.encode())

    # Convertir los bytes en base64 (cadena de texto)
    usuario_encriptado_base64 = base64.b64encode(usuario_encriptado).decode('utf-8')
    contrasena_encriptada_base64 = base64.b64encode(contrasena_encriptada).decode('utf-8')

    # Guardar las credenciales en el archivo JSON
    try:
        with open('cuentas.json', 'r') as file:
            cuentas = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        cuentas = {}

    # Agregar la nueva cuenta
    cuentas[usuario] = {'usuario': usuario_encriptado_base64, 'contrasena': contrasena_encriptada_base64}

    # Guardar el archivo actualizado
    with open('cuentas.json', 'w') as file:
        json.dump(cuentas, file)

    messagebox.showinfo("Éxito", "Cuenta guardada con éxito.")
    mostrar_opciones()  # Actualizar la interfaz después de guardar

# Iniciar sesión con la cuenta seleccionada
def iniciar_sesion():
    cuenta_seleccionada = combo_cuentas.get()
    juego_seleccionado = combo_juegos.get()  # Obtener el juego seleccionado

    if cuenta_seleccionada == "" or juego_seleccionado == "":
        messagebox.showerror("Error", "Por favor, selecciona una cuenta y un juego.")
        return

    try:
        # Obtener las credenciales guardadas
        with open('cuentas.json', 'r') as file:
            cuentas = json.load(file)

        cuenta = cuentas[cuenta_seleccionada]
        clave = obtener_clave()
        fernet = Fernet(clave)

        # Convertir las credenciales de base64 a bytes y desencriptarlas
        usuario_encriptado = base64.b64decode(cuenta['usuario'].encode('utf-8'))
        contrasena_encriptada = base64.b64decode(cuenta['contrasena'].encode('utf-8'))

        usuario = fernet.decrypt(usuario_encriptado).decode()
        contrasena = fernet.decrypt(contrasena_encriptada).decode()

        # Automatizar la apertura del cliente dependiendo del juego seleccionado
        if juego_seleccionado == "League of Legends":
            pyautogui.hotkey('win', 'r')  # Abre la ventana de ejecutar
            pyautogui.write("C:/Users/Public/Desktop/League of Legends.lnk")  # Ruta del cliente LoL
        elif juego_seleccionado == "Valorant":
            pyautogui.hotkey('win', 'r')  # Abre la ventana de ejecutar
            pyautogui.write("C:/Users/Public/Desktop/VALORANT.lnk")  # Ruta del cliente Valorant

        pyautogui.press('enter')

        time.sleep(6)  # Esperar a que el cliente se inicie

        # Escribir las credenciales en el cliente
        pyautogui.write(usuario)
        pyautogui.press('tab')
        pyautogui.write(contrasena)
        pyautogui.press('enter')

       

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

# Eliminar la cuenta seleccionada
def eliminar_cuenta():
    cuenta_seleccionada = combo_cuentas.get()

    if cuenta_seleccionada == "":
        messagebox.showerror("Error", "Por favor, selecciona una cuenta para eliminar.")
        return

    try:
        # Obtener las cuentas guardadas
        with open('cuentas.json', 'r') as file:
            cuentas = json.load(file)

        if cuenta_seleccionada in cuentas:
            # Eliminar la cuenta seleccionada
            del cuentas[cuenta_seleccionada]

            # Guardar el archivo actualizado
            with open('cuentas.json', 'w') as file:
                json.dump(cuentas, file)

            messagebox.showinfo("Éxito", "Cuenta eliminada con éxito.")
            mostrar_opciones()  # Actualizar la interfaz después de eliminar
        else:
            messagebox.showerror("Error", "La cuenta seleccionada no existe.")
    
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

# Limpiar campos para agregar una nueva cuenta
def limpiar_campos():
    entry_usuario.delete(0, tk.END)
    entry_contrasena.delete(0, tk.END)

# Mostrar el menú de opciones
def mostrar_opciones():
    # Limpiar la ventana actual
    for widget in root.winfo_children():
        widget.grid_forget()

    # Mostrar siempre el formulario de nueva cuenta
    tk.Label(root, text="Usuario:").grid(row=0, column=0)
    global entry_usuario
    entry_usuario = tk.Entry(root)
    entry_usuario.grid(row=0, column=1)

    tk.Label(root, text="Contraseña:").grid(row=1, column=0)
    global entry_contrasena
    entry_contrasena = tk.Entry(root, show="*")
    entry_contrasena.grid(row=1, column=1)

    # Botón para guardar cuenta
    tk.Button(root, text="Guardar Cuenta", command=guardar_credenciales).grid(row=2, column=0, columnspan=2)

    # Intentar cargar las cuentas guardadas
    try:
        with open('cuentas.json', 'r') as file:
            cuentas = json.load(file)
            cuentas_guardadas = list(cuentas.keys())
    except (FileNotFoundError, json.JSONDecodeError):
        cuentas_guardadas = []

    if cuentas_guardadas:
        # Si hay cuentas guardadas, mostrar la opción para iniciar sesión
        tk.Label(root, text="Selecciona una cuenta para iniciar sesión:").grid(row=3, column=0, columnspan=2)
        global combo_cuentas
        combo_cuentas = ttk.Combobox(root, values=cuentas_guardadas, state="readonly")
        combo_cuentas.grid(row=4, column=0, columnspan=2)

        # Agregar un ComboBox para seleccionar el juego
        tk.Label(root, text="Selecciona un juego:").grid(row=5, column=0, columnspan=2)
        global combo_juegos
        combo_juegos = ttk.Combobox(root, values=["League of Legends", "Valorant"], state="readonly")
        combo_juegos.grid(row=6, column=0, columnspan=2)

        tk.Button(root, text="Iniciar Sesión", command=iniciar_sesion).grid(row=7, column=0, columnspan=2)

        # Agregar un botón para eliminar la cuenta
        tk.Button(root, text="Eliminar Cuenta", command=eliminar_cuenta).grid(row=8, column=0, columnspan=2)
    else:
        # Si no hay cuentas guardadas, no mostrar el botón de iniciar sesión
        pass

# Verificar si existe la clave, si no, generar una nueva
try:
    open('clave.key', 'rb')
except FileNotFoundError:
    generar_clave()

# Crear ventana principal
root = tk.Tk()
root.title("Gestor de Cuentas y Juegos")

# Mostrar las opciones dependiendo de si hay cuentas guardadas o no
mostrar_opciones()

# Ejecutar la aplicación
root.mainloop()
