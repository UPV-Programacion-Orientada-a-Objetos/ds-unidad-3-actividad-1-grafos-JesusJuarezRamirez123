from libcpp.string cimport string
from libcpp.vector cimport vector
from libcpp.pair cimport pair

cdef extern from "src/GrafoBase.h":
    cdef cppclass GrafoBase:
        pass

cdef extern from "src/GrafoDisperso.h":
    cdef cppclass GrafoDisperso(GrafoBase):
        GrafoDisperso() except +
        void cargarDatos(string archivo)
        pair[int, int] obtenerNodoMayorGrado()
        vector[pair[int, int]] BFS(int inicio, int profundidad_max)
        int obtenerNumeroNodos()
        int obtenerNumeroAristas()
