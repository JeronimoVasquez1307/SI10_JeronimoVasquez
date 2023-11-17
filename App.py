import streamlit as st
import numpy as np
from PIL import Image
from skimage import io, filters, exposure, color
from scipy import ndimage
import io as bytes_io
import base64

# Función para aplicar filtro de desenfoque
def aplicar_desenfoque(imagen, sigma):
    """
    Aplica un filtro de desenfoque gaussiano a la imagen.

    Argumentos:
    imagen (array): Imagen a procesar.
    sigma (float): Valor del desenfoque gaussiano.

    Retorna:
    array: Imagen procesada con desenfoque aplicado.
    """
    desenfocada = ndimage.gaussian_filter(imagen, sigma=sigma)
    return desenfocada

# Función para aplicar filtro de detección de bordes
def aplicar_deteccion_bordes(imagen):
    """
    Aplica un filtro de detección de bordes a la imagen.

    Argumentos:
    imagen (array): Imagen a procesar.

    Retorna:
    array: Imagen con detección de bordes aplicada.
    """
    bordes = filters.sobel(color.rgb2gray(imagen))
    return bordes

# Función para ajustar el brillo y contraste
def ajustar_brillo_contraste(imagen, brillo, contraste):
    """
    Ajusta el brillo y contraste de la imagen.

    Argumentos:
    imagen (array): Imagen a procesar.
    brillo (float): Valor de ajuste de brillo.
    contraste (float): Valor de ajuste de contraste.

    Retorna:
    array: Imagen con brillo y contraste ajustados.
    """
    ajustada = exposure.adjust_gamma(imagen, brillo)
    ajustada = exposure.rescale_intensity(ajustada, in_range=(0, 1), 
                                          out_range=(0, 1))
    return ajustada

# Función para rotar la imagen
def rotar_imagen(imagen, angulo):
    """
    Rota la imagen según el ángulo proporcionado.

    Argumentos:
    imagen (array): Imagen a procesar.
    angulo (float): Ángulo de rotación en grados.

    Retorna:
    array: Imagen rotada.
    """
    rotada = ndimage.rotate(imagen, angulo, reshape=False)
    return rotada

# Función para voltear la imagen
def voltear_imagen(imagen, direccion):
    """
    Voltea la imagen vertical u horizontalmente.

    Argumentos:
    imagen (array): Imagen a procesar.
    direccion (int): 0 para vertical, 1 para horizontal.

    Retorna:
    array: Imagen volteada.
    """
    volteada = np.flip(imagen, axis=direccion)
    return volteada

# Función para cambiar el tamaño de la imagen
def cambiar_tamano(imagen, nuevo_tamano):
    """
    Cambia el tamaño de la imagen.

    Argumentos:
    imagen (array): Imagen a procesar.
    nuevo_tamano (tuple): Tupla con las dimensiones del 
    nuevo tamaño (ancho, alto).

    Retorna:
    array: Imagen redimensionada.
    """
    redimensionada = np.array(Image.fromarray(imagen).resize(nuevo_tamano))
    return redimensionada

# Función para invertir los colores de la imagen
def invertir_colores(imagen):
    """
    Invierte los colores de la imagen.

    Argumentos:
    imagen (array): Imagen a procesar.

    Retorna:
    array: Imagen con colores invertidos.
    """
    invertida = np.invert(imagen)
    return invertida

# Función para binarizar la imagen
def binarizar_imagen(imagen, umbral):
    """
    Convierte la imagen en una imagen binaria según un umbral dado.

    Argumentos:
    imagen (array): Imagen a procesar.
    umbral (int): Valor del umbral para binarización.

    Retorna:
    array: Imagen binarizada.
    """
    binaria = imagen > umbral
    binaria = binaria.astype(np.uint8) * 255
    return binaria

