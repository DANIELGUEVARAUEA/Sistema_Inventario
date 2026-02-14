# main.py

from modelos.producto import Producto
from servicios.inventario import Inventario


# Función que muestra el menú principal
def mostrar_menu():
    print("\n===== SISTEMA DE INVENTARIO DG =====")
    print("1. Añadir producto")
    print("2. Eliminar producto")
    print("3. Actualizar producto")
    print("4. Buscar producto")
    print("5. Listar inventario")
    print("0. Salir")


# Función principal del programa
def main():
    inventario = Inventario()  # Creamos una instancia del inventario

    # Ciclo principal del sistema
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        # Opción 1: Añadir producto
        if opcion == "1":
            idp = input("ID: ")
            nombre = input("Nombre: ")
            cantidad = int(input("Cantidad: "))
            precio = float(input("Precio: "))

            producto = Producto(idp, nombre, cantidad, precio)

            if inventario.anadir_producto(producto):
                print("Producto añadido correctamente.")
            else:
                print("Error: El ID ya existe.")

        # Opción 2: Eliminar producto
        elif opcion == "2":
            idp = input("ID del producto a eliminar: ")
            if inventario.eliminar_producto(idp):
                print("Producto eliminado.")
            else:
                print("Producto no encontrado.")

        # Opción 3: Actualizar producto
        elif opcion == "3":
            idp = input("ID del producto a actualizar: ")
            nueva_cantidad = int(input("Nueva cantidad: "))
            nuevo_precio = float(input("Nuevo precio: "))

            if inventario.actualizar_producto(idp, nueva_cantidad, nuevo_precio):
                print("Producto actualizado.")
            else:
                print("Producto no encontrado.")

        # Opción 4: Buscar producto
        elif opcion == "4":
            texto = input("Ingrese nombre o parte del nombre: ")
            resultados = inventario.buscar_por_nombre(texto)

            for producto in resultados:
                print(producto)

        # Opción 5: Listar inventario
        elif opcion == "5":
            for producto in inventario.listar_productos():
                print(producto)

        # Opción 0: Salir
        elif opcion == "0":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción inválida.")


# Punto de entrada del programa
if __name__ == "__main__":
    main()
