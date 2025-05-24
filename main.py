import pygame
from battlefield import Battlefield
from agent import Agent
from task import Task
from fuzzy_engine import get_fuzzy_assignment
import heapq
import matplotlib.pyplot as plt
import random

# === Pygame Settings ===
CELL_SIZE = 50
GRID_WIDTH = 10
GRID_HEIGHT = 10
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
GREEN = (50, 200, 50)
BLUE = (50, 50, 200)
YELLOW = (255, 255, 0)

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Battlefield Assignment")
font = pygame.font.SysFont(None, 24)

# === PSO & GA Simulations (Mock Versions) ===
def simulate_pso(health, distance, urgency):
    return (health * 0.4 + urgency * 0.4 - distance * 0.2) + random.uniform(-1, 1)

def simulate_ga(health, distance, urgency):
    return (health * 0.5 + urgency * 0.3 - distance * 0.2) + random.uniform(-1, 1)

# === Show Charts Function ===
def show_performance_charts():
    assigned_agents = list(assignments.keys())
    task_efficiency = []
    response_time = []
    pso_scores = []
    ga_scores = []

    for aid in assigned_agents:
        agent = next(a for a in agents if a.id == aid)
        tid = assignments[aid]
        task = next(t for t in tasks if t.id == tid)

        dist = abs(agent.x - task.x) + abs(agent.y - task.y)
        fuzzy_score = get_fuzzy_assignment(agent.health, dist, task.urgency)
        pso_score = simulate_pso(agent.health, dist, task.urgency)
        ga_score = simulate_ga(agent.health, dist, task.urgency)

        task_efficiency.append(fuzzy_score)
        response_time.append(dist)
        pso_scores.append(pso_score)
        ga_scores.append(ga_score)

    plt.figure(figsize=(15, 5))

    # Task Efficiency Comparison
    plt.subplot(1, 2, 1)
    agent_labels = [f"A{aid}" for aid in assigned_agents]
    x = range(len(agent_labels))
    width = 0.2

    plt.bar([i - width for i in x], task_efficiency, width=width, label='Fuzzy', color='green')
    plt.bar(x, pso_scores, width=width, label='PSO', color='blue')
    plt.bar([i + width for i in x], ga_scores, width=width, label='GA', color='purple')

    plt.title("Task Efficiency Comparison")
    plt.xlabel("Agents")
    plt.ylabel("Score")
    plt.xticks(ticks=x, labels=agent_labels)
    plt.legend()

    # Response Time Bar Chart
    plt.subplot(1, 2, 2)
    plt.bar(agent_labels, response_time, color='orange')
    plt.title("Response Time (Distance)")
    plt.xlabel("Agents")
    plt.ylabel("Distance")

    plt.tight_layout()
    plt.show()

# === Main Execution ===
battle = Battlefield()

agents = [
    Agent(1, 'Attacker', 1, 1, health=80),
    Agent(2, 'Attacker', 3, 3, health=60),
    Agent(3, 'Attacker', 9, 0, health=90)
]

tasks = [
    Task(1, 'Attack', 2, 2, urgency=9),
    Task(2, 'Defend', 5, 5, urgency=7),
    Task(3, 'Scout', 8, 0, urgency=6)
]

for agent in agents:
    battle.place_entity(agent.x, agent.y, agent)

for task in tasks:
    battle.place_entity(task.x, task.y, task)

print("\n🗺️ Battlefield Grid:")
battle.display()

assignments = {}

