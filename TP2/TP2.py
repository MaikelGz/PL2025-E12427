import re
from collections import Counter, defaultdict

def guardar_compositores(compositores):
    with open("resultado.txt", "w", encoding="utf-8") as archivo:
        archivo.write("Compositores ordenados alfabéticamente:\n")
        for compositor in sorted(compositores):
            archivo.write(f"{compositor}\n")

def guardar_epocas(epocas):
    with open("resultado.txt", "a", encoding="utf-8") as archivo:
        archivo.write("\nObras totales en cada período:\n")
        for epoca, cantidad in epocas.items():
            archivo.write(f"{epoca}: {cantidad} obras\n")

def guardar_obras_por_epoca(obras_por_epoca):
    with open("resultado.txt", "a", encoding="utf-8") as archivo:
        archivo.write("\nObras ordenadas por período:\n")
        for epoca, obras in sorted(obras_por_epoca.items()):
            archivo.write(f"{epoca}:\n")
            for obra in sorted(obras):
                archivo.write(f"  - {obra}\n")

def analizar_csv(archivo):
    patron = re.compile(r'^([^;]*);(?:[^;]*;){2}([^;]*);([^;]*)')
    datos = parseador(archivo)
    
    compositores_unicos = set()
    conteo_epocas = Counter()
    obras_por_epoca = defaultdict(list)
    
    for item in datos:
        linea_completa = ";".join(item)
        coincidencia = patron.match(linea_completa)
        
        if coincidencia:
            titulo, epoca, autor = map(str.strip, coincidencia.groups())
            compositores_unicos.add(autor)
            conteo_epocas[epoca] += 1
            obras_por_epoca[epoca].append(titulo)
    
    guardar_compositores(compositores_unicos)
    guardar_epocas(conteo_epocas)
    guardar_obras_por_epoca(obras_por_epoca)

def parseador(ruta_archivo):
    datos_limpios = []
    linea_actual = []
    dentro_comillas = False
    
    with open(ruta_archivo, encoding="utf-8") as archivo:
        lineas = archivo.readlines()[1:]  
        
        for linea in lineas:
            linea = linea.strip()
            contenido_procesado = []
            
            for caracter in linea:
                if caracter == '"':
                    dentro_comillas = not dentro_comillas
                elif dentro_comillas and caracter == ';':
                    contenido_procesado.append(',')
                else:
                    contenido_procesado.append(caracter)
            
            linea_actual.append("".join(contenido_procesado))
            
            if not dentro_comillas:
                datos_limpios.append(" ".join(linea_actual))
                linea_actual.clear()
    
    return [registro.split(';') for registro in datos_limpios]

def main():
    archivo_csv = "obras.csv"
    analizar_csv(archivo_csv)
    print("Análisis completado. Resultados guardados en 'resultado.txt'.")

if __name__ == "__main__":
    main()
