#include "GrafoDisperso.h"
#include <fstream>
#include <sstream>
#include <algorithm>
#include <queue>
#include <set>
#include <iostream>

GrafoDisperso::GrafoDisperso() : num_nodos(0), num_aristas(0) {}

GrafoDisperso::~GrafoDisperso() {}

void GrafoDisperso::cargarDatos(const std::string& archivo) {
    std::ifstream file(archivo);
    if (!file.is_open()) {
        std::cerr << "Error al abrir el archivo: " << archivo << std::endl;
        return;
    }

    std::cout << "[C++ Core] Cargando dataset '" << archivo << "'..." << std::endl;

    // Paso 1: Leer el archivo para construir una lista de adyacencia temporal
    // Usamos vector de vectores para facilitar la construccion dinamica
    // Asumimos que los nodos son enteros no negativos.
    // Necesitamos encontrar el nodo maximo para dimensionar.
    
    std::vector<std::vector<int>> adj_temp;
    std::string line;
    int max_id = -1;
    int u, v;

    while (std::getline(file, line)) {
        if (line.empty() || line[0] == '#') continue; // Saltar comentarios
        std::stringstream ss(line);
        if (ss >> u >> v) {
            max_id = std::max(max_id, std::max(u, v));
            if (adj_temp.size() <= static_cast<size_t>(max_id)) {
                adj_temp.resize(max_id + 1);
            }
            adj_temp[u].push_back(v);
            // Si fuera no dirigido, descomentar:
            // adj_temp[v].push_back(u); 
            num_aristas++;
        }
    }
    
    num_nodos = max_id + 1;
    // Asegurar que adj_temp tenga el tamaño correcto si hay nodos aislados al final
    if (adj_temp.size() < static_cast<size_t>(num_nodos)) {
        adj_temp.resize(num_nodos);
    }

    std::cout << "[C++ Core] Carga completa. Nodos: " << num_nodos << " | Aristas: " << num_aristas << std::endl;

    // Paso 2: Convertir a formato CSR
    row_ptr.resize(num_nodos + 1);
    col_indices.reserve(num_aristas); // Reserva memoria para evitar reallocs

    int current_idx = 0;
    for (int i = 0; i < num_nodos; ++i) {
        row_ptr[i] = current_idx;
        // Ordenar vecinos para acceso mas rapido o consistente (opcional pero recomendado)
        std::sort(adj_temp[i].begin(), adj_temp[i].end());
        
        for (int neighbor : adj_temp[i]) {
            col_indices.push_back(neighbor);
            current_idx++;
        }
    }
    row_ptr[num_nodos] = current_idx;

    // Liberar memoria temporal
    std::vector<std::vector<int>>().swap(adj_temp);

    std::cout << "[C++ Core] Estructura CSR construida." << std::endl;
}

std::pair<int, int> GrafoDisperso::obtenerNodoMayorGrado() {
    int max_degree = -1;
    int node_id = -1;

    for (int i = 0; i < num_nodos; ++i) {
        // En CSR, el grado de salida es row_ptr[i+1] - row_ptr[i]
        int degree = row_ptr[i+1] - row_ptr[i];
        if (degree > max_degree) {
            max_degree = degree;
            node_id = i;
        }
    }
    return {node_id, max_degree};
}

std::vector<std::pair<int, int>> GrafoDisperso::BFS(int inicio, int profundidad_max) {
    std::vector<std::pair<int, int>> aristas_visitadas;
    if (inicio < 0 || inicio >= num_nodos) return aristas_visitadas;

    std::vector<int> distancia(num_nodos, -1);
    std::queue<int> q;

    distancia[inicio] = 0;
    q.push(inicio);

    while (!q.empty()) {
        int u = q.front();
        q.pop();

        if (distancia[u] >= profundidad_max) continue;

        // Iterar sobre vecinos usando CSR
        int start_idx = row_ptr[u];
        int end_idx = row_ptr[u+1];

        for (int i = start_idx; i < end_idx; ++i) {
            int v = col_indices[i];
            
            // Guardamos la arista visitada para visualizacion
            // (incluso si el nodo ya fue visitado, la arista existe)
            // Pero para evitar duplicados en visualizacion, quizas solo aristas del arbol BFS?
            // El requerimiento dice "lista de nodos visitados y sus aristas".
            // Retornaremos todas las aristas exploradas desde los nodos visitados dentro del rango.
            
            bool first_visit = (distancia[v] == -1);
            
            // Solo agregamos aristas que conectan con nodos dentro del rango de profundidad
            // Si distancia[u] < profundidad_max, entonces v estara a distancia[u]+1 <= profundidad_max
            aristas_visitadas.push_back({u, v});

            if (first_visit) {
                distancia[v] = distancia[u] + 1;
                q.push(v);
            }
        }
    }
    return aristas_visitadas;
}

int GrafoDisperso::obtenerNumeroNodos() {
    return num_nodos;
}

int GrafoDisperso::obtenerNumeroAristas() {
    return num_aristas;
}

std::vector<int> GrafoDisperso::obtenerVecinos(int nodo) {
    std::vector<int> vecinos;
    if (nodo < 0 || nodo >= num_nodos) return vecinos;

    int start_idx = row_ptr[nodo];
    int end_idx = row_ptr[nodo+1];

    for (int i = start_idx; i < end_idx; ++i) {
        vecinos.push_back(col_indices[i]);
    }
    return vecinos;
}
