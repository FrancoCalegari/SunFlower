import customtkinter as ctk
import sqlite3
import os
from tkinter import messagebox

import mainSF


# Obtener conexión y trabajar con la base de datos
from dbController import get_connection, init_db
conn = get_connection()
cursor = conn.cursor()

# Funciones
def mostrar_mensaje(mensaje):
    textbox.delete("0.0", "end")
    textbox.insert("0.0", mensaje)

def crear_usuario():
    
    usuario = ctk.CTkInputDialog(text="Nombre de usuario:", title="Crear usuario").get_input()
    contraseña = ctk.CTkInputDialog(text="Ingrese la contraseña:", title="Ingresar contraseña").get_input()
    correo = ctk.CTkInputDialog(text="Ingrese su correo:", title="Correo").get_input()
    telefono = ctk.CTkInputDialog(text="Ingrese su teléfono:", title="Teléfono").get_input()
    relacion = ctk.CTkInputDialog(text="¿Con quién tiene una relación?", title="Relación").get_input()
    cumpleaños = ctk.CTkInputDialog(text="Ingresa tu cumpleaños:", title="Cumpleaños").get_input()

    if usuario and contraseña and correo and telefono and relacion and cumpleaños:
        cursor.execute("INSERT INTO usuarios (usuario, contraseña, Correo, telefono, RelacionCon, cumpleaños) VALUES (?, ?, ?, ?, ?, ?)",
                       (usuario, contraseña, correo, telefono, relacion, cumpleaños))
        conn.commit()
        mostrar_mensaje("✅ Tu usuario fue creado con éxito.")

def leer_usuarios():
    cursor.execute("SELECT id, usuario, contraseña, Correo, telefono, RelacionCon, cumpleaños FROM usuarios")
    usuarios = cursor.fetchall()
    if usuarios:
        mensaje = "📋 Lista de usuarios:\n\n"
        for user in usuarios:
            mensaje += f"ID: {user[0]} | Usuario: {user[1]} | Contraseña: {user[2]} | Correo: {user[3]} | Tel: {user[4]} | Relación: {user[5]} | Cumpleaños: {user[6]}\n"
    else:
        mensaje = "⚠️ No hay usuarios registrados."
    mostrar_mensaje(mensaje)

def actualizar_usuario():
    id_usuario = ctk.CTkInputDialog(text="ID del usuario a actualizar:", title="Actualizar Usuario").get_input()
    if not id_usuario:
        return
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id_usuario,))
    resultado = cursor.fetchone()
    if resultado:
        nuevo_usuario = ctk.CTkInputDialog(text="Nuevo nombre de usuario:", title="Actualizar").get_input()
        nueva_contraseña = ctk.CTkInputDialog(text="Nueva contraseña:", title="Actualizar").get_input()
        nuevo_correo = ctk.CTkInputDialog(text="Nuevo correo:", title="Actualizar").get_input()
        nuevo_telefono = ctk.CTkInputDialog(text="Nuevo teléfono:", title="Actualizar").get_input()
        nueva_relacion = ctk.CTkInputDialog(text="Nueva relación:", title="Actualizar").get_input()
        nuevo_cumpleaños = ctk.CTkInputDialog(text="Nuevo cumpleaños:", title="Actualizar").get_input()

        cursor.execute("""
        UPDATE usuarios
        SET usuario=?, contraseña=?, Correo=?, telefono=?, RelacionCon=?, cumpleaños=?
        WHERE id=?
        """, (nuevo_usuario, nueva_contraseña, nuevo_correo, nuevo_telefono, nueva_relacion, nuevo_cumpleaños, id_usuario))
        conn.commit()
        mostrar_mensaje("✅ Usuario actualizado correctamente.")
    else:
        mostrar_mensaje("❌ No se encontró un usuario con ese ID.")

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


# Ventana principal (solo accesible tras login)
def mostrar_ventana_Admin():
    cursor.connection
    global textbox  # Para que mostrar_mensaje funcione
    ventana = ctk.CTk()
    ventana.geometry("1280x720")
    ventana.title("SUNFLOWER - Admin Panel")

    # Crear un marco principal para dividir la ventana en dos secciones
    marco_principal = ctk.CTkFrame(ventana)
    marco_principal.pack(fill="both", expand=True, padx=10, pady=10)

    # Sección izquierda: Panel de información
    marco_izquierdo = ctk.CTkFrame(marco_principal, width=800)
    marco_izquierdo.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    label_info = ctk.CTkLabel(marco_izquierdo, text="Panel de Información", font=("Arial", 20))
    label_info.pack(pady=10)

    textbox = ctk.CTkTextbox(marco_izquierdo, width=700, height=600)
    textbox.pack(pady=10)

    # Sección derecha: Botones de acciones
    marco_derecho = ctk.CTkFrame(marco_principal, width=400)
    marco_derecho.pack(side="left", fill="y", padx=10, pady=10)

    label_acciones = ctk.CTkLabel(marco_derecho, text="Acciones", font=("Arial", 20))
    label_acciones.pack(pady=10)

    botones = [
        ("Crear usuario", crear_usuario),
        ("Leer usuarios", leer_usuarios),
        ("Actualizar usuario", actualizar_usuario),
        ("Eliminar usuario", eliminar_usuario),
    ]

    for texto, comando in botones:
        btn = ctk.CTkButton(marco_derecho, text=texto, command=comando, width=300)
        btn.pack(pady=10)

    # Botón para cerrar sesión
    def cerrar_sesion():
        ventana.destroy()
        mainSF.login()

    btn_cerrar_sesion = ctk.CTkButton(marco_derecho, text="Cerrar sesión", command=cerrar_sesion, width=300)
    btn_cerrar_sesion.pack(pady=10)

    ventana.mainloop()