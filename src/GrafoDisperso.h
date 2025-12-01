#ifndef GRAFODISPERSO_H
#define GRAFODISPERSO_H

#include "GrafoBase.h"
#include <vector>
#include <string>
#include <iostream>

class GrafoDisperso : public GrafoBase {
private:
    int num_nodos;
    int num_aristas;
    
    // Estructura CSR (Compressed Sparse Row)
    // row_ptr: indices donde empieza cada fila en col_indices (tamaño num_nodos + 1)
    std::vector<int> row_ptr;
    // col_indices: indices de las columnas (destinos de las aristas)
    std::vector<int> col_indices;
    // values: no necesario para grafos no ponderados, pero parte del estandar CSR. Omitido por eficiencia.

public:
    GrafoDisperso();
    ~GrafoDisperso();

    void cargarDatos(const std::string& archivo) override;
    std::pair<int, int> obtenerNodoMayorGrado() override;
    std::vector<std::pair<int, int>> BFS(int inicio, int profundidad_max) override;
    int obtenerNumeroNodos() override;
    int obtenerNumeroAristas() override;

    // Metodo auxiliar para obtener vecinos (usado internamente o expuesto si necesario)
    std::vector<int> obtenerVecinos(int nodo);
};

#endif // GRAFODISPERSO_H
