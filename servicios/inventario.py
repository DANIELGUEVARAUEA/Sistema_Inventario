# servicios/inventario.py

import os
from typing import List, Optional, Tuple

from modelos.producto import Producto


class Inventario:
    """
    Inventario  en el cual se crea una base de datos en un archivo de texto:
    - Carga automática al iniciar desde inventario.txt
    - Guardado automático al añadir / actualizar / eliminar
    - Manejo de excepciones: FileNotFoundError, PermissionError, OSError, y datos corruptos
    - Si el archivo no existe, lo crea desde cero
    """

    def __init__(self, ruta_archivo: str = "inventario.txt"):
        self._productos: List[Producto] = []
        self._ruta_archivo = ruta_archivo
        self._avisos_carga: List[str] = []

        self._asegurar_archivo()
        self._cargar_desde_archivo()

    # -------------------------
    # Utilidades (archivo)
    # -------------------------

    def _asegurar_archivo(self) -> None:
        """Crea el archivo si no existe."""
        try:
            if not os.path.exists(self._ruta_archivo):
                with open(self._ruta_archivo, "w", encoding="utf-8"):
                    pass
        except PermissionError as e:
            self._avisos_carga.append(
                f"No se pudo crear '{self._ruta_archivo}' por falta de permisos: {e}"
            )
        except OSError as e:
            self._avisos_carga.append(
                f"Error del sistema creando '{self._ruta_archivo}': {e}"
            )

    def _producto_a_linea(self, producto: Producto) -> str:
        """Convierte Producto -> línea 'id|nombre|cantidad|precio'."""
        return (
            f"{producto.get_id()}|{producto.get_nombre()}|"
            f"{producto.get_cantidad()}|{producto.get_precio()}"
        )

    def _linea_a_producto(self, linea: str) -> Producto:
        """
        Convierte línea -> Producto.
        Lanza ValueError si el formato es inválido o los tipos no convierten.
        """
        partes = linea.strip().split("|")
        if len(partes) != 4:
            raise ValueError("Formato inválido. Se esperaba: id|nombre|cantidad|precio")

        id_str = partes[0].strip()
        nombre = partes[1].strip()
        cantidad = int(partes[2].strip())
        precio = float(partes[3].strip())

        if not id_str or not nombre:
            raise ValueError("ID o nombre vacío.")

        # Usa tu constructor real:
        return Producto(id_str, nombre, cantidad, precio)

    def _cargar_desde_archivo(self) -> None:
        """
        Reconstruye la lista desde el archivo.
        Si hay líneas corruptas, se ignoran y se registran avisos.
        """
        self._productos = []
        self._avisos_carga = []

        try:
            with open(self._ruta_archivo, "r", encoding="utf-8") as f:
                for num_linea, linea in enumerate(f, start=1):
                    linea = linea.strip()
                    if not linea:
                        continue

                    try:
                        prod = self._linea_a_producto(linea)

                        # Evitar duplicados por ID en caso de archivo corrupto
                        if self._buscar_por_id(prod.get_id()) is None:
                            self._productos.append(prod)
                        else:
                            self._avisos_carga.append(
                                f"Línea {num_linea}: ID duplicado '{prod.get_id()}'. Se ignoró."
                            )

                    except (ValueError, TypeError) as e:
                        self._avisos_carga.append(
                            f"Línea {num_linea} corrupta. Se ignoró. Detalle: {e}"
                        )

        except FileNotFoundError:
            # Si lo borraron mientras corre, lo recreamos
            self._avisos_carga.append(
                f"No se encontró '{self._ruta_archivo}'. Se creó un archivo nuevo vacío."
            )
            self._asegurar_archivo()

        except PermissionError as e:
            self._avisos_carga.append(
                f"No hay permisos para leer '{self._ruta_archivo}': {e}"
            )

        except OSError as e:
            self._avisos_carga.append(
                f"Error del sistema leyendo '{self._ruta_archivo}': {e}"
            )

    def _guardar_todo(self) -> Tuple[bool, str]:
        """
        Guarda TODO el inventario.
        Usa archivo temporal + os.replace para reducir riesgo de corrupción.
        """
        tmp_path = f"{self._ruta_archivo}.tmp"
        try:
            with open(tmp_path, "w", encoding="utf-8") as f:
                for p in self._productos:
                    f.write(self._producto_a_linea(p) + "\n")

            os.replace(tmp_path, self._ruta_archivo)
            return True, f"Inventario guardado en '{self._ruta_archivo}'."

        except PermissionError as e:
            return False, f"Permisos insuficientes al guardar '{self._ruta_archivo}': {e}"

        except OSError as e:
            return False, f"Error del sistema al guardar '{self._ruta_archivo}': {e}"

        finally:
            # Limpieza del temporal si quedó
            try:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
            except OSError:
                pass

    def obtener_avisos_carga(self) -> List[str]:
        """Avisos (líneas corruptas, permisos, etc.) generados al cargar."""
        return list(self._avisos_carga)

    # -------------------------
    # Utilidad interna
    # -------------------------

    def _buscar_por_id(self, id: str) -> Optional[Producto]:
        for producto in self._productos:
            if producto.get_id() == id:
                return producto
        return None

    # -------------------------
    # Métodos públicos (persistentes)
    # -------------------------

    def anadir_producto(self, producto: Producto, notificar: bool = False) -> Tuple[bool, str]:
        if self._buscar_por_id(producto.get_id()) is not None:
            msg = f"No se agregó: ya existe un producto con ID '{producto.get_id()}'."
            if notificar:
                print(msg)
            return False, msg

        self._productos.append(producto)

        ok, detalle = self._guardar_todo()
        msg = "Producto agregado y guardado." if ok else f"Agregado en memoria, pero NO se pudo guardar. {detalle}"

        if notificar:
            print(msg)
        return ok, msg

    def eliminar_producto(self, id: str, notificar: bool = False) -> Tuple[bool, str]:
        producto = self._buscar_por_id(id)
        if producto is None:
            msg = f"No se eliminó: no existe producto con ID '{id}'."
            if notificar:
                print(msg)
            return False, msg

        self._productos.remove(producto)

        ok, detalle = self._guardar_todo()
        msg = "Producto eliminado y guardado." if ok else f"Eliminado en memoria, pero NO se pudo guardar. {detalle}"

        if notificar:
            print(msg)
        return ok, msg

    def actualizar_producto(
        self,
        id: str,
        nueva_cantidad=None,
        nuevo_precio=None,
        notificar: bool = False
    ) -> Tuple[bool, str]:
        producto = self._buscar_por_id(id)
        if producto is None:
            msg = f"No se actualizó: no existe producto con ID '{id}'."
            if notificar:
                print(msg)
            return False, msg

        # Aquí dejamos que tus setters validen y lancen ValueError si aplica
        try:
            if nueva_cantidad is not None:
                producto.set_cantidad(int(nueva_cantidad))

            if nuevo_precio is not None:
                producto.set_precio(float(nuevo_precio))

        except (ValueError, TypeError) as e:
            msg = f"Datos inválidos, no se actualizó. Detalle: {e}"
            if notificar:
                print(msg)
            return False, msg

        ok, detalle = self._guardar_todo()
        msg = "Producto actualizado y guardado." if ok else f"Actualizado en memoria, pero NO se pudo guardar. {detalle}"

        if notificar:
            print(msg)
        return ok, msg

    def buscar_por_nombre(self, texto: str) -> List[Producto]:
        texto = (texto or "").lower()
        return [p for p in self._productos if texto in p.get_nombre().lower()]

    def listar_productos(self) -> List[Producto]:
        return self._productos