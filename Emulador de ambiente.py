import json
import random

# Clase base para todas las especies
class Especie:
    def __init__(self, nombre, tipo, capacidad_reproduccion):
        self.nombre = nombre
        self.tipo = tipo
        self.capacidad_reproduccion = capacidad_reproduccion
        self.poblacion = 1

    def reproducirse(self):
        # Fórmula de reproducción
        incremento = self.poblacion * self.capacidad_reproduccion
        self.poblacion += int(incremento)

# Clase Planta, hereda de Especie
class Planta(Especie):
    def __init__(self, nombre, capacidad_reproduccion):
        super().__init__(nombre, "planta", capacidad_reproduccion)

# Clase Animal, base para Herbivoros y Carnivoros
class Animal(Especie):
    def __init__(self, nombre, tipo, capacidad_reproduccion, capacidad_busqueda, velocidad_digestion):
        super().__init__(nombre, tipo, capacidad_reproduccion)
        self.capacidad_busqueda = capacidad_busqueda
        self.velocidad_digestion = velocidad_digestion

    def buscar_alimento(self):
        # Método genérico de búsqueda de alimento
        return self.capacidad_busqueda * self.velocidad_digestion

# Herbivoro hereda de Animal
class Herbivoro(Animal):
    def __init__(self, nombre, capacidad_reproduccion, capacidad_busqueda, velocidad_digestion):
        super().__init__(nombre, "herbivoro", capacidad_reproduccion, capacidad_busqueda, velocidad_digestion)

# Carnivoro hereda de Animal
class Carnivoro(Animal):
    def __init__(self, nombre, capacidad_reproduccion, capacidad_busqueda, velocidad_digestion, tasa_efectividad_caza):
        super().__init__(nombre, "carnivoro", capacidad_reproduccion, capacidad_busqueda, velocidad_digestion)
        self.tasa_efectividad_caza = tasa_efectividad_caza

    def buscar_alimento(self):
        # Carnivoro tiene en cuenta la tasa de efectividad de caza
        return self.capacidad_busqueda * self.tasa_efectividad_caza * self.velocidad_digestion

# Clase Ecosistema para manejar las interacciones
class Ecosistema:
    def __init__(self):
        self.plantas = []
        self.herbivoros = []
        self.carnivoros = []

    def agregar_especie(self, especie):
        if isinstance(especie, Planta):
            self.plantas.append(especie)
        elif isinstance(especie, Herbivoro):
            self.herbivoros.append(especie)
        elif isinstance(especie, Carnivoro):
            self.carnivoros.append(especie)

    def simular_dia(self):
        # Reproducción de plantas
        for planta in self.plantas:
            planta.reproducirse()

        # Alimentación y reproducción de herbívoros
        for herbivoro in self.herbivoros:
            alimento_disponible = sum([planta.poblacion for planta in self.plantas])
            alimento_consumido = alimento_disponible * herbivoro.capacidad_busqueda * herbivoro.velocidad_digestion
            if alimento_consumido > 0:
                herbivoro.reproducirse()
            else:
                herbivoro.poblacion *= 0.9  # Mortalidad si no se alimenta

        # Alimentación y reproducción de carnívoros
        for carnivoro in self.carnivoros:
            presas_disponibles = sum([herbivoro.poblacion for herbivoro in self.herbivoros])
            alimento_consumido = presas_disponibles * carnivoro.capacidad_busqueda * carnivoro.tasa_efectividad_caza * carnivoro.velocidad_digestion
            if alimento_consumido > 0:
                carnivoro.reproducirse()
            else:
                carnivoro.poblacion *= 0.9  # Mortalidad si no se alimenta

    def guardar_ecosistema(self, archivo):
        # Guardar en formato JSON
        data = {
            "plantas": [planta.__dict__ for planta in self.plantas],
            "herbivoros": [herbivoro.__dict__ for herbivoro in self.herbivoros],
            "carnivoros": [carnivoro.__dict__ for carnivoro in self.carnivoros]
        }
        with open(archivo, 'w') as file:
            json.dump(data, file)

    def cargar_ecosistema(self, archivo):
        # Cargar datos desde un archivo JSON
        with open(archivo, 'r') as file:
            data = json.load(file)
            for p in data['plantas']:
                planta = Planta(p['nombre'], p['capacidad_reproduccion'])
                planta.poblacion = p['poblacion']
                self.plantas.append(planta)
            for h in data['herbivoros']:
                herbivoro = Herbivoro(h['nombre'], h['capacidad_reproduccion'], h['capacidad_busqueda'], h['velocidad_digestion'])
                herbivoro.poblacion = h['poblacion']
                self.herbivoros.append(herbivoro)
            for c in data['carnivoros']:
                carnivoro = Carnivoro(c['nombre'], c['capacidad_reproduccion'], c['capacidad_busqueda'], c['velocidad_digestion'], c['tasa_efectividad_caza'])
                carnivoro.poblacion = c['poblacion']
                self.carnivoros.append(carnivoro)
