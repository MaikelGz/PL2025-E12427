import re
import os

def conversor_md_html(md_text):
    reglas = [
         (r'^(#{1})\s+(.+)', r'<h1>\2</h1>'),  # Encabezado H1
        (r'^(#{2})\s+(.+)', r'<h2>\2</h2>'),  # Encabezado H2
        (r'^(#{3})\s+(.+)', r'<h3>\2</h3>'),  # Encabezado H3
        (r'\*\*(.*?)\*\*', r'<b>\1</b>'),  # Negrita
        (r'\*(.*?)\*', r'<i>\1</i>'),  # Cursiva
        (r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1"/>'),  # Imagen
        (r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>'),  # Enlace
        (r'^\d+\.\s*(.+)', r'<li>\1</li>')  # Elementos de lista numerada
    ]

    lineas = md_text.split('\n')
    html_lineas = []
    lista_abierta = False

    for linea in lineas:
        for patron, reemplazo in reglas:
                linea = re.sub(patron, reemplazo, linea)
     
        if linea.startswith('<li>'):
            if not lista_abierta:
                html_lineas.append('<ol>')  
                lista_abierta = True
            html_lineas.append(linea)
        else:
            if lista_abierta:
                html_lineas.append('</ol>')  
                lista_abierta = False
            html_lineas.append(linea)

    if lista_abierta:
        html_lineas.append('</ol>')  

    return '\n'.join(html_lineas)


def main():
    archivo_md = "entrada.md"
    archivo_html= "salida.html"

    if not os.path.exists(archivo_md):
        print(f"Error: No se encontró el archivo '{archivo_md}' en el directorio actual.")
        return

    try:
        with open(archivo_md, 'r', encoding='utf-8') as f:
            contenido_md = f.read()

        contenido_html = conversor_md_html(contenido_md)

        with open(archivo_html, 'w', encoding='utf-8') as f:
            f.write(contenido_html)

        print(f"Conversión completada: El archivo '{archivo_html}' ha sido generado.")

    except Exception as e:
        print(f"Error: {e}")

        


if __name__=="__main__":
    main()