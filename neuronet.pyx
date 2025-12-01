# distutils: language = c++
# distutils: sources = src/GrafoDisperso.cpp

from neuronet_core cimport GrafoDisperso
from libcpp.string cimport string
from libcpp.vector cimport vector
from libcpp.pair cimport pair

cdef class NeuroNetEngine:
    cdef GrafoDisperso* c_grafo  # Puntero a la instancia C++

    def __cinit__(self):
        self.c_grafo = new GrafoDisperso()

    def __dealloc__(self):
        del self.c_grafo

    def cargar_datos(self, archivo: str):
        """Carga un dataset desde un archivo."""
        cdef string c_archivo = archivo.encode('utf-8')
        self.c_grafo.cargarDatos(c_archivo)

    def obtener_nodo_mayor_grado(self):
        """Retorna (nodo_id, grado)."""
        return self.c_grafo.obtenerNodoMayorGrado()

    def bfs(self, inicio: int, profundidad_max: int):
        """Ejecuta BFS y retorna lista de aristas (u, v)."""
        return self.c_grafo.BFS(inicio, profundidad_max)

    def obtener_estadisticas(self):
        """Retorna diccionario con estadisticas basicas."""
        return {
            "nodos": self.c_grafo.obtenerNumeroNodos(),
            "aristas": self.c_grafo.obtenerNumeroAristas()
        }
