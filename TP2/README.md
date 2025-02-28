# TPC2 - Análise de um dataset de obras musicais 

## Descripción
Este programa analiza un dataset que contiene información sobre obras musicales. Procesa los datos para generar:
- Una lista ordenada alfabéticamente de los compositores musicales.
- La distribución de las obras por período, mostrando la cantidad de obras catalogadas en cada uno.
- Un diccionario que asocia cada período con una lista alfabética de los títulos de las obras correspondientes.

Para garantizar un procesamiento correcto, está prohibido el uso del módulo `csv` de Python. El archivo de entrada debe estar correctamente formateado y sin errores en la separación de campos.

---

## Ejecución
Para ejecutar el programa, asegúrate de que los siguientes archivos estén en la misma carpeta:
- Un archivo `obras.csv` que contenga los datos de las obras musicales.
- El script `analisis_obras.py`.

Ejecuta el programa con el siguiente comando:
```sh
$ python analisis_obras.py
```

El resultado del análisis se guardará en el archivo `resultado.txt`.

---

## Estructura del Algoritmo
El programa sigue las siguientes etapas:
1. **Lectura del archivo CSV** - Procesa el archivo ignorando la primera línea (encabezado) y manejando los campos entre comillas.
2. **Extracción de información** - Utiliza expresiones regulares para capturar los campos relevantes: título de la obra, período y compositor.
3. **Organización de los datos**:
   - Genera una lista de compositores ordenados alfabéticamente.
   - Cuenta cuántas obras pertenecen a cada período.
   - Crea un diccionario que relaciona los períodos con los títulos de las obras, ordenados alfabéticamente.
4. **Guardado de los resultados** - La información procesada se almacena en el archivo `resultado.txt`.

---

## Autor
- **Nombre:** Mikel Gonzalez Rodriguez  
- **ID:** E12427  
- **Foto:**  
![FotoDNI](https://github.com/user-attachments/assets/89f3adbe-49b9-4930-808f-9d0bc81bcb00)
