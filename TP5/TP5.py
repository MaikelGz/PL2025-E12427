import json
from datetime import datetime

def cargar_stock():
    try:
        with open('stock.json', 'r', encoding='utf-8') as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return []

def guardar_stock(stock):
    with open('stock.json', 'w', encoding='utf-8') as archivo:
        json.dump(stock, archivo, ensure_ascii=False, indent=4)

def calcular_saldo(monedas):
    valores = {'2e':200, '1e':100, '50c':50, '20c':20, '10c':10, '5c':5, '2c':2, '1c':1}
    saldo = 0
    for moneda in monedas:
        saldo += valores.get(moneda, 0)
    return saldo

def listar_stock(stock):
    print("cod | nombre | cantidad | precio")
    print("-"*35)
    for prod in stock:
        print(f"{prod['cod']} | {prod['nombre']} | {prod['quant']} | {prod['precio']}€")


def maquina_vending():
    stock = cargar_stock()
    saldo = 0

    fecha = datetime.now().strftime("%Y-%m-%d")
    print(f"maq: {fecha}, Stock cargado, Estado atualizado.")
    print("maq: Buen dia. Estoy disponible para atender su pedido.")

    while True:
        comando = input(">> ").strip().upper()

        if comando == "LISTAR":
            listar_stock(stock)

        elif comando.startswith("MOEDA"):
            monedas = comando[5:].replace('.', '').split(',')
            monedas = [moneda.strip().lower() for moneda in monedas if moneda.strip()]
            saldo += calcular_saldo(monedas)
            euros, centimos = divmod(saldo, 100)
            print(f"maq: Saldo = {euros}e{centimos}c")

        elif comando.startswith("SELECIONAR"):
            cod_producto = comando.split()[1]
            producto = next((p for p in stock if p['cod'] == cod_producto), None)

            if producto:
                precio_cents = int(producto['precio']*100)
                if producto['quant'] > 0:
                    if saldo >= precio_cents:
                        saldo -= precio_cents
                        producto['quant'] -= 1
                        print(f'maq: Puedes retirar el produto dispensado "{producto["nombre"]}"')
                        print(f"maq: Saldo = {saldo//100}e{saldo%100}c")
                    else:
                        print("maq: Saldo insufuciente para satisfacer su pedido")
                        print(f"maq: Saldo = {saldo//100}e{saldo%100}c; Pedido = {precio_cents//100}e{precio_cents%100}c")
                else:
                    print("maq: Produto agotado.")
            else:
                print("maq: Produto inexistente.")

        elif comando.startswith("ADICIONAR"):
            datos = comando.split()
            cod, nombre, quant, precio = datos[1], datos[2], int(datos[3]), float(datos[4])
            producto = next((p for p in stock if p['cod'] == cod), None)

            if producto:
                producto['quant'] += quant
                producto['precio'] = precio
            else:
                stock.append({"cod":cod, "nombre":nombre, "quant":quant, "precio":precio})

            print("maq: Stock atualizado.")

        elif comando == "SAIR":
            troco = saldo
            monedas_saldo = []
            for valor, etiqueta in [(200,'2e'),(100,'1e'),(50,'50c'),(20,'20c'),(10,'10c'),(5,'5c'),(2,'2c'),(1,'1c')]:
                cantidad, troco = divmod(troco, valor)
                if cantidad > 0:
                    monedas_saldo.append(f"{cantidad}x {etiqueta}")

            print("maq: Pode retirar el producto: " + ', '.join(monedas_saldo) + '.')
            guardar_stock(stock)
            print("maq: Hasta la proxima")
            break

        else:
            print("maq: Comando no reconocido.")


if __name__ == "__main__":
    maquina_vending()