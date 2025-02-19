def sumador_texto(texto):
    suma = 0
    activo = True  
    
    i = 0
    while i < len(texto):
        char = texto[i]
        
        if texto[i:i+2].lower() == "on":
            activo = True
            i += 2
            continue
        elif texto[i:i+3].lower() == "off":
            activo = False
            i += 3
            continue

        if char.isdigit():
            num = ""
            while i < len(texto) and texto[i].isdigit():
                num += texto[i]
                i += 1
            if activo:
                suma += int(num)
            continue 
        
        if char == "=":
            print(suma)
        
        i += 1
    
    print(suma)  

def main():
    try:
        with open("entrada.txt", "r", encoding="utf-8") as file:
            sumador_texto(file.read())
    except FileNotFoundError:
        print("Error: No se encontró el archivo 'entrada.txt'.")

if __name__ == "__main__":
    main()