def assign_tasks(mode):
    print(f"\n=== Task Assignment Scores ({mode}) ===")
    score_heap = []
    for agent in agents:
        for task in tasks:
            dist = abs(agent.x - task.x) + abs(agent.y - task.y)
            if mode == 'fuzzy':
                score = get_fuzzy_assignment(agent.health, dist, task.urgency)
            elif mode == 'pso':
                score = simulate_pso(agent.health, dist, task.urgency)
            elif mode == 'ga':
                score = simulate_ga(agent.health, dist, task.urgency)
            heapq.heappush(score_heap, (-score, agent.id, task.id, score))

    used_agents = set()
    used_tasks = set()
    assignments.clear()

    while score_heap and len(used_agents) < len(agents):
        _, aid, tid, score = heapq.heappop(score_heap)
        if aid not in used_agents and tid not in used_tasks:
            assignments[aid] = tid
            used_agents.add(aid)
            used_tasks.add(tid)
            print(f"✅ Agent {aid} assigned to Task {tid} with Score {score:.2f}")

# === Commander Interaction ===
selected_agent_id = None
current_mode = 'fuzzy'
assign_tasks(current_mode)

def draw_grid():
    screen.fill(WHITE)
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 1)

    # Draw Tasks
    for task in tasks:
        pygame.draw.circle(screen, RED, (task.x * CELL_SIZE + 25, task.y * CELL_SIZE + 25), 15)
        label = font.render(f"T{task.id}", True, BLACK)
        screen.blit(label, (task.x * CELL_SIZE + 5, task.y * CELL_SIZE + 5))

    # Draw Agents
    for agent in agents:
        color = GREEN if agent.id != selected_agent_id else YELLOW
        pygame.draw.circle(screen, color, (agent.x * CELL_SIZE + 25, agent.y * CELL_SIZE + 25), 15)
        label = font.render(f"A{agent.id}", True, BLACK)
        screen.blit(label, (agent.x * CELL_SIZE + 5, agent.y * CELL_SIZE + 5))

    # Draw assignment lines
    for aid, tid in assignments.items():
        agent = next(a for a in agents if a.id == aid)
        task = next(t for t in tasks if t.id == tid)
        pygame.draw.line(screen, BLUE,
                         (agent.x * CELL_SIZE + 25, agent.y * CELL_SIZE + 25),
                         (task.x * CELL_SIZE + 25, task.y * CELL_SIZE + 25), 2)

    mode_label = font.render(f"Mode: {current_mode.upper()} (F/P/G to change)", True, BLACK)
    screen.blit(mode_label, (10, WINDOW_HEIGHT - 30))

    pygame.display.flip()

def get_entity_at_position(x, y):
    grid_x = x // CELL_SIZE
    grid_y = y // CELL_SIZE
    for agent in agents:
        if agent.x == grid_x and agent.y == grid_y:
            return 'agent', agent.id
    for task in tasks:
        if task.x == grid_x and task.y == grid_y:
            return 'task', task.id
    return None, None

# === GUI Event Loop ===
running = True
while running:
    draw_grid()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            etype, eid = get_entity_at_position(mx, my)
            if etype == 'agent':
                selected_agent_id = eid
            elif etype == 'task' and selected_agent_id:
                agent = next(a for a in agents if a.id == selected_agent_id)
                task = next(t for t in tasks if t.id == eid)
                dist = abs(agent.x - task.x) + abs(agent.y - task.y)
                if current_mode == 'fuzzy':
                    score = get_fuzzy_assignment(agent.health, dist, task.urgency)
                elif current_mode == 'pso':
                    score = simulate_pso(agent.health, dist, task.urgency)
                elif current_mode == 'ga':
                    score = simulate_ga(agent.health, dist, task.urgency)
                assignments[selected_agent_id] = eid
                print(f"✅ Agent {selected_agent_id} reassigned to Task {eid} with Score {score:.2f}")
                selected_agent_id = None

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_c:
                show_performance_charts()
            elif event.key == pygame.K_f:
                current_mode = 'fuzzy'
                assign_tasks(current_mode)
            elif event.key == pygame.K_p:
                current_mode = 'pso'
                assign_tasks(current_mode)
            elif event.key == pygame.K_g:
                current_mode = 'ga'
                assign_tasks(current_mode)

pygame.quit()
