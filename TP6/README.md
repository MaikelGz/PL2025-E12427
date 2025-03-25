# TPC6 - Recursivo Descendente LL(1) para expresiones aritméticas

## Descripción
Este programa implementa un parser LL(1) recursivo descendente en Python usando la biblioteca `ply.lex` para reconocer y calcular el valor de expresiones aritméticas. Las expresiones pueden incluir números enteros, paréntesis y las operaciones básicas: suma, resta, multiplicación y división.

Las características del programa son:

- **Análisis léxico**: utiliza `ply.lex` para identificar tokens (números, operadores y paréntesis).
- **Parser LL(1)**: implementado mediante funciones recursivas (`expr`, `term` y `factor`) que gestionan la precedencia de operadores.
- **Evaluación inmediata**: calcula directamente el valor numérico de las expresiones introducidas.
- **Manejo de errores**: detecta y reporta errores sintácticos (tokens inesperados) y errores aritméticos (como división por cero).

---

## Ejecución

Para ejecutar el programa, asegúrate de tener:
- Python instalado.
- La biblioteca `ply` instalada (`pip install ply`).

Guarda el script Python (por ejemplo: `TP6.py`) y ejecuta desde terminal:

```sh
$ python TP6.py
```

---

## Estructura del Algoritmo

El programa sigue la siguiente estructura lógica:

1. **Definición de tokens**: especifica los tokens básicos reconocibles por el lexer (`NUMBER`, `PLUS`, `MINUS`, `TIMES`, `DIVIDE`, `LPAREN`, `RPAREN`).
2. **Funciones de tokens**: asocia patrones regulares a cada token.
3. **Análisis léxico con PLY**: genera el lexer con `ply.lex`.
4. **Parser LL(1)**: implementado mediante las funciones:
   - `expr()`: maneja la suma y resta.
   - `term()`: maneja multiplicación y división.
   - `factor()`: maneja números y expresiones agrupadas en paréntesis.
5. **Evaluación de expresiones**: parsea y calcula directamente el resultado.
6. **Manejo de errores**: incluye excepciones para tokens incorrectos o errores matemáticos (división por cero).

---

## Ejemplo de uso

A continuación se muestra un ejemplo práctico del resultado de ejecutar el programa con algunas expresiones aritméticas:

![LexPython](https://github.com/user-attachments/assets/3dfe02d9-0c90-4944-97dd-25ffea2da8f7)


---

## Autor
- **Nombre:** Mikel Gonzalez Rodriguez  
- **ID:** E12427  
- **Foto:**  
![FotoDNI](https://github.com/user-attachments/assets/89f3adbe-49b9-4930-808f-9d0bc81bcb00)
