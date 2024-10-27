import json
import random
import time
import math
import argparse

EF_INICIAL = 2.5  # Factor de facilidad inicial

class Pregunta:
    def __init__(self, data):
        self.id = data['id']
        self.pregunta = data['pregunta']
        self.opciones = data['opciones']
        self.respuesta_correcta = data['respuesta_correcta']
        self.EF = EF_INICIAL  # Factor de facilidad inicial
        self.intervalo = 0
        self.repeticion = 0
        self.proxima_revision = time.time()

def cargar_preguntas(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return [Pregunta(item) for item in data]

def guardar_estado(preguntas, filename):
    data = []
    for pregunta in preguntas:
        data.append({
            'id': pregunta.id,
            'pregunta': pregunta.pregunta,
            'opciones': pregunta.opciones,
            'respuesta_correcta': pregunta.respuesta_correcta,
            'EF': pregunta.EF,
            'intervalo': pregunta.intervalo,
            'repeticion': pregunta.repeticion,
            'proxima_revision': pregunta.proxima_revision
        })
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def calcular_EF(EF, calidad):
    EF = EF + (0.1 - (5 - calidad) * (0.08 + (5 - calidad) * 0.02))
    if EF < 1.3:
        EF = 1.3
    return EF

def supermemo2(pregunta, calidad):
    if calidad < 3:
        pregunta.repeticion = 0
        pregunta.intervalo = 1
    else:
        if pregunta.repeticion == 0:
            pregunta.intervalo = 1
        elif pregunta.repeticion == 1:
            pregunta.intervalo = 6
        else:
            pregunta.intervalo = pregunta.intervalo * pregunta.EF
        pregunta.EF = calcular_EF(pregunta.EF, calidad)
        pregunta.repeticion += 1
    pregunta.proxima_revision = time.time() + pregunta.intervalo * 86400  # Convertir días a segundos

def seleccionar_preguntas(preguntas):
    ahora = time.time()
    disponibles = [p for p in preguntas if p.proxima_revision <= ahora]
    if not disponibles:
        print("No hay preguntas para revisar ahora. ¡Buen trabajo!")
        return []
    random.shuffle(disponibles)
    return disponibles[:5]  # Selecciona hasta 5 preguntas

def handle_self_assessment_question(pregunta):
    print("\n" + pregunta.pregunta)
    print("\n1. I knew the answer")
    print("2. I did not know the answer")
    
    respuesta_usuario = int(input("Your response (1 or 2): "))
    
    if respuesta_usuario == 1:
        print("¡Great!")
        calidad = 5  # High quality for known answers
        return True, calidad
    else:
        print("Keep studying!")
        calidad = 2  # Low quality for unknown answers
        return False, calidad

def main():
    parser = argparse.ArgumentParser(description='SRE Learning System')
    parser.add_argument('--self-assessment', action='store_true', 
                       help='Enable self-assessment mode without multiple choice')
    args = parser.parse_args()

    print("\nTip: Press Ctrl+C or type 'q' at any prompt to exit")
    preguntas = cargar_preguntas('preguntas.json')
    
    try:
        while True:
            preguntas_a_revisar = seleccionar_preguntas(preguntas)
            if not preguntas_a_revisar:
                break
            
            random.shuffle(preguntas_a_revisar)
            for pregunta in preguntas_a_revisar:
                print("\n" + pregunta.pregunta)
                
                if args.self_assessment:
                    print("\n1. I knew the answer")
                    print("2. I did not know the answer")
                    respuesta = input("Your response (1 or 2, or 'q' to quit): ").lower()
                    if respuesta == 'q':
                        raise KeyboardInterrupt
                    respuesta_usuario = int(respuesta)
                    
                    if respuesta_usuario == 1:
                        print("¡Great!")
                        calidad = 5
                    else:
                        print(f"The correct answer was: {pregunta.opciones[pregunta.respuesta_correcta]}")
                        calidad = 2
                else:
                    for idx, opcion in enumerate(pregunta.opciones):
                        print(f"{idx + 1}. {opcion}")
                    respuesta = input("Tu respuesta (número, o 'q' para salir): ").lower()
                    if respuesta == 'q':
                        raise KeyboardInterrupt
                    respuesta_usuario = int(respuesta) - 1
                    
                    if respuesta_usuario == pregunta.respuesta_correcta:
                        print("¡Correcto!")
                        calidad = 5
                    else:
                        print(f"Incorrecto. La respuesta correcta era: {pregunta.opciones[pregunta.respuesta_correcta]}")
                        calidad = 2
                
                supermemo2(pregunta, calidad)
            
            guardar_estado(preguntas, 'estado_preguntas.json')
            continuar = input("\n¿Deseas continuar? (s/n): ").lower()
            if continuar != 's':
                break
                
    except (KeyboardInterrupt, EOFError):
        print("\n\nGuardando progreso...")
    except ValueError:
        print("\n\nEntrada inválida. Guardando progreso...")
    finally:
        guardar_estado(preguntas, 'estado_preguntas.json')
        print("¡Hasta luego!")

if __name__ == "__main__":
    main()
