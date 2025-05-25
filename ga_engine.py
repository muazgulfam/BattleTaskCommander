from pyeasyga.pyeasyga import GeneticAlgorithm
import random

def get_ga_assignment(agents, tasks):
    # Create a flat list of (agent, task) pairings as possible genes
    data = [(agent, task) for agent in agents for task in tasks]

    def fitness(individual, data):
        total_score = 0
        used_agents = set()
        used_tasks = set()

        for i, bit in enumerate(individual):
            if bit == 1:
                agent, task = data[i]
                if agent.id in used_agents or task.id in used_tasks:
                    continue  # Avoid duplicate assignments
                dist = abs(agent.x - task.x) + abs(agent.y - task.y)
                score = agent.health * 0.5 + task.urgency * 0.3 - dist * 0.2
                total_score += score
                used_agents.add(agent.id)
                used_tasks.add(task.id)

        return total_score

    ga = GeneticAlgorithm(data)
    ga.fitness_function = fitness
    ga.population_size = 50
    ga.generations = 100
    ga.mutation_probability = 0.1
    ga.crossover_probability = 0.8

    def create_individual(data):
        # Start with all 0s, then randomly activate num_agents genes
        num_genes = len(data)
        num_agents = len(agents)
        idxs = random.sample(range(num_genes), num_agents)
        individual = [1 if i in idxs else 0 for i in range(num_genes)]
        return individual

    ga.create_individual = create_individual

    ga.run()

    # Get the best individual properly
    best_individual = ga.best_individual()[1]  # The individual is the second element

    assignment = {}
    used_tasks = set()

    for i, bit in enumerate(best_individual):
        if bit == 1:
            agent, task = data[i]
            if agent.id not in assignment and task.id not in used_tasks:
                assignment[agent.id] = task.id
                used_tasks.add(task.id)

    return assignment