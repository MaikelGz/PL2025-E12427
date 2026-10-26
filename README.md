# Procesamiento de Lenguajes — PL2025

Contiene seis trabajos prácticos independientes y una implementación evolutiva de un compilador para un subconjunto de Pascal, desarrollados principalmente en Python.

## Contenido

| Directorio | Componente | Entrada principal | Salida o efecto |
| --- | --- | --- | --- |
| [`TP1`](TP1/README.md) | Sumador con control `on`/`off` | `entrada.txt` | Muestra acumulados al encontrar `=` y al final |
| [`TP2`](TP2/README.md) | Análisis de catálogo de obras musicales | `obras.csv` | `resultado.txt` |
| [`TP3`](TP3/README.md) | Conversión Markdown a HTML | `entrada.md` | `salida.html` |
| [`TP4`](TP4/README.md) | Lexer para consultas de estilo SPARQL | `entrada.txt` | `resultado.txt` |
| [`TP5`](TP5/README.md) | Máquina expendedora interactiva | `stock.json` | Actualiza `stock.json` al salir |
| [`TP6`](TP6/README.md) | Lexer y parser LL(1) de expresiones aritméticas | Expresiones incluidas en el script | Muestra resultados en consola |
| [`Projeto_Compilador`](Projeto_Compilador/README.md) | Compilador de subconjunto de Pascal | `programa_pascalN.pas` | `codigo_ensamblador.asm` |

Los README de cada directorio describen su práctica con más detalle. Los scripts se ejecutan de forma independiente: no existe un punto de entrada común ni una aplicación integrada.

## Requisitos

- Python 3.
- `ply` para las prácticas TP4, TP6 y el proyecto de compilador.

Instalación de la dependencia:

```bash
python -m pip install ply
```

TP1, TP2, TP3 y TP5 utilizan módulos de la biblioteca estándar de Python. No se incluye un archivo de dependencias común; PLY debe instalarse en el entorno desde el que se ejecuten los scripts que lo requieren.

## Puesta en marcha

Cada práctica se inicia desde su propio directorio, ya que los programas abren sus archivos de datos con rutas relativas al directorio de trabajo actual. Por ejemplo:

```bash
cd TP1
python TP1.py
```

Para compilar un programa Pascal:

```bash
cd Projeto_Compilador
python Lex7.py
```

El compilador solicita el número del ejemplo, carga `programa_pascalN.pas` y escribe el resultado en `codigo_ensamblador.asm` cuando el análisis termina sin errores. Los ejemplos incluidos están numerados del 0 al 5.

## Descripción técnica

### TP1 — Sumador textual

`sumador_texto` recorre el texto carácter a carácter. Reconoce secuencias de dígitos como enteros y mantiene un estado de suma activada o desactivada al detectar las cadenas `on` y `off` sin distinguir mayúsculas. Mientras la suma está activada acumula los números; cada `=` provoca la impresión del total parcial. Al acabar imprime también el total final. La entrada se lee de `entrada.txt` en UTF-8.

### TP2 — Catálogo de obras musicales

El programa procesa registros delimitados por punto y coma sin utilizar el módulo `csv`. `parseador` conserva registros que pueden abarcar varias líneas entre comillas y sustituye los separadores internos de esos campos por comas. Después, una expresión regular extrae título, período y autor de las columnas esperadas. Se construyen autores únicos, recuentos por período y listas de títulos, y se escriben en `resultado.txt`. El formato y orden de columnas deben corresponder al patrón utilizado por el script.

### TP3 — Markdown a HTML

`conversor_md_html` aplica reglas de expresiones regulares línea por línea para convertir encabezados de nivel 1 a 3, negrita, cursiva, imágenes, enlaces y elementos numerados. Agrupa líneas consecutivas de lista en etiquetas `<ol>`. Lee `entrada.md` y genera `salida.html`. Es un conversor didáctico de una selección de sintaxis, no una implementación completa de Markdown ni un sanitizador HTML.

### TP4 — Analizador léxico de consultas