def main():
    """
    Función principal que ejecuta la interfaz de usuario y maneja 
    las operaciones de procesamiento de imágenes.
    """

    st.title("Editor básico de imagenes")

    uploaded_file = st.file_uploader("Sube una imagen", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        imagen = np.array(Image.open(uploaded_file))
        st.image(imagen, caption="Imagen Original", use_column_width=True)

        funcionalidades = {
            "Desenfoque": aplicar_desenfoque,
            "Detección de Bordes": aplicar_deteccion_bordes,
            "Ajustar Brillo/Contraste": ajustar_brillo_contraste,
            "Rotar Imagen": rotar_imagen,
            "Voltear Imagen": voltear_imagen,
            "Cambiar Tamaño": cambiar_tamano,
            "Invertir Colores": invertir_colores,
            "Binarizar Imagen": binarizar_imagen
        }

        funcion_seleccionada = st.selectbox("Selecciona una función", list(funcionalidades.keys()))

        if funcion_seleccionada in ["Ajustar Brillo/Contraste", "Rotar Imagen", "Voltear Imagen"]:
            if funcion_seleccionada == "Ajustar Brillo/Contraste":
                brillo = st.slider("Brillo", 0.5, 1.5, 1.0, 0.05)
                contraste = st.slider("Contraste", 0.5, 1.5, 1.0, 0.05)
                imagen_procesada = funcionalidades[funcion_seleccionada](imagen, brillo, contraste)
                imagen_procesada = np.clip(imagen_procesada, 0.0, 1.0)  
                imagen_procesada = (255 * imagen_procesada).astype(np.uint8)  
            elif funcion_seleccionada == "Rotar Imagen":
                angulo_rotacion = st.slider("Ángulo de Rotación", -180.0, 180.0, 0.0)
                imagen_procesada = funcionalidades[funcion_seleccionada](imagen, angulo_rotacion)
            else:
                direccion_volteo = st.radio("Dirección de Volteo:", ("Vertical", "Horizontal"))
                direccion = 0 if direccion_volteo == "Vertical" else 1
                imagen_procesada = funcionalidades[funcion_seleccionada](imagen, direccion)
        elif funcion_seleccionada == "Cambiar Tamaño":
            nuevo_ancho = st.number_input("Nuevo ancho", value=imagen.shape[1])
            nueva_altura = st.number_input("Nueva altura", value=imagen.shape[0])
            nuevo_tamano = (nuevo_ancho, nueva_altura)
            imagen_procesada = funcionalidades[funcion_seleccionada](imagen, nuevo_tamano)
        elif funcion_seleccionada == "Binarizar Imagen":
            umbral = st.slider("Umbral de binarización", 0, 255, 128)
            imagen_procesada = funcionalidades[funcion_seleccionada](color.rgb2gray(imagen), umbral)
        elif funcion_seleccionada == "Desenfoque":
            sigma = st.slider("Valor de sigma", 0.1, 10.0, 3.0)
            imagen_procesada = funcionalidades[funcion_seleccionada](imagen, sigma)
        elif funcion_seleccionada == "Detección de Bordes":
            imagen_procesada = funcionalidades[funcion_seleccionada](imagen)
            imagen_procesada = color.gray2rgb(imagen_procesada) 
            imagen_procesada = np.clip(imagen_procesada, 0.0, 1.0)  
            imagen_procesada = (255 * imagen_procesada).astype(np.uint8)  
        elif funcion_seleccionada == "Invertir Colores":
            imagen_procesada = funcionalidades[funcion_seleccionada](imagen)

        st.image(imagen_procesada, caption=f"{funcion_seleccionada}", use_column_width=True)

        buffered = bytes_io.BytesIO()
        img_pil = Image.fromarray(imagen_procesada)
        img_pil.save(buffered, format="PNG")
        buffered.seek(0)
        b64 = base64.b64encode(buffered.read()).decode()
        href = f'<a href="data:file/png;base64,{b64}" download="imagen_procesada.png">Descargar \
        imagen procesada</a>'
        st.markdown(href, unsafe_allow_html=True)

        st.footer("Desarrollado por: Jerónimo Vásquez González" + "\n" + \
                 "Contacto: jevasquez@unal.edu.co)

if __name__ == "__main__":
    main()

