from my_vf2pp import graph
import random
from itertools import combinations
import numpy as np

class GeneticIsomorphismSolver:
    def __init__(self, S: graph, G: graph, population_size=50, max_generations=1000):
        self.S = S
        self.G = G
        self.population_size = population_size
        self.max_generations = max_generations

        self.build_fingerprint_map()

    def build_fingerprint_map(self):
        def calcular_numero_triangulos(G, node):
            # Iterar sobre todas las combinaciones de pares de vecinos y contar los triangulos asociados al nodo inicial
            triangulos = 0
            for neigh1, neigh2 in combinations(G.neighs[node], 2):
                if neigh2 in G.neighs[neigh1]:
                    triangulos += 1
            return triangulos
        
        calcular_grados = lambda G, node: G.deg(node)
        calcular_grados_vecinos = lambda G, node: sum(G.deg(neigh) for neigh in G.neighs[node])

        fingerprints_S = {node:(calcular_grados(self.S, node), calcular_grados_vecinos(self.S, node), calcular_numero_triangulos(self.S, node)) for node in self.S.nodes}

        fingerprints_G = {node:(calcular_grados(self.G, node), calcular_grados_vecinos(self.G, node), calcular_numero_triangulos(self.G, node)) for node in self.G.nodes}

        # print("Fingerprints S:", fingerprints_S)
        # print("Fingerprints G:", fingerprints_G)
        self.fingerprint_S = fingerprints_S
        self.fingerprint_G = fingerprints_G

    def calcular_candidatos(self, node_S, already_used = set()):
        def todos_mayores(punto1, punto2):
            return all(c2 >= c1 for c1, c2 in zip(punto1, punto2))
        
        candidatos = set()
        for node_G, fingerprint_G in self.fingerprint_G.items():
            if node_G not in already_used:
                if todos_mayores(self.fingerprint_S[node_S],fingerprint_G):
                    candidatos.add(node_G)
        if not candidatos:
            print("No hay candidatos para el nodo", node_S)
        return candidatos


    def generate_initial_population(self):
        population = []
        for _ in range(self.population_size):
            already_used = set()
            individual = {node:None for node in self.S.nodes}
            for node in self.S.nodes:
                candidate = random.choice(list(self.calcular_candidatos(node, already_used)))
                individual[node] = candidate
                already_used.add(candidate)
            population.append(individual)

        return population
    
    def fitness(self, individual):
        # Se busca maximizar la cantidad de aristas que se conservan en el grafo S
        # Se verifica entonces que cada arista de S tenga una arista correspondiente en G con el mapeo creado (individuo)

        # Penalizamos que el individuo no use nodos distintos de G:
        fitness_value = 0

        if len(set(individual.values())) != len(individual.values()):
            return fitness_value

        for u, v in self.S.edges:
            mapped_edge = tuple(sorted((individual[u], individual[v])))
            print("Evaluando arista", mapped_edge)
            if mapped_edge in self.G.edges:
                fitness_value += 1

        return fitness_value
    
    def crossover(self, parent1, parent2):  
        # Realiza un cruce entre dos padres para generar un nuevo individuo
        # Para cada nodo del mapeo se elige aletoriamente entre el nodo mapeado por el padre 1 o el padre 2
        # No se asegura que el nuevo individuo sea un mapeo válido por lo que se penaliza en la función de fitness
        child = {}
        for node in self.S.nodes:
            if random.random() < 0.5:
                child[node] = parent1[node]
            else:
                child[node] = parent2[node]
        return child
    
    def mutate(self, individual, mutation_rate=0.1):
        # Realiza una mutación en el individuo, cambiando aleatoriamente el mapeo de un nodo por alguno de sus otros candidatos
        # Se asegura que el nuevo nodo no haya sido usado en el mapeo
        already_used = set(individual.values())
        for node in individual:
            if random.random() < mutation_rate:
                candidates = self.calcular_candidatos(node, already_used)
                if candidates:
                    new_node = random.choice(list(candidates))
                    already_used.remove(individual[node])
                    already_used.add(new_node)
                    individual[node] = new_node

        return individual
    
    def solve(self):
        population = self.generate_initial_population()
        best_individual = None
        best_fitness = float('-inf')

        for generation in range(self.max_generations):
            # Calcular el fitness de la población
            fitness_scores = [self.fitness(individual) for individual in population]

            # Selecciono el mejor fitness
            curr_max_fitness = max(fitness_scores)

            if curr_max_fitness > best_fitness:
                best_fitness = curr_max_fitness
                best_individual = population[fitness_scores.index(curr_max_fitness)]
                if best_fitness == len(self.S.edges):
                    print("Isomorfismo encontrado en la generación", generation)
                    break # En este caso se encuentra un isomorfismo exacto

            # Seleccionamos nuevos individuos para la siguienete generación
            new_population = [best_individual] # Incluimos el mejor individuo (elitismo)
            print(fitness_scores)
            while len(new_population) < self.population_size:
                parent1 = population[random.choices(range(len(population)), weights=fitness_scores)[0]]
                parent2 = population[random.choices(range(len(population)), weights=fitness_scores)[0]]

                child = self.crossover(parent1, parent2)
                child = self.mutate(child)

                if child and self.fitness(child) >= 0: # Verificamos que solo se acepten mapeos válidos
                    new_population.append(child)
        
        return best_individual, best_fitness
    
if __name__ == "__main__":
    G = graph(list(range(5)),
            [(0,1),(1,2),(2,3),(3,4),(4,0),(4,1),(4,2)],
            {i:0 for i in range(5)})

    S = graph(list(range(4)),
            [(0,1),(1,2),(2,0), (1,3)],
            {i:0 for i in range(4)})

    solver = GeneticIsomorphismSolver(S, G, population_size=10)
    print(solver.G.edges)
    print(solver.solve())