El lexer se construye con `ply.lex` y reconoce palabras clave de consulta, variables con `?`, recursos con prefijos `dbo:` y `foaf:`, cadenas opcionalmente etiquetadas con idioma, números enteros, el término `a`, llaves y puntos. Omite espacios, tabuladores y saltos de línea; descarta comentarios que comienzan por `#` e informa de caracteres ilegales. El archivo `entrada.txt` se transforma en una secuencia de registros `tipo, valor, posición` en `resultado.txt`. No valida la sintaxis ni la semántica de la consulta.

### TP5 — Máquina expendedora

La aplicación mantiene en memoria una lista de productos cargada de `stock.json`, con campos `cod`, `nombre`, `quant` y `precio`. El bucle de comandos admite `LISTAR`, `MOEDA`, `SELECIONAR <código>`, `ADICIONAR <código> <nombre> <cantidad> <precio>` y `SAIR`. El saldo se representa en céntimos y las monedas aceptadas son `2e`, `1e`, `50c`, `20c`, `10c`, `5c`, `2c` y `1c`. Las compras reducen cantidad y saldo; la salida calcula una descomposición del saldo restante en monedas y persiste el inventario JSON. Si no encuentra el JSON, inicia con el inventario vacío.

### TP6 — Evaluador de expresiones LL(1)

`ply.lex` identifica enteros, operadores `+`, `-`, `*`, `/` y paréntesis. La clase `Parser` implementa descenso recursivo mediante `expr`, `term` y `factor`, lo que da prioridad a multiplicación y división frente a suma y resta, y permite agrupar con paréntesis. Detecta caracteres ilegales, tokens inesperados y división por cero. El script evalúa una colección de ejemplos definida en el propio archivo; no implementa un bucle de entrada interactiva.

### Proyecto de compilador Pascal

`Projeto_Compilador/Lex7.py` reúne las fases principales del compilador:

1. **Análisis léxico:** `ply.lex` reconoce palabras reservadas, identificadores, números, cadenas entre comillas simples, operadores y delimitadores.
2. **Análisis sintáctico:** `ply.yacc` valida la gramática implementada y construye una representación de nodos (AST) para bloques, declaraciones, expresiones y sentencias.
3. **Información semántica:** una tabla de símbolos asigna índices de memoria y almacena tipos; se comprueban algunos usos no válidos, como identificadores no declarados, operaciones de longitud con tipos incompatibles y accesos indexados.
4. **Generación:** un recorrido del AST emite instrucciones tipo ensamblador de pila para una máquina virtual, con operaciones aritméticas, lectura/escritura, etiquetas, saltos y acceso a arrays/cadenas.

El subconjunto implementado incluye declaraciones `integer`, `boolean`, `string` y arrays; asignaciones; expresiones aritméticas, relacionales y lógicas; `if`/`else`, `while`, `for ... to` y `for ... downto`; `readln`, `write`, `writeln`; indexación y `length` sobre cadenas. El artefacto generado es código para una máquina virtual, no código máquina nativo ni un ejecutable independiente. Aunque el enunciado menciona subprogramas como opción, el script principal no implementa una gramática completa de `procedure` y `function`.

`Lex3.py` a `Lex6.py` reflejan versiones intermedias de evolución del lexer/parser. `Lex7.py` es la implementación principal descrita y ejecutada por el README del proyecto. `programa_pascal0.pas` a `programa_pascal5.pas` sirven como programas de muestra. También hay salidas y tablas auxiliares generadas por PLY (`parsetab.py`, `parser.out`) y materiales del enunciado; no son puntos de entrada alternativos.

## Archivos de ejemplo y resultados versionados

Los directorios de las prácticas contienen archivos de entrada de muestra y, en algunos casos, resultados guardados en el repositorio. Al ejecutar los programas, los archivos de salida con nombre fijo pueden sobrescribirse. En particular, TP2 y TP4 escriben ambos un archivo llamado `resultado.txt`, pero en directorios distintos.

