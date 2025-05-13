import customtkinter as ctk
import sqlite3
import os
from tkinter import messagebox
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageOps

import mainSF

# Almacena el frame del panel derecho para reemplazar contenido dinámicamente
panel_derecho_contenedor = None


# Obtener conexión y trabajar con la base de datos
from dbController import get_connection, init_db
conn = get_connection()
cursor = conn.cursor()

# Funciones esteticas
def imagen_con_bordes_redondeados(imagen, radio=3):
    # Asegurar modo RGBA
    imagen = imagen.convert("RGBA")
    
    # Crear máscara redondeada
    mascara = Image.new("L", imagen.size, 0)
    draw = ImageDraw.Draw(mascara)
    draw.rounded_rectangle([(0, 0), imagen.size], radius=radio, fill=255)
    
    # Aplicar máscara
    imagen_redondeada = ImageOps.fit(imagen, imagen.size)
    imagen_redondeada.putalpha(mascara)
    return imagen_redondeada


def limpiar_panel_derecho():
    global panel_derecho_contenedor
    for widget in panel_derecho_contenedor.winfo_children():
        widget.destroy()



def mostrar_mensaje(mensaje):
    print(mensaje)  # Imprimir en consola



# Funciónes Principales

def crear_usuario():
    global panel_derecho_contenedor
    limpiar_panel_derecho()
    for widget in panel_derecho_contenedor.winfo_children():
        widget.destroy()

    ctk.CTkLabel(panel_derecho_contenedor, text="Crear nuevo usuario", font=("Arial", 18)).pack(pady=10)

    campos = ["usuario", "contraseña", "correo", "telefono", "relacion", "cumpleaños"]
    entradas = {}

    for campo in campos:
        lbl = ctk.CTkLabel(panel_derecho_contenedor, text=campo.capitalize())
        lbl.pack()
        entry = ctk.CTkEntry(panel_derecho_contenedor)
        entry.pack(pady=5)
        entradas[campo] = entry

    # Sección para imagen de perfil
    imagen_seleccionada = {"ruta": None}
    
    def seleccionar_imagen():
        archivo = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png *.jpg *.jpeg")])
        if archivo:
            imagen_seleccionada["ruta"] = archivo
            mostrar_mensaje("📷 Imagen seleccionada correctamente.")

    btn_imagen = ctk.CTkButton(panel_derecho_contenedor, text="Seleccionar imagen de perfil (opcional)", command=seleccionar_imagen)
    btn_imagen.pack(pady=10)

    # Etiqueta para mensajes de error
    mensaje_label = ctk.CTkLabel(panel_derecho_contenedor, text="", text_color="red")
    mensaje_label.pack()

    def guardar_usuario():
        mensaje_label.configure(text="")  # Limpiar mensaje previo
        datos = [entradas[c].get().strip() for c in campos]

        if not all(datos[:4]):
            mensaje_label.configure(text="⚠️ Completa todos los campos obligatorios.")
            return

        if not datos[4]:
            datos[4] = "sinrelacion"

        nombre_usuario = datos[0]

        # Verificar si el usuario ya existe
        cursor.execute("SELECT id FROM usuarios WHERE usuario = ?", (nombre_usuario,))
        if cursor.fetchone():
            mensaje_label.configure(text="❌ El nombre de usuario ya existe. Por favor escoge otro.")
            return

        try:
            cursor.execute("""
                INSERT INTO usuarios (usuario, contraseña, Correo, telefono, RelacionCon, cumpleaños)
                VALUES (?, ?, ?, ?, ?, ?)
            """, datos)
            conn.commit()
        except Exception as e:
            mensaje_label.configure(text=f"❌ Error en la base de datos: {e}")
            return

        # Crear carpeta y guardar imagen
        carpeta_usuario = os.path.join("users", nombre_usuario)
        os.makedirs(carpeta_usuario, exist_ok=True)
        ruta_destino = os.path.join(carpeta_usuario, "profile.png")

        try:
            if imagen_seleccionada["ruta"]:
                imagen = Image.open(imagen_seleccionada["ruta"])
            else:
                imagen = Image.open("defaultuser.png")
            imagen.save(ruta_destino)
        except Exception as e:
            mensaje_label.configure(text=f"⚠️ Error al guardar imagen: {e}")
            return

        mostrar_mensaje("✅ Usuario creado correctamente.")
        limpiar_panel_derecho()
        leer_usuarios()  # ✅ Actualizar tabla de usuarios
        editar_usuario(cursor.lastrowid)

    btn_guardar = ctk.CTkButton(panel_derecho_contenedor, text="💾 Guardar usuario", command=guardar_usuario)
    btn_guardar.pack(pady=20)





