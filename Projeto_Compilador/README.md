# Compilador Pascal con Lex y Yacc (PLY)

Este proyecto implementa un compilador simple para un subconjunto del lenguaje Pascal utilizando **PLY** (Python Lex-Yacc). El archivo principal del proyecto es `Lex7.py`, que contiene el analizador léxico, el analizador sintáctico, el verificador semántico y el generador de código.

## 📄 ¿Cómo funciona?

El script `Lex7.py` realiza las siguientes tareas principales:

### 1. **Análisis Léxico**
El compilador utiliza `ply.lex` para tokenizar el código fuente en Pascal. Soporta:
- Palabras clave de Pascal (`program`, `begin`, `end`, `var`, etc.)
- Identificadores
- Números
- Cadenas de texto
- Operadores (`+`, `-`, `*`, `div`, `mod`, etc.)
- Símbolos (`:=`, `;`, `()`, `[]`, etc.)

### 2. **Análisis Sintáctico (Parsing)**
El parser está implementado con `ply.yacc` y soporta:
- Declaraciones de variables (incluyendo arrays y strings)
- Estructuras de control (`if`, `while`, `for`, incluyendo `downto`)
- Entrada/Salida (`readln`, `write`, `writeln`)
- Expresiones y condiciones
- Operaciones con strings (por ejemplo, `length()`)

La gramática construye un Árbol de Sintaxis Abstracta (AST) durante el análisis.

### 3. **Tabla de Símbolos**
Se mantiene una tabla de símbolos para registrar las variables declaradas, sus tipos e índices de memoria. También se maneja la información de arrays y cadenas.

### 4. **Generación de Código**
Se recorre el AST para generar un código en pseudo-ensamblador basado en pila para una máquina virtual. Se soportan operaciones como:
- Expresiones aritméticas y lógicas
- Control de flujo con etiquetas y saltos
- Operaciones de lectura y escritura
- Indexación de arrays y cadenas
- Funciones incorporadas como `length`

### 5. **Ejecución**
Para ejecutar el compilador:
```bash
python Lex7.py
```
Solicitará un número que corresponde a un archivo fuente Pascal llamado `programa_pascalN.pas` (por ejemplo, `programa_pascal1.pas`).

Tras el análisis y generación exitosos, el código se guarda en:
```
codigo_ensamblador.asm
```

## 📁 Estructura de Archivos

- `Lex7.py`: Script principal del compilador.
- `programa_pascalN.pas`: Archivos fuente en Pascal para compilar.
- `codigo_ensamblador.asm`: Archivo de salida con el código pseudo-ensamblador generado.

## ✅ Requisitos

- Python 3.x
- [PLY](https://www.dabeaz.com/ply/)

Instalar PLY con:
```bash
pip install ply
```

## 🛠️ Notas

- Se incluye manejo de errores de sintaxis y algunos errores semánticos (por ejemplo, variables no declaradas, límites de arrays inválidos).
- Se manejan cadenas y arrays con indexación y verificación de longitud.
- Este proyecto es ideal para fines educativos y para estudiar los fundamentos del diseño de compiladores.

---
