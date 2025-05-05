import customtkinter as ctk
import sqlite3
import os
from tkinter import messagebox

# Configuración de la app
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Conexión a la base de datos
conn = sqlite3.connect("SunFlower.db")
cursor = conn.cursor()

# Crear tablas si no existen
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT NOT NULL,
    contraseña TEXT NOT NULL,
    Correo TEXT NOT NULL,
    telefono NUMERIC NOT NULL,
    RelacionCon TEXT NOT NULL,
    cumpleaños NUMERIC NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS eventos (
    titulo TEXT NOT NULL,
    descripción TEXT NOT NULL,
    duracionEvento NUMERIC NOT NULL,
    TiempoEstimado NUMERIC NOT NULL,
    genero TEXT NOT NULL,
    clasificacion TEXT NOT NULL,
    FueraDentro TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS relaciones (
    NombreRelacion TEXT NOT NULL,
    FechaDeRelacion NUMERIC NOT NULL,
    EventosExtra TEXT NOT NULL
)
""")

conn.commit()

# Funciones
def mostrar_mensaje(mensaje):
    textbox.delete("0.0", "end")
    textbox.insert("0.0", mensaje)

def crear_usuario():
    ventana_crear = ctk.CTkToplevel()
    ventana_crear.geometry("400x500")
    ventana_crear.title("Crear Usuario")

    ctk.CTkLabel(ventana_crear, text="Nombre de usuario:").pack(pady=5)
    entry_usuario = ctk.CTkEntry(ventana_crear)
    entry_usuario.pack(pady=5)

    ctk.CTkLabel(ventana_crear, text="Contraseña:").pack(pady=5)
    entry_contraseña = ctk.CTkEntry(ventana_crear, show="*")
    entry_contraseña.pack(pady=5)

    ctk.CTkLabel(ventana_crear, text="Correo:").pack(pady=5)
    entry_correo = ctk.CTkEntry(ventana_crear)
    entry_correo.pack(pady=5)

    ctk.CTkLabel(ventana_crear, text="Teléfono:").pack(pady=5)
    entry_telefono = ctk.CTkEntry(ventana_crear)
    entry_telefono.pack(pady=5)

    ctk.CTkLabel(ventana_crear, text="Relación con:").pack(pady=5)
    entry_relacion = ctk.CTkEntry(ventana_crear)
    entry_relacion.pack(pady=5)

    ctk.CTkLabel(ventana_crear, text="Cumpleaños:").pack(pady=5)
    entry_cumpleaños = ctk.CTkEntry(ventana_crear)
    entry_cumpleaños.pack(pady=5)

    def guardar_usuario():
        usuario = entry_usuario.get()
        contraseña = entry_contraseña.get()
        correo = entry_correo.get()
        telefono = entry_telefono.get()
        relacion = entry_relacion.get()
        cumpleaños = entry_cumpleaños.get()

        if usuario and contraseña and correo and telefono and relacion and cumpleaños:
            cursor.execute("INSERT INTO usuarios (usuario, contraseña, Correo, telefono, RelacionCon, cumpleaños) VALUES (?, ?, ?, ?, ?, ?)",
                           (usuario, contraseña, correo, telefono, relacion, cumpleaños))
            conn.commit()
            mostrar_mensaje("✅ Tu usuario fue creado con éxito.")
            ventana_crear.destroy()
        else:
            messagebox.showerror("Error", "⚠️ Todos los campos son obligatorios.")

    ctk.CTkButton(ventana_crear, text="Guardar", command=guardar_usuario).pack(pady=20)

def leer_usuarios():
    cursor.execute("SELECT id, usuario, Correo, telefono, RelacionCon, cumpleaños FROM usuarios")
    usuarios = cursor.fetchall()
    if usuarios:
        mensaje = "📋 Lista de usuarios:\n\n"
        for user in usuarios:
            mensaje += f"ID: {user[0]} | Usuario: {user[1]} | Correo: {user[2]} | Tel: {user[3]} | Relación: {user[4]} | Cumpleaños: {user[5]}\n"
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
    global textbox  # Para que mostrar_mensaje funcione
    ventana = ctk.CTk()
    ventana.geometry("1280x720")
    ventana.title("SUNFLOWER - Admin Panel")

    textbox = ctk.CTkTextbox(ventana, width=650, height=300)
    textbox.pack(pady=10)

    botones = [
        ("Crear usuario", crear_usuario),
        ("Leer usuarios", leer_usuarios),
        ("Actualizar usuario", actualizar_usuario),
        ("Eliminar usuario", eliminar_usuario),
    ]


    for texto, comando in botones:
        btn = ctk.CTkButton(ventana, text=texto, command=comando, width=300)
        btn.pack(pady=5)

    ventana.mainloop()

def mostrar_ventana_usuario_normal(usuario):
    ventana = ctk.CTk()
    ventana.geometry("900x600")
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
        ventana_evento = ctk.CTkToplevel()
        ventana_evento.geometry("400x500")
        ventana_evento.title("Crear Usuario")

        ctk.CTkLabel(ventana_evento, text="Título del evento:").pack(pady=5)
        entry_titulo = ctk.CTkEntry(ventana_evento)
        entry_titulo.pack(pady=5)
        
        ctk.CTkLabel(ventana_evento, text="Descripción:").pack(pady=5)
        entry_descripcion = ctk.CTkEntry(ventana_evento)
        entry_descripcion.pack(pady=5)

        ctk.CTkLabel(ventana_evento, text="Duración del evento (horas):").pack(pady=5)
        entry_duracion = ctk.CTkEntry(ventana_evento)
        entry_duracion.pack(pady=5)

        ctk.CTkLabel(ventana_evento, text="Tiempo estimado (horas):").pack(pady=5)
        entry_estimado = ctk.CTkEntry(ventana_evento)
        entry_estimado.pack(pady=5)

        ctk.CTkLabel(ventana_evento, text="Género:").pack(pady=5)
        entry_genero = ctk.CTkEntry(ventana_evento)
        entry_genero.pack(pady=5)

        ctk.CTkLabel(ventana_evento, text="Clasificación:").pack(pady=5)
        entry_clasificacion = ctk.CTkEntry(ventana_evento)
        entry_clasificacion.pack(pady=5)

        ctk.CTkLabel(ventana_evento, text="Lugar:").pack(pady=5)
        entry_lugar = ctk.CTkEntry(ventana_evento)
        entry_lugar.pack(pady=5)

        def guardar_evento():
            titulo = entry_titulo.get()
            descripcion = entry_descripcion.get()
            duracion = entry_duracion.get()
            estimado = entry_estimado.get()
            genero = entry_genero.get()
            clasificacion = entry_clasificacion.get()
            lugar = entry_lugar.get()

            if titulo and descripcion and duracion and estimado and genero and clasificacion and lugar:
                cursor.execute("""
                INSERT INTO eventos (titulo, descripción, duracionEvento, TiempoEstimado, genero, clasificacion, FueraDentro)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (titulo, descripcion, duracion, estimado, genero, clasificacion, lugar))
                conn.commit()
                messagebox.showinfo("Éxito", "🎉 Evento agregado correctamente.")
                ventana_evento.destroy()
            else:
                messagebox.showerror("Error", "⚠️ Todos los campos son obligatorios.")

        ctk.CTkButton(ventana_evento, text="Guardar", command=guardar_evento).pack(pady=20)
        
    # --- Botones
    btn_ver_eventos = ctk.CTkButton(ventana, text="📂 Ver eventos con mi pareja", command=ver_eventos)
    btn_ver_eventos.pack(pady=10)

    btn_agregar_evento = ctk.CTkButton(ventana, text="➕ Agregar evento", command=agregar_evento)
    btn_agregar_evento.pack(pady=10)

    ventana.mainloop()



