# TPC4 - Analizador Léxico

## Descripción
Este programa implementa un analizador léxico para procesar consultas en un lenguaje similar a SPARQL. Se encarga de tokenizar elementos como palabras clave, variables, identificadores, números y símbolos especiales. Los tokens reconocidos incluyen:

- **Palabras clave**: `SELECT`, `WHERE`, `LIMIT`, `FILTER`, `OPTIONAL`, `ORDER BY`, `GROUP BY`.
- **Variables**: Identificadores que comienzan con `?`, como `?nombre` o `?edad`.
- **Identificadores de recursos (IRI)**: Prefijos como `dbo:` o `foaf:` seguidos de un nombre.
- **Cadenas de texto**: Texto encerrado entre comillas (`"texto"@en`).
- **Números**: Secuencias de dígitos enteros (`1000`).
- **Tipos**: La palabra `a`, utilizada en consultas RDF.
- **Símbolos especiales**: `{`, `}`, `.` (llaves y punto).
- **Comentarios**: Líneas que comienzan con `#` y son ignoradas por el lexer.

El programa lee una consulta desde un archivo de entrada, la procesa con el analizador léxico y guarda los tokens resultantes en un archivo de salida.

---

## Ejecución
Para ejecutar el programa, asegúrate de que los siguientes archivos estén en la misma carpeta:
- Un archivo `entrada.txt` con la consulta a analizar.
- El script `TP4.py` (nombre del archivo del analizador léxico).

Ejecuta el programa con el siguiente comando:
```sh
$ python TP4.py
```
El resultado se guardará en `resultado.txt`, mostrando los tokens con su tipo, valor, número de línea y posición en el texto.

---

## Estructura del Algoritmo
El programa sigue las siguientes etapas:
1. **Definición de tokens**: Se especifican los tipos de tokens, incluyendo palabras clave, identificadores, operadores y literales.
2. **Expresiones regulares**: Se utilizan patrones para identificar cada tipo de token.
3. **Manejo de espacios y errores**: Se ignoran espacios en blanco y se detectan caracteres no válidos.
4. **Construcción del lexer**: Se usa `ply.lex` para generar el analizador.
5. **Lectura del archivo de entrada**: Se carga el texto desde `entrada.txt`.
6. **Procesamiento de tokens**: Se ejecuta el lexer y se generan los tokens.
7. **Escritura del resultado**: Se guardan los tokens en `resultado.txt`.

---

## Autor
- **Nombre:** Mikel Gonzalez Rodriguez  
- **ID:** E12427  
- **Foto:**  
![FotoDNI](https://github.com/user-attachments/assets/89f3adbe-49b9-4930-808f-9d0bc81bcb00)

