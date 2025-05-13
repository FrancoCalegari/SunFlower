import customtkinter as ctk
import sqlite3
import os
from tkinter import messagebox
from PIL import Image, ImageTk, ImageOps

# Modulo personalizado para manejo de fotos de perfil
import profilephotoSF

# Modulo personalizado panel administrador
import adminpanelF
import userspanelSF
from dbController import get_connection, init_db

conn = get_connection()
cursor = conn.cursor()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

init_db()


def login():
    # Crear la imagen por defecto si no existe
    imagen_default_path = "defaultuser.png"
    imagen_seleccionada = {"ruta": None}
    img_preview = None
    img_label = None
    
    def mostrar_login():
        limpiar_contenedor()
        titulo_label.configure(text="Iniciar Sesión")

        ctk.CTkLabel(contenedor, text="Usuario").pack(pady=5)
        entry_user.pack(pady=5)

        ctk.CTkLabel(contenedor, text="Contraseña").pack(pady=5)
        entry_pass.pack(pady=5)

        btn_login.pack(pady=10)
        btn_registro.pack(pady=5)

    def mostrar_registro():
        
        limpiar_contenedor()

        

            # Imagen por defecto y preview
        def actualizar_preview():
            nonlocal img_preview, img_label
            ruta = imagen_seleccionada["ruta"] or imagen_default_path
            try:
                img = Image.open(ruta).resize((100, 100))
                img = ImageOps.expand(img, border=3, fill="black")  # Simula border-radius
                img_preview = ctk.CTkImage(img, size=(100, 100))
                if img_label:
                    img_label.configure(image=img_preview)
                else:
                    img_label = ctk.CTkLabel(contenedor, image=img_preview, text="")
                    img_label.pack(pady=10)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")

        def seleccionar_imagen():
            import easygui
            archivo = easygui.fileopenbox(title="Selecciona una imagen de perfil", filetypes=["*.png", "*.jpg", "*.jpeg"])
            if archivo:
                imagen_seleccionada["ruta"] = archivo
                actualizar_preview()

        actualizar_preview()

        ctk.CTkButton(contenedor, text="Seleccionar imagen de perfil (opcional)", command=seleccionar_imagen).pack(pady=5)

        titulo_label.configure(text="Registro de Usuario")

        ctk.CTkLabel(contenedor, text="Usuario").pack(pady=5)
        entry_user.pack(pady=5)

        ctk.CTkLabel(contenedor, text="Contraseña").pack(pady=5)
        entry_pass.pack(pady=5)

        ctk.CTkLabel(contenedor, text="Correo").pack(pady=5)
        entry_email.pack(pady=5)

        ctk.CTkLabel(contenedor, text="Teléfono").pack(pady=5)
        entry_phone.pack(pady=5)

        ctk.CTkLabel(contenedor, text="Cumpleaños").pack(pady=5)
        entry_birthday.pack(pady=5)


        btn_registrar.pack(pady=10)
        btn_volver.pack(pady=5)

    def limpiar_contenedor():
        for widget in contenedor.winfo_children():
            widget.pack_forget()

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

    def registrar_usuario():
        usuario = entry_user.get()
        contraseña = entry_pass.get()
        correo = entry_email.get()
        telefono = entry_phone.get()
        cumpleaños = entry_birthday.get()

        if not (usuario and contraseña and correo and telefono and cumpleaños):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        cursor.execute("SELECT * FROM usuarios WHERE usuario = ? OR Correo = ?", (usuario, correo))
        if cursor.fetchone():
            messagebox.showerror("Error", "El usuario o correo ya están registrados.")
            return

        cursor.execute("INSERT INTO usuarios (usuario, contraseña, Correo, telefono, cumpleaños) VALUES (?, ?, ?, ?, ?)",
                    (usuario, contraseña, correo, telefono, cumpleaños))

        conn.commit()
            # Crear carpeta del usuario
        carpeta_usuario = os.path.join("users", usuario)
        os.makedirs(carpeta_usuario, exist_ok=True)

        ruta_destino = os.path.join(carpeta_usuario, "profile.png")

        # Guardar imagen o imagen por defecto
        try:
            ruta_origen = imagen_seleccionada["ruta"] or imagen_default_path
            imagen = Image.open(ruta_origen)
            imagen.save(ruta_destino)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la imagen de perfil: {e}")
            return

        messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
        mostrar_login()

    login_window = ctk.CTk()
    login_window.geometry("1280x720")
    login_window.title("SUNFLOWER - Login")

    # Contenedor centrado
    contenedor_central = ctk.CTkFrame(login_window)
    contenedor_central.place(relx=0.5, rely=0.5, anchor="center")

    titulo_label = ctk.CTkLabel(contenedor_central, text="Iniciar Sesión", font=("Arial", 20))
    titulo_label.pack(pady=10)

    contenedor = ctk.CTkFrame(contenedor_central)
    contenedor.pack(padx=20, pady=20)

    # Entradas compartidas
    entry_user = ctk.CTkEntry(contenedor, placeholder_text="Usuario")
    entry_pass = ctk.CTkEntry(contenedor, show="*", placeholder_text="Contraseña")
    entry_email = ctk.CTkEntry(contenedor, placeholder_text="Correo")
    entry_phone = ctk.CTkEntry(contenedor, placeholder_text="Teléfono")
    entry_birthday = ctk.CTkEntry(contenedor, placeholder_text="Cumpleaños")

    # Botones
    btn_login = ctk.CTkButton(contenedor, text="Iniciar sesión", command=verificar_login)
    btn_registro = ctk.CTkButton(contenedor, text="Registrarse", command=mostrar_registro)

    btn_registrar = ctk.CTkButton(contenedor, text="Registrar", command=registrar_usuario)
    btn_volver = ctk.CTkButton(contenedor, text="Volver al Login", command=mostrar_login)

    mostrar_login()
    login_window.mainloop()



if __name__ == "__main__":
    login()
    conn.close()
