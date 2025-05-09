import os
import shutil
from tkinter import filedialog, messagebox
import customtkinter as ctk
from PIL import Image, ImageTk, ImageOps, ImageDraw

# Función para subir la foto de perfil en el registro
def subir_foto_perfil(usuario):
    ruta_carpeta = os.path.join('users', usuario)
    os.makedirs(ruta_carpeta, exist_ok=True)

    ruta_foto = filedialog.askopenfilename(title='Seleccionar foto de perfil', filetypes=[('Imágenes', '*.png *.jpg *.jpeg *.webp')])

    if ruta_foto:
        ruta_destino = os.path.join(ruta_carpeta, 'profile.png')
        shutil.copy(ruta_foto, ruta_destino)
        messagebox.showinfo('Éxito', 'Foto de perfil guardada correctamente.')
        return ruta_destino
    else:
        messagebox.showerror('Error', 'No se seleccionó ninguna imagen.')
        return None

# Función para cambiar la foto de perfil desde el panel de usuario
def cambiar_foto_perfil(usuario):
    ruta_carpeta = os.path.join('users', usuario)
    ruta_foto_actual = os.path.join(ruta_carpeta, 'profile.png')

    if not os.path.exists(ruta_foto_actual):
        messagebox.showwarning('Advertencia', 'No se ha encontrado una foto de perfil para este usuario.')

    ruta_foto_nueva = filedialog.askopenfilename(title='Seleccionar nueva foto de perfil', filetypes=[('Imágenes', '*.png *.jpg *.jpeg *.webp')])

    if ruta_foto_nueva:
        shutil.copy(ruta_foto_nueva, ruta_foto_actual)
        messagebox.showinfo('Éxito', 'Foto de perfil actualizada correctamente.')
        return ruta_foto_actual
    else:
        messagebox.showerror('Error', 'No se seleccionó ninguna imagen.')
        return None

# Función para obtener la foto de perfil en forma redonda
def obtener_foto_redonda(ruta_foto, tamaño=(150, 150)):
    if not os.path.exists(ruta_foto):
        return None

    try:
        img = Image.open(ruta_foto).resize(tamaño)
        mask = Image.new('L', tamaño, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + tamaño, fill=255)
        img = ImageOps.fit(img, tamaño, centering=(0.5, 0.5))
        img.putalpha(mask)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        messagebox.showerror('Error', f'Error al cargar la foto de perfil: {e}')
        return None
