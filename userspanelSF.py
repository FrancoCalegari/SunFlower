import customtkinter as ctk
import os
from tkinter import messagebox, filedialog
from tkcalendar import Calendar
from PIL import ImageTk

import profilephotoSF
from dbController import get_connection
conn = get_connection()
cursor = conn.cursor()


def mostrar_ventana_usuario_normal(usuario):
    ventana = ctk.CTk()
    ventana.geometry("1280x720")
    ventana.title(f"SUNFLOWER - {usuario[1]} 🌻")

    pareja = usuario[5]  # RelacionCon

    # --- Frame principal para organizar el contenido en dos columnas
    frame_principal = ctk.CTkFrame(ventana)
    frame_principal.pack(pady=20, padx=20, fill="both", expand=True)

    # --- Frame para la foto de perfil (Izquierda)
    frame_izquierda = ctk.CTkFrame(frame_principal, width=200)
    frame_izquierda.pack(side="left", fill="y", padx=(0, 10))

    # --- Frame para la información (Derecha)
    frame_derecha = ctk.CTkFrame(frame_principal)
    frame_derecha.pack(side="right", fill="both", expand=True)

    # --- Mostrar foto de perfil en la izquierda
    ruta_foto = os.path.join('users', usuario[1], 'profile.png')
    foto = profilephotoSF.obtener_foto_redonda(ruta_foto)

    if foto:
        label_foto = ctk.CTkLabel(frame_izquierda, image=foto, text="")
        label_foto.image = foto
        label_foto.pack(pady=10)

    # --- Estado de relación en la derecha
    estado_relacion = f"""
    👤 Usuario: {usuario[1]}
    📧 Correo: {usuario[3]}
    📱 Teléfono: {usuario[4]}
    💕 Relación con: {usuario[5]}
    🎂 Cumpleaños: {usuario[6]}
    """

    label = ctk.CTkLabel(frame_derecha, text="Estado de tu relación ❤️", font=("Arial", 20))
    label.pack(pady=10)

    textbox = ctk.CTkTextbox(frame_derecha, width=700, height=120)
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
        def ventana_agregar_evento():
            titulo = entry_titulo.get()
            descripcion = entry_descripcion.get()
            duracion = entry_duracion.get()
            estimado = entry_estimado.get()
            genero = entry_genero.get()
            clasificacion = entry_clasificacion.get()
            lugar = entry_lugar.get()

            if not (titulo and descripcion and duracion and estimado and lugar):
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return
            else:
                cursor.execute("""
                INSERT INTO eventos (titulo, descripción, duracionEvento, TiempoEstimado, genero, clasificacion, FueraDentro)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (titulo, descripcion, duracion, estimado, genero, clasificacion, lugar))
                conn.commit()
                messagebox.showinfo("Éxito", "🎉 Evento agregado correctamente.")
        
        evento_window = ctk.CTk()
        evento_window.geometry("1280x720")
        evento_window.title("SUNFLOWER - Agregar evento")
        
        ctk.CTkLabel(evento_window, text="Titulo").pack(pady=10)
        entry_titulo = ctk.CTkEntry(evento_window)
        entry_titulo.pack()

        ctk.CTkLabel(evento_window, text="Descripción del evento").pack(pady=10)
        entry_descripcion = ctk.CTkEntry(evento_window)
        entry_descripcion.pack()

        ctk.CTkLabel(evento_window, text="Duración del evento").pack(pady=10)
        entry_duracion = ctk.CTkEntry(evento_window)
        entry_duracion.pack()

        ctk.CTkLabel(evento_window, text="Tiempo estimado").pack(pady=10)
        entry_estimado = ctk.CTkEntry(evento_window)
        entry_estimado.pack()

        ctk.CTkLabel(evento_window, text="Etiqueta (Aire libre, Gamer, etc.)").pack(pady=10)
        entry_genero = ctk.CTkEntry(evento_window)
        entry_genero.pack()

        ctk.CTkLabel(evento_window, text="Clasificación (A, B, C...)").pack(pady=10)
        entry_clasificacion = ctk.CTkEntry(evento_window)
        entry_clasificacion.pack()

        ctk.CTkLabel(evento_window, text="Lugar").pack(pady=10)
        entry_lugar = ctk.CTkEntry(evento_window)
        entry_lugar.pack()

        btn_guardar_cambios = ctk.CTkButton(
            evento_window, 
            text="Guardar Evento", 
            command=lambda: [ventana_agregar_evento(), evento_window.destroy()]
        )
        btn_guardar_cambios.pack(pady=20)

        btn_volver = ctk.CTkButton(evento_window, text="Cancelar", command=lambda: [evento_window.destroy()])
        btn_volver.pack(pady=10)
        evento_window.mainloop()


    # --- Función para cerrar sesión
    def cerrar_sesion():
        ventana.destroy()
        import mainSF
        mainSF.login()
    # --- Galería de fotos
    galeria_frame = ctk.CTkFrame(frame_izquierda, width=300, height=200)
    galeria_frame.pack(pady=15)

    def cargar_galeria():
        ruta_usuario = os.path.join('users', usuario[1])
        archivos = os.listdir(ruta_usuario)
        fotos = [f for f in archivos if f.endswith(('.png', '.jpg', '.jpeg', '.webp')) and f != 'profile.png']

        for widget in galeria_frame.winfo_children():
            widget.destroy()

        for foto in fotos:
            ruta_foto = os.path.join(ruta_usuario, foto)
            img = profilephotoSF.obtener_foto_redonda(ruta_foto, tamaño=(50, 50))
            if img:
                label_foto = ctk.CTkLabel(galeria_frame, image=img, text="")
                label_foto.image = img
                label_foto.pack(pady=5)

    def subir_foto():
        ruta_usuario = os.path.join('users', usuario[1])
        os.makedirs(ruta_usuario, exist_ok=True)

        archivo = filedialog.askopenfilename(title='Seleccionar foto', filetypes=[('Imágenes', '*.png *.jpg *.jpeg *.webp')])
        if archivo:
            nombre_archivo = os.path.basename(archivo)
            destino = os.path.join(ruta_usuario, nombre_archivo)
            os.rename(archivo, destino)
            cargar_galeria()
            messagebox.showinfo('Éxito', 'Foto subida correctamente.')

    cargar_galeria()

    btn_subir_foto = ctk.CTkButton(frame_izquierda, text="Subir Foto a la galería", command=subir_foto)
    btn_subir_foto.pack(pady=5)

    # --- Calendario compacto
    def mostrar_eventos_seleccionados(event):
        fecha_seleccionada = calendario.get_date()
        cursor.execute("SELECT * FROM eventos WHERE descripción LIKE ?", ('%' + pareja + '%',))
        eventos = cursor.fetchall()
        eventos_mensaje = f"Eventos para {fecha_seleccionada}:\n\n"
        for ev in eventos:
            eventos_mensaje += f"Título: {ev[0]} | Descripción: {ev[1]} | Duración: {ev[2]}h\n"

        if not eventos:
            eventos_mensaje = "⚠️ No hay eventos para esta fecha."

        messagebox.showinfo("Eventos en la fecha seleccionada", eventos_mensaje)

    # --- Calendario estilizado y centrado
    calendario_frame = ctk.CTkFrame(frame_derecha, width=450, height=500, corner_radius=15)
    calendario_frame.pack(pady=20, padx=(30), side="right")

    calendario = Calendar(
        calendario_frame,
        selectmode="day",
        background="#2b2b2b",
        foreground="#FFFFFF",
        headersbackground="#2b2b2b",
        headersforeground="#1f6aa5",
        borderwidth=0,
        weekendbackground="#1f6aa5",
        weekendforeground="#FFFFFF",
        othermonthbackground="#2C2F33",
        othermonthforeground="#6C7A89",
        font=("Arial", 10)
    )
    calendario.pack(pady=20, padx=20)
    calendario.bind("<<CalendarSelected>>", mostrar_eventos_seleccionados)

    # --- Función para cerrar sesión
    def cerrar_sesion():
        ventana.destroy()
        import mainSF
        mainSF.login()
    # --- Botones
    btn_ver_eventos = ctk.CTkButton(frame_derecha, text="📂 Ver eventos con mi pareja", command=ver_eventos)
    btn_ver_eventos.pack(pady=10)

    btn_agregar_evento = ctk.CTkButton(frame_derecha, text="➕ Agregar evento", command=agregar_evento)
    btn_agregar_evento.pack(pady=10)

    btn_gestionar_foto = ctk.CTkButton(frame_izquierda, text="📸 Cambiar foto de perfil", command=lambda: gestionar_foto_perfil(usuario[1]))
    btn_gestionar_foto.pack(pady=10)

    btn_cerrar_sesion = ctk.CTkButton(frame_derecha, text="🔒 Cerrar sesión", command=cerrar_sesion)
    btn_cerrar_sesion.pack(pady=10)

    ventana.mainloop()



# --- NUEVA FUNCIÓN: Mostrar y cambiar foto de perfil
def gestionar_foto_perfil(usuario):
    ventana_foto = ctk.CTkToplevel()
    ventana_foto.geometry("400x300")
    ventana_foto.title("Gestionar Foto de Perfil")

    ruta_foto = os.path.join('users', usuario, 'profile.png')
    foto = profilephotoSF.obtener_foto_redonda(ruta_foto)

    if foto:
        label_foto = ctk.CTkLabel(ventana_foto, image=foto, text="")
        label_foto.image = foto
        label_foto.pack(pady=10)

    def cambiar_foto():
        nueva_foto = profilephotoSF.cambiar_foto_perfil(usuario)
        if nueva_foto:
            nueva_img = profilephotoSF.obtener_foto_redonda(nueva_foto)
            label_foto.configure(image=nueva_img)
            label_foto.image = nueva_img

    btn_cambiar_foto = ctk.CTkButton(ventana_foto, text="Cambiar Foto de Perfil", command=cambiar_foto)
    btn_cambiar_foto.pack(pady=10)

    ventana_foto.mainloop()