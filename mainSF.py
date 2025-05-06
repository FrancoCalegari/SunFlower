import customtkinter as ctk
import sqlite3
import os
from tkinter import messagebox

#modulo personalizado panel administrador
import adminpanelF
import userspanelSF
# Obtener conexión y trabajar con la base de datos
from dbController import get_connection, init_db
conn = get_connection()
cursor = conn.cursor()


# Configuración de la app
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Inicializar la base de datos (crear tablas si no existen)
init_db()


# Ventana de Login
def login():
    def verificar_login():
        usuario = entry_user.get()
        contraseña = entry_pass.get()

        if usuario == "root" and contraseña == "root":
            login_window.destroy()
            adminpanelF.mostrar_ventana_Admin()
        else:
            cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND contraseña = ?", (usuario, contraseña))
            user = cursor.fetchone()
            if user:
                login_window.destroy()
                userspanelSF.mostrar_ventana_usuario_normal(user)
            else:
                messagebox.showerror("Error", "Credenciales incorrectas o usuario no registrado.")

    def abrir_registro():
        login_window.destroy()
        ventana_registro()

    login_window = ctk.CTk()
    login_window.geometry("1280x720")
    login_window.title("SUNFLOWER - Login")

    ctk.CTkLabel(login_window, text="Usuario").pack(pady=10)
    entry_user = ctk.CTkEntry(login_window)
    entry_user.pack()

    ctk.CTkLabel(login_window, text="Contraseña").pack(pady=10)
    entry_pass = ctk.CTkEntry(login_window, show="*")
    entry_pass.pack()

    btn_login = ctk.CTkButton(login_window, text="Iniciar sesión", command=verificar_login)
    btn_login.pack(pady=20)

    btn_registro = ctk.CTkButton(login_window, text="Registrarse", command=abrir_registro)
    btn_registro.pack(pady=10)

    login_window.mainloop()

# Ventana de Registro
def ventana_registro():
    def registrar_usuario():
        usuario = entry_user.get()
        contraseña = entry_pass.get()
        correo = entry_email.get()
        telefono = entry_phone.get()
        relacion = entry_relation.get()
        cumpleaños = entry_birthday.get()

        if not (usuario and contraseña and correo and telefono and relacion and cumpleaños):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        cursor.execute("SELECT * FROM usuarios WHERE usuario = ? OR Correo = ?", (usuario, correo))
        if cursor.fetchone():
            messagebox.showerror("Error", "El usuario o correo ya están registrados.")
            return

        cursor.execute("INSERT INTO usuarios (usuario, contraseña, Correo, telefono, RelacionCon, cumpleaños) VALUES (?, ?, ?, ?, ?, ?)",
                       (usuario, contraseña, correo, telefono, relacion, cumpleaños))
        conn.commit()
        messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
        registro_window.destroy()
        login()

    registro_window = ctk.CTk()
    registro_window.geometry("1280x720")
    registro_window.title("SUNFLOWER - Registro")

    ctk.CTkLabel(registro_window, text="Usuario").pack(pady=10)
    entry_user = ctk.CTkEntry(registro_window)
    entry_user.pack()

    ctk.CTkLabel(registro_window, text="Contraseña").pack(pady=10)
    entry_pass = ctk.CTkEntry(registro_window, show="*")
    entry_pass.pack()

    ctk.CTkLabel(registro_window, text="Correo").pack(pady=10)
    entry_email = ctk.CTkEntry(registro_window)
    entry_email.pack()

    ctk.CTkLabel(registro_window, text="Teléfono").pack(pady=10)
    entry_phone = ctk.CTkEntry(registro_window)
    entry_phone.pack()

    ctk.CTkLabel(registro_window, text="Relación con").pack(pady=10)
    entry_relation = ctk.CTkEntry(registro_window)
    entry_relation.pack()

    ctk.CTkLabel(registro_window, text="Cumpleaños").pack(pady=10)
    entry_birthday = ctk.CTkEntry(registro_window)
    entry_birthday.pack()

    btn_registrar = ctk.CTkButton(registro_window, text="Registrar", command=registrar_usuario)
    btn_registrar.pack(pady=20)

    btn_volver = ctk.CTkButton(registro_window, text="Volver", command=lambda: [registro_window.destroy(), login()])
    btn_volver.pack(pady=10)

    registro_window.mainloop()

# Iniciar app
login()

# Cierre de la conexión al salir
conn.close()