def eliminar_usuario_por_id(id_usuario):
    confirmar = messagebox.askyesno("Confirmar eliminación", "¿Estás seguro de que deseas eliminar este usuario?")
    if confirmar:
        cursor.execute("SELECT usuario FROM usuarios WHERE id = ?", (id_usuario,))
        resultado = cursor.fetchone()
        if resultado:
            nombre_usuario = resultado[0]
            carpeta_usuario = os.path.join("users", nombre_usuario)
            if os.path.exists(carpeta_usuario):
                try:
                    import shutil
                    shutil.rmtree(carpeta_usuario)  # Eliminar carpeta del usuario si existe
                except Exception as e:
                    print(f"Error eliminando carpeta: {e}")

        cursor.execute("DELETE FROM usuarios WHERE id = ?", (id_usuario,))
        conn.commit()
        mostrar_mensaje("🗑️ Usuario eliminado correctamente.")
        leer_usuarios()  # Refrescar la lista

def leer_usuarios():
    global panel_derecho_contenedor
    limpiar_panel_derecho()

    for widget in panel_derecho_contenedor.winfo_children():
        widget.destroy()

    cursor.execute("SELECT id, usuario, correo, telefono, RelacionCon FROM usuarios")

    usuarios = cursor.fetchall()

    if not usuarios:
        label_vacio = ctk.CTkLabel(panel_derecho_contenedor, text="⚠️ No hay usuarios registrados.", font=("Arial", 16))
        label_vacio.pack(pady=10)
        return

    scroll_frame = ctk.CTkScrollableFrame(panel_derecho_contenedor, width=400, height=600)
    scroll_frame.pack(expand=True, fill="both", padx=10, pady=10)

    for user in usuarios:
        id_usuario, nombre_usuario, correo, telefono, relacion = user
        ruta_imagen = os.path.join("users", nombre_usuario, "profile.png")
        
        if not relacion:
            relacion = "sinrelacion"

        if os.path.exists(ruta_imagen):
            original = Image.open(ruta_imagen).resize((80, 80))
        else:
            original = Image.new("RGB", (80, 80), color="gray")

        

        
        imagen_redondeada = imagen_con_bordes_redondeados(original, radio=9)
        img = ctk.CTkImage(imagen_redondeada, size=(80, 80))

        user_frame = ctk.CTkFrame(scroll_frame, corner_radius=10)
        user_frame.pack(fill="x", pady=5, padx=5)

        img_label = ctk.CTkLabel(user_frame, image=img, text="")
        img_label.image = img
        img_label.pack(side="left", padx=20)

        text_label = ctk.CTkLabel(user_frame, text=f"ID: {id_usuario}\n{nombre_usuario}\n{correo} | {telefono}\nRelación: {relacion}", anchor="center", justify="center")

        text_label.pack(side="left", padx=20)

        btn_frame = ctk.CTkFrame(user_frame)
        btn_frame.pack(side="right", padx=20)

        editar_btn = ctk.CTkButton(btn_frame, text="Editar", width=40, command=lambda uid=id_usuario: editar_usuario(uid))
        editar_btn.pack(pady=2)

        eliminar_btn = ctk.CTkButton(btn_frame, text="Eliminar", width=40, fg_color="red", hover_color="#b30000",
                                    command=lambda uid=id_usuario: eliminar_usuario_por_id(uid))
        eliminar_btn.pack(pady=2)



def eliminar_usuario():
    id_usuario = ctk.CTkInputDialog(text="ID del usuario a eliminar:", title="Eliminar Usuario").get_input()
    if not id_usuario:
        return
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id_usuario,))
    resultado = cursor.fetchone()
    if resultado:
        cursor.execute("DELETE FROM usuarios WHERE id = ?", (id_usuario,))
        conn.commit()
        mostrar_mensaje("🗑️ Usuario eliminado correctamente.")
    else:
        mostrar_mensaje("❌ No se encontró un usuario con ese ID.")


