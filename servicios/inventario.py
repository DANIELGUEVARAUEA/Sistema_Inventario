# servicios/inventario.py

from modelos.producto import Producto  # Importamos la clase Producto


# Clase que gestiona el inventario
class Inventario:

    # Constructor: inicializa la lista de productos
    def __init__(self):
        self._productos = []  # Lista principal que almacena los productos

    # -------------------------
    # Método interno de apoyo
    # -------------------------

    # Busca un producto por su ID
    # Retorna el producto si lo encuentra, o None si no existe
    def _buscar_por_id(self, id: str):
        for producto in self._productos:
            if producto.get_id() == id:
                return producto
        return None

    # -------------------------
    # Métodos públicos
    # -------------------------

    # Añade un nuevo producto validando que el ID no esté repetido
    def anadir_producto(self, producto: Producto):
        # Verificamos si ya existe un producto con el mismo ID
        if self._buscar_por_id(producto.get_id()) is not None:
            return False  # No se agrega porque el ID ya existe
        
        # Si no existe, lo agregamos a la lista
        self._productos.append(producto)
        return True

    # Elimina un producto por ID
    def eliminar_producto(self, id: str):
        producto = self._buscar_por_id(id)
        
        # Si no existe, retorna False
        if producto is None:
            return False
        
        # Si existe, lo eliminamos de la lista
        self._productos.remove(producto)
        return True

    # Actualiza la cantidad y/o precio de un producto
    def actualizar_producto(self, id: str, nueva_cantidad=None, nuevo_precio=None):
        producto = self._buscar_por_id(id)

        # Si no se encuentra el producto
        if producto is None:
            return False

        # Si se proporciona nueva cantidad, se actualiza
        if nueva_cantidad is not None:
            producto.set_cantidad(nueva_cantidad)

        # Si se proporciona nuevo precio, se actualiza
        if nuevo_precio is not None:
            producto.set_precio(nuevo_precio)

        return True

    # Busca productos por nombre (coincidencia parcial)
    def buscar_por_nombre(self, texto: str):
        resultados = []

        # Convertimos a minúsculas para búsqueda sin importar mayúsculas
        texto = texto.lower()

        # Recorremos la lista de productos
        for producto in self._productos:
            # Si el texto está contenido en el nombre
            if texto in producto.get_nombre().lower():
                resultados.append(producto)

        return resultados

    # Devuelve todos los productos registrados
    def listar_productos(self):
        return self._productos
