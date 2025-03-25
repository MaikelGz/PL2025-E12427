# TPC5 - Máquina Vending

## Descripción
Este programa implementa una máquina expendedora (vending) en Python, usando JSON para almacenar y actualizar el stock disponible. Permite realizar las siguientes operaciones:

- **Cargar stock desde un archivo JSON**: `stock.json`.
- **Guardar stock actualizado**: al finalizar la sesión, guarda automáticamente en el mismo archivo JSON.
- **Introducir monedas**: reconoce monedas de euros y céntimos (ej.: `1e`, `50c`).
- **Seleccionar productos**: permite elegir productos mediante un código, gestionando saldos, disponibilidad y precios.
- **Añadir o actualizar productos**: permite agregar nuevos productos o modificar los existentes.
- **Devolver cambio**: calcula y devuelve el cambio exacto al usuario al terminar la sesión.

---

## Ejecución
Para ejecutar el programa, asegúrate de tener en el mismo directorio:
- El archivo `stock.json` (contiene el stock inicial).
- El script Python con el nombre deseado (por ejemplo: `TP5.py`).

Ejecuta con:

```sh
$ python TP5.py
```

---

## Estructura del Algoritmo
El programa sigue los siguientes pasos:

1. **Cargar stock inicial**: lee productos desde `stock.json`.
2. **Inicio del programa**: muestra saludo inicial y fecha actual.
3. **Lectura de comandos**:
   - **LISTAR**: muestra el stock disponible.
   - **MOEDA**: introduce monedas para aumentar el saldo.
   - **SELECIONAR**: selecciona un producto, verificando saldo y stock.
   - **ADICIONAR**: agrega o actualiza productos en el stock.
   - **SAIR**: termina la interacción, devuelve cambio y actualiza stock.
4. **Actualización de stock**: guarda los cambios en `stock.json` al finalizar.

---

## Ejemplo de uso

A continuación se muestra un ejemplo práctico de interacción con la máquina:

![UsoMaquinaPython](https://github.com/user-attachments/assets/7c1123dd-db72-45ff-8f8e-67cc4adf4ad2)


---

## Autor
- **Nombre:** Mikel Gonzalez Rodriguez  
- **ID:** E12427  
- **Foto:**  
![FotoDNI](https://github.com/user-attachments/assets/89f3adbe-49b9-4930-808f-9d0bc81bcb00)
