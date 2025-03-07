# TPC3 - Conversor de MarkDown a HTML

## Descripción
Este programa convierte un archivo en formato Markdown a HTML, procesando los elementos básicos de la sintaxis Markdown. Transforma:
- Encabezados (`#`, `##`, `###`) en sus equivalentes HTML (`<h1>`, `<h2>`, `<h3>`).
- Texto en **negrita** (`**texto**`) en `<b>texto</b>`.
- Texto en *cursiva* (`*texto*`) en `<i>texto</i>`.
- Listas numeradas en listas HTML (`<ol><li>elemento</li></ol>`).
- Enlaces `[texto](URL)` en `<a href="URL">texto</a>`.
- Imágenes `![texto alternativo](URL)` en `<img src="URL" alt="texto alternativo"/>`.

El archivo de entrada debe estar correctamente formateado para garantizar una conversión sin errores.

---

## Ejecución
Para ejecutar el programa, asegúrate de que los siguientes archivos estén en la misma carpeta:
- Un archivo `entrada.md` que contenga el texto en formato Markdown.
- El script `TP3	.py`.

Ejecuta el programa con el siguiente comando:
```sh
$ python TP3.py
```

El resultado se guardará en un archivo `salida.html` en la misma carpeta.

---

## Estructura del Algoritmo
El programa sigue las siguientes etapas:
1. **Lectura del archivo Markdown** - Abre y lee el contenido de `entrada.md`.
2. **Conversión a HTML** - Utiliza expresiones regulares para detectar y transformar:
   - Encabezados (`#`, `##`, `###`).
   - Texto en negrita (`**texto**`).
   - Texto en cursiva (`*texto*`).
   - Listas numeradas (`1. item` → `<ol><li>item</li></ol>`).
   - Enlaces y imágenes en sus equivalentes HTML.
3. **Guardado del resultado** - Genera y escribe el contenido HTML en `salida.html`.

---

## Autor
- **Nombre:** Mikel Gonzalez Rodriguez  
- **ID:** E12427  
- **Foto:**  
![FotoDNI](https://github.com/user-attachments/assets/89f3adbe-49b9-4930-808f-9d0bc81bcb00)
