from pyswarm import pso
import numpy as np
from itertools import permutations
import sys
import os

# Suppress pyswarm output
class DummyOutput:
    def write(self, x): pass
    def flush(self): pass

def get_pso_assignment(agents, tasks):
    num_agents = len(agents)
    num_tasks = len(tasks)

    if num_tasks == 0:
        return {}

    # Use brute force for small inputs
    if num_agents <= 7 and num_tasks <= num_agents:
        return brute_force_assignment(agents, tasks)

    prev_stdout = sys.stdout
    sys.stdout = DummyOutput()  # Suppress pyswarm internal print

    def fitness(x):
        total_score = 0
        assigned_tasks = set()
        for i, task_index in enumerate(x.astype(int)):
            if task_index >= num_tasks:
                continue
            if task_index in assigned_tasks:
                continue
            assigned_tasks.add(task_index)
            agent = agents[i]
            task = tasks[task_index]

            dist = abs(agent.x - task.x) + abs(agent.y - task.y)
            time_to_reach = dist / max(agent.speed, 0.1)

            # Task urgency rises over time; minimize time to start
            score = agent.health * 0.3 + task.urgency * 0.4 - time_to_reach * 0.3
            total_score += score
        return -total_score  # minimize

    lb = np.zeros(len(agents))
    ub = np.full(len(agents), num_tasks)  # index range up to num_tasks (invalids ignored)

    xopt, _ = pso(fitness, lb, ub, swarmsize=30, maxiter=50, debug=False)

    sys.stdout = prev_stdout  # Restore normal output

    result = {}
    used_tasks = set()
    for i, task_index in enumerate(xopt.astype(int)):
        if task_index < num_tasks and task_index not in used_tasks:
            result[agents[i].id] = tasks[task_index].id
            used_tasks.add(task_index)
        else:
            result[agents[i].id] = None

    return result

def brute_force_assignment(agents, tasks):
    num_agents = len(agents)
    num_tasks = len(tasks)
    best_score = float('-inf')
    best_assignment = {}

    for perm in permutations(range(num_tasks), min(num_agents, num_tasks)):
        score = 0
        assignment = {}
        for i, task_index in enumerate(perm):
            agent = agents[i]
            task = tasks[task_index]
            dist = abs(agent.x - task.x) + abs(agent.y - task.y)
            time_to_reach = dist / max(agent.speed, 0.1)
            score += agent.health * 0.3 + task.urgency * 0.4 - time_to_reach * 0.3
            assignment[agent.id] = task.id
        if score > best_score:
            best_score = score
            best_assignment = assignment

    for agent in agents:
        if agent.id not in best_assignment:
            best_assignment[agent.id] = None

    return best_assignment