# Ventana de Login
def login():
    def verificar_login():
        usuario = entry_user.get()
        contraseña = entry_pass.get()

        if usuario == "root" and contraseña == "root":
            login_window.destroy()
            mostrar_ventana_Admin()
        else:
            cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND contraseña = ?", (usuario, contraseña))
            user = cursor.fetchone()
            if user:
                login_window.destroy()
                mostrar_ventana_usuario_normal(user)
            else:
                messagebox.showerror("Error", "Credenciales incorrectas o usuario no registrado.")


    login_window = ctk.CTk()
    login_window.geometry("400x300")
    login_window.title("SUNFLOWER - Login")

    ctk.CTkLabel(login_window, text="Usuario").pack(pady=10)
    entry_user = ctk.CTkEntry(login_window)
    entry_user.pack()

    ctk.CTkLabel(login_window, text="Contraseña").pack(pady=10)
    entry_pass = ctk.CTkEntry(login_window, show="*")
    entry_pass.pack()

    btn_login = ctk.CTkButton(login_window, text="Iniciar sesión", command=verificar_login)
    btn_login.pack(pady=20)

    btn_login = ctk.CTkButton(login_window, text="Registrarse", command=crear_usuario)
    btn_login.pack(pady=20)

    login_window.mainloop()

# Iniciar app
login()

# Cierre de la conexión al salir
conn.close()
