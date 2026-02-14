# modelos/producto.py

# Clase que representa la entidad Producto
class Producto:
    
    # Constructor: inicializa los atributos del producto
    def __init__(self, id: str, nombre: str, cantidad: int, precio: float):
        self._id = id              # Identificador único del producto
        self._nombre = nombre      # Nombre del producto
        self._cantidad = cantidad  # Cantidad disponible en inventario
        self._precio = precio      # Precio unitario del producto

    # -------------------
    # Métodos GETTERS
    # -------------------

    # Devuelve el ID del producto
    def get_id(self) -> str:
        return self._id

    # Devuelve el nombre del producto
    def get_nombre(self) -> str:
        return self._nombre

    # Devuelve la cantidad disponible
    def get_cantidad(self) -> int:
        return self._cantidad

    # Devuelve el precio del producto
    def get_precio(self) -> float:
        return self._precio

    # -------------------
    # Métodos SETTERS
    # -------------------

    # Modifica el nombre del producto
    def set_nombre(self, nombre: str) -> None:
        self._nombre = nombre

    # Modifica la cantidad con validación
    def set_cantidad(self, cantidad: int) -> None:
        # Validamos que la cantidad no sea negativa
        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa.")
        self._cantidad = cantidad

    # Modifica el precio con validación
    def set_precio(self, precio: float) -> None:
        # Validamos que el precio no sea negativo
        if precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        self._precio = precio

    # Método especial que permite mostrar el objeto de forma legible
    def __str__(self) -> str:
        return f"ID: {self._id} | Nombre: {self._nombre} | Cantidad: {self._cantidad} | Precio: ${self._precio:.2f}"
