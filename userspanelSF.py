import customtkinter as ctk
import sqlite3
import os
from tkinter import messagebox

import mainSF

# Obtener conexión y trabajar con la base de datos
from dbController import get_connection, init_db
conn = get_connection()
cursor = conn.cursor()


def mostrar_ventana_usuario_normal(usuario):
    ventana = ctk.CTk()
    ventana.geometry("1280x720")
    ventana.title(f"SUNFLOWER - {usuario[1]} 🌻")

    pareja = usuario[5]  # RelacionCon

    # --- Estado de relación
    estado_relacion = f"""
        👤 Usuario: {usuario[1]}
        📧 Correo: {usuario[3]}
        📱 Teléfono: {usuario[4]}
        💕 Relación con: {usuario[5]}
        🎂 Cumpleaños: {usuario[6]}
    """

    label = ctk.CTkLabel(ventana, text="Estado de tu relación ❤️", font=("Arial", 20))
    label.pack(pady=10)

    textbox = ctk.CTkTextbox(ventana, width=700, height=120)
    textbox.insert("0.0", estado_relacion)
    textbox.configure(state="disabled")
    textbox.pack(pady=10)

    # --- Función para ver eventos relacionados con la pareja
    def ver_eventos():
        cursor.execute("SELECT * FROM eventos WHERE descripción LIKE ?", ('%' + pareja + '%',))
        eventos = cursor.fetchall()
        if eventos:
            texto = "📅 Eventos relacionados:\n\n"
            for ev in eventos:
                texto += f"Título: {ev[0]} | Descripción: {ev[1]} | Duración: {ev[2]} | Tiempo estimado: {ev[3]} | Género: {ev[4]} | Clasificación: {ev[5]} | Lugar: {ev[6]}\n\n"
        else:
            texto = "⚠️ No hay eventos relacionados con tu pareja."
        messagebox.showinfo("Eventos", texto)

    # --- Función para agregar un evento
    def agregar_evento():
        titulo = ctk.CTkInputDialog(text="Título del evento:", title="Agregar Evento").get_input()
        descripcion = ctk.CTkInputDialog(text="Descripción (incluye nombre de tu pareja para vincularlo):", title="Agregar Evento").get_input()
        duracion = ctk.CTkInputDialog(text="Duración (horas):", title="Agregar Evento").get_input()
        estimado = ctk.CTkInputDialog(text="Tiempo estimado (minutos):", title="Agregar Evento").get_input()
        genero = ctk.CTkInputDialog(text="Género del evento (comedia, romántico, etc.):", title="Agregar Evento").get_input()
        clasificacion = ctk.CTkInputDialog(text="Clasificación (A, B, C):", title="Agregar Evento").get_input()
        lugar = ctk.CTkInputDialog(text="¿Es dentro o fuera?", title="Agregar Evento").get_input()

        if titulo and descripcion and duracion and estimado and genero and clasificacion and lugar:
            cursor.execute("""
            INSERT INTO eventos (titulo, descripción, duracionEvento, TiempoEstimado, genero, clasificacion, FueraDentro)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (titulo, descripcion, duracion, estimado, genero, clasificacion, lugar))
            conn.commit()
            messagebox.showinfo("Éxito", "🎉 Evento agregado correctamente.")

    # --- Función para cerrar sesión
    def cerrar_sesion():
        ventana.destroy()
        mainSF.login()

    # --- Botones
    btn_ver_eventos = ctk.CTkButton(ventana, text="📂 Ver eventos con mi pareja", command=ver_eventos)
    btn_ver_eventos.pack(pady=10)

    btn_agregar_evento = ctk.CTkButton(ventana, text="➕ Agregar evento", command=agregar_evento)
    btn_agregar_evento.pack(pady=10)

    btn_cerrar_sesion = ctk.CTkButton(ventana, text="🔒 Cerrar sesión", command=cerrar_sesion)
    btn_cerrar_sesion.pack(pady=10)

    ventana.mainloop()