def editar_usuario(id_usuario):
    global panel_derecho_contenedor
    limpiar_panel_derecho()
    for widget in panel_derecho_contenedor.winfo_children():
        widget.destroy()

    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id_usuario,))
    usuario = cursor.fetchone()
    if not usuario:
        return

    campos = ["usuario", "contraseña", "Correo", "telefono", "RelacionCon", "cumpleaños"]
    valores = dict(zip(campos, usuario[1:]))

    # Imagen
    ruta_imagen = os.path.join("users", valores['usuario'], "profile.png")
    if os.path.exists(ruta_imagen):
        img = ctk.CTkImage(Image.open(ruta_imagen), size=(100, 100))
    else:
        img = ctk.CTkImage(Image.new("RGB", (100, 100), color="gray"), size=(100, 100))

    label_img = ctk.CTkLabel(panel_derecho_contenedor, image=img, text="")
    label_img.image = img
    label_img.pack(pady=10)

    entradas = {}
    for campo, valor in valores.items():
        lbl = ctk.CTkLabel(panel_derecho_contenedor, text=campo.capitalize())
        lbl.pack()
        entry = ctk.CTkEntry(panel_derecho_contenedor)
        entry.insert(0, valor)
        entry.pack(pady=5)
        entradas[campo] = entry

    def guardar_cambios():
        nuevo_usuario = entradas["usuario"].get()
        datos = [entradas[c].get() for c in campos]

        # Obtener nombre de usuario anterior
        nombre_anterior = valores["usuario"]

        if not entradas["RelacionCon"].get():
            entradas["RelacionCon"].delete(0, "end")
            entradas["RelacionCon"].insert(0, "sinrelacion")


        # Renombrar carpeta si el nombre ha cambiado
        if nuevo_usuario != nombre_anterior:
            carpeta_anterior = os.path.join("users", nombre_anterior)
            carpeta_nueva = os.path.join("users", nuevo_usuario)

            if os.path.exists(carpeta_anterior):
                try:
                    os.rename(carpeta_anterior, carpeta_nueva)
                except Exception as e:
                    mostrar_mensaje(f"⚠️ Error al renombrar la carpeta: {e}")
                    return

        # Actualizar en la base de datos
        cursor.execute("""
            UPDATE usuarios
            SET usuario=?, contraseña=?, Correo=?, telefono=?, RelacionCon=?, cumpleaños=?
            WHERE id=?
        """, (*datos, id_usuario))
        conn.commit()
        mostrar_mensaje("✅ Usuario actualizado.")

        # 🔄 Refrescar la vista del mismo usuario con nuevos datos
        editar_usuario(id_usuario)



    btn_guardar = ctk.CTkButton(panel_derecho_contenedor, text="💾 Guardar cambios", command=guardar_cambios)
    btn_guardar.pack(pady=10)


# Estilo de ventana principal de Administracion
def mostrar_ventana_Admin():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    global panel_derecho_contenedor

    ventana = ctk.CTk()
    ventana.geometry("1280x720")
    ventana.title("SUNFLOWER - Admin Panel")
    ventana.grid_columnconfigure(0, weight=1)
    ventana.grid_columnconfigure(1, weight=3)
    ventana.grid_rowconfigure(0, weight=1)

    # Panel izquierdo
    marco_izquierdo = ctk.CTkFrame(ventana, corner_radius=15)
    marco_izquierdo.grid(row=0, column=0, sticky="nswe", padx=20, pady=20)

    label_acciones = ctk.CTkLabel(marco_izquierdo, text="Acciones", font=ctk.CTkFont(size=20, weight="bold"))
    label_acciones.pack(pady=(20, 10))

    botones = [
        ("➕ Crear usuario", crear_usuario),
        ("📖 Leer usuarios", leer_usuarios),
        ("🗑️ Eliminar usuario", eliminar_usuario),
    ]
    for texto, comando in botones:
        btn = ctk.CTkButton(marco_izquierdo, text=texto, command=comando, width=200)
        btn.pack(pady=10)

    btn_cerrar_sesion = ctk.CTkButton(marco_izquierdo, text="🔓 Cerrar sesión", command=lambda: [ventana.destroy(), mainSF.login()], fg_color="red", hover_color="#b30000")
    btn_cerrar_sesion.pack(pady=20)

    #salida del comando label

    salidaComandoAdmin = ctk.CTkLabel(marco_izquierdo, text="Salida del comando", font=ctk.CTkFont(size=20, weight="bold"))
    salidaComandoAdmin.pack(pady=(20, 10))

    # Panel derecho
    panel_derecho_contenedor = ctk.CTkFrame(ventana, corner_radius=15)
    panel_derecho_contenedor.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
    leer_usuarios()

    ventana.mainloop()

