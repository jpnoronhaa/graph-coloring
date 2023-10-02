#include <iostream>
#include <vector>
#include <map>

using namespace std;

struct Vertex {
    int id;
    char color;

    Vertex(int _id, char _color) : id(_id), color(_color) {}
};

struct Graph{
  private:
    map<int, vector<Vertex> > adjList;
  public: 
    void addVertex(int id, char color) {
        Vertex v(id, color);
        adjList[id].push_back(v);
    }
    void addEdge(int from, int to) {
        if (adjList.find(from) != adjList.end() && adjList.find(to) != adjList.end()) {
             adjList[from].push_back(Vertex(to, adjList[to][0].color));
             adjList[to].push_back(Vertex(from, adjList[from][0].color));
        } else {
            cout << "Vértices não existem!" << endl;
        }
    }

    void printGraph() {
        for (const auto& pair : adjList) {
            cout << "Vértice " << pair.first << " (Cor: " << pair.second[0].color << "): ";
            for (const Vertex& v : pair.second) {
                cout << v.id << " ";
            }
            cout << endl;
        }
    }
};

int main() {
  Graph graph;

  graph.addVertex(1, 'A');
  graph.addVertex(2, 'B');
  graph.addVertex(3, 'C');
  graph.addVertex(4, 'D');

  graph.addEdge(1, 2);
  graph.addEdge(1, 3);
  graph.addEdge(3, 4);
  graph.addEdge(4, 1);

  graph.printGraph();
  return 0;
}