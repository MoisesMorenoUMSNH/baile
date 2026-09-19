import math
import src.SimpleSearch as sp

class CiudadTaxi:
    def __init__(self, ancho, alto, obstaculos, pos_pasajero, pos_destino):
        self.ancho = ancho
        self.alto = alto
        self.obstaculos = frozenset(obstaculos)
        self.pos_pasajero = pos_pasajero
        self.pos_destino = pos_destino

    def es_valida(self, x, y):
        # Validamos que la casilla esté dentro del mapa y no sea un obstáculo
        return 0 <= x < self.ancho and 0 <= y < self.alto and (x, y) not in self.obstaculos

    def sucesor(self, nodo):
        # Generamos los estados siguientes a partir del estado actual: ((x, y), lleva_pasajero)
        hijos = []
        (x, y), lleva_pasajero = nodo.state

        movimientos = [
            ((0, 1), "Arriba"),
            ((0, -1), "Abajo"),
            ((-1, 0), "Izquierda"),
            ((1, 0), "Derecha")
        ]

        for (dx, dy), accion in movimientos:
            nuevo_x, nuevo_y = x + dx, y + dy

            if self.es_valida(nuevo_x, nuevo_y):
                # El pasajero está a bordo si ya lo llevaba o si llega a su posición
                nuevo_lleva_pasajero = lleva_pasajero or ((nuevo_x, nuevo_y) == self.pos_pasajero)
                nuevo_estado = ((nuevo_x, nuevo_y), nuevo_lleva_pasajero)

                hijo = sp.node(
                    nuevo_estado,
                    parent=nodo,
                    depth=nodo.depth + 1,
                    op=accion,
                    step_cost=1
                )
                hijos.append(hijo)

        return hijos

    def meta(self, *nodos):
        # Meta: taxi en destino con el pasajero a bordo
        pos_taxi, lleva_pasajero = nodos[0].state
        return pos_taxi == self.pos_destino and lleva_pasajero

    def h_manhattan(self, nodo, nodo_meta=None):
        # Heurística Manhattan: recoger al pasajero + llevarlo al destino
        (taxi_x, taxi_y), lleva_pasajero = nodo.state
        pasajero_x, pasajero_y = self.pos_pasajero
        destino_x, destino_y = self.pos_destino

        if not lleva_pasajero:
            return (abs(taxi_x - pasajero_x) + abs(taxi_y - pasajero_y)) + (abs(pasajero_x - destino_x) + abs(pasajero_y - destino_y))
        else:
            return abs(taxi_x - destino_x) + abs(taxi_y - destino_y)

    def h_euclidiana(self, nodo, nodo_meta=None):
        # Heurística Euclidiana: recoger al pasajero + llevarlo al destino
        (taxi_x, taxi_y), lleva_pasajero = nodo.state
        pasajero_x, pasajero_y = self.pos_pasajero
        destino_x, destino_y = self.pos_destino

        if not lleva_pasajero:
            return math.hypot(taxi_x - pasajero_x, taxi_y - pasajero_y) + math.hypot(pasajero_x - destino_x, pasajero_y - destino_y)
        else:
            return math.hypot(taxi_x - destino_x, taxi_y - destino_y)