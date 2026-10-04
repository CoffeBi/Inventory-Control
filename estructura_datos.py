class Pila:

    def __init__(self):
        self.elementos = []

    def push(self, accion):
        self.elementos.append(accion)

    def pop(self):
        if self.elementos:
            return self.elementos.pop()
        return None

    def ver_cima(self):
        if self.elementos:
            return self.elementos[-1]
        return None

    def esta_vacia(self):
        return len(self.elementos) == 0


class Cola:

    def __init__(self):
        self.elementos = []

    def encolar(self, id_prod):
        if id_prod not in self.elementos:
            self.elementos.append(id_prod)

    def desencolar(self):
        if self.elementos:
            return self.elementos.pop(0)
        return None

    def esta_vacia(self):
        return len(self.elementos) == 0

    def tamanio(self):
        return len(self.elementos)


def buscar_en_lista(lista, id_buscado, i=0):
    if i == len(lista):
        return None
    elemento = lista[i]
    if isinstance(elemento, dict) and elemento.get("nombre", "").lower() == id_buscado.lower():
        return elemento
    elif hasattr(elemento, "id") and getattr(elemento, "id") == id_buscado:
        return elemento
    elif elemento == id_buscado:
        return elemento
    return buscar_en_lista(lista, id_buscado, i + 1)
