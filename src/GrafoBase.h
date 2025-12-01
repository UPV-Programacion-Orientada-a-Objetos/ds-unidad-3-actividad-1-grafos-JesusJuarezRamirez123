#ifndef GRAFOBASE_H
#define GRAFOBASE_H

#include <string>
#include <vector>
#include <utility>

class GrafoBase {
public:
    virtual ~GrafoBase() {}

    // Carga los datos desde un archivo de texto (Edge List)
    virtual void cargarDatos(const std::string& archivo) = 0;

    // Retorna el ID del nodo con mayor grado y su grado
    virtual std::pair<int, int> obtenerNodoMayorGrado() = 0;

    // Ejecuta BFS desde un nodo inicio hasta una profundidad maxima
    // Retorna un vector de pares (origen, destino) representando las aristas visitadas
    virtual std::vector<std::pair<int, int>> BFS(int inicio, int profundidad_max) = 0;

    // Retorna el numero de nodos
    virtual int obtenerNumeroNodos() = 0;
    
    // Retorna el numero de aristas
    virtual int obtenerNumeroAristas() = 0;
};

#endif // GRAFOBASE_H
