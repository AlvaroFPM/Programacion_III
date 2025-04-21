
class NodoVuelo:
    def __init__(self, vuelo):
        self.vuelo = vuelo
        self.anterior = None
        self.siguiente = None

class ListaVuelos:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.contador = 0

    def agregar_vuelo(self, vuelo):
        nuevo_nodo = NodoVuelo(vuelo)
        if not self.primero:
            self.primero = self.ultimo = nuevo_nodo
        else:
            self.ultimo.siguiente = nuevo_nodo
            nuevo_nodo.anterior = self.ultimo
            self.ultimo = nuevo_nodo
        self.contador += 1

    def agregar_emergencia(self, vuelo):
        nuevo_nodo = NodoVuelo(vuelo)
        if not self.primero:
            self.primero = self.ultimo = nuevo_nodo
        else:
            nuevo_nodo.siguiente = self.primero
            self.primero.anterior = nuevo_nodo
            self.primero = nuevo_nodo
        self.contador += 1

    def insertar_en_posicion(self, vuelo, posicion):
        if posicion <= 0:
            self.agregar_emergencia(vuelo)
            return
        if posicion >= self.contador:
            self.agregar_vuelo(vuelo)
            return
        nuevo_nodo = NodoVuelo(vuelo)
        actual = self.primero
        for _ in range(posicion):
            actual = actual.siguiente
        anterior = actual.anterior
        anterior.siguiente = nuevo_nodo
        nuevo_nodo.anterior = anterior
        nuevo_nodo.siguiente = actual
        actual.anterior = nuevo_nodo
        self.contador += 1

    def extraer_vuelo(self, posicion):
        if not self.primero or posicion < 0 or posicion >= self.contador:
            return None
        actual = self.primero
        for _ in range(posicion):
            actual = actual.siguiente
        if actual.anterior:
            actual.anterior.siguiente = actual.siguiente
        else:
            self.primero = actual.siguiente
        if actual.siguiente:
            actual.siguiente.anterior = actual.anterior
        else:
            self.ultimo = actual.anterior
        self.contador -= 1
        return actual.vuelo

    def cambiar_posicion(self, origen, destino):
        if origen == destino or origen < 0 or destino < 0 or origen >= self.contador or destino >= self.contador:
            return False
        vuelo = self.extraer_vuelo(origen)
        self.insertar_en_posicion(vuelo, destino)
        return True

    def obtener_ultimo(self):
        return self.ultimo.vuelo if self.ultimo else None

    def obtener_mas_proximo(self):
        return self.primero.vuelo if self.primero else None

    def mostrar_vuelos(self):
        vuelos = []
        actual = self.primero
        while actual:
            vuelos.append(actual.vuelo)
            actual = actual.siguiente
        return vuelos
