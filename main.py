import pygame
import random
import time
import matplotlib.pyplot as plt
import heapq
from agent import Agent
from task import Task
from battlefield import Battlefield
from pso_engine import get_pso_assignment
from ga_engine import get_ga_assignment
from fuzzy_engine import get_fuzzy_assignment

# === Settings ===
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
DARK_RED = (150, 0, 0)

TASK_DURATION = 15
TASK_LIMIT = 10
TASK_ADD_INTERVAL = 3  # New task frequency (seconds)
ASSIGNMENT_LOG_INTERVAL = 7  # Log assignment details every 7 seconds

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Battlefield Assignment")
font = pygame.font.SysFont(None, 24)
battle = Battlefield()

# === Initialization ===
agents = []
tasks = []
assignments = {}  # Current agent-task assignments
assignment_history = []  # Log of assignments over time
task_timers = {}  # Task creation timestamps
progress_timers = {}  # Task progress trackers
unassigned_tasks = set()
agent_targets = {}  # Target positions for agents
selected_agent_id = None
current_mode = 'fuzzy'
occupied_positions = set()
last_task_add = time.time()
last_assignment_log_time = 0

# === Utility Function: Get Unique Grid Position ===
def get_unique_position():
    while True:
        x, y = random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)
        if (x, y) not in occupied_positions:
            occupied_positions.add((x, y))
            return x, y

# Initialize agents
for i in range(3):
    x, y = get_unique_position()
    agents.append(Agent(i+1, 'Attacker', x, y, health=random.randint(50, 100), stamina=random.randint(50, 100), speed=random.randint(1, 5)))

# Initialize tasks
for i in range(3):
    x, y = get_unique_position()
    task = Task(i+1, 'Task', x, y, urgency=random.randint(5, 10))
    tasks.append(task)
    task_timers[task.id] = time.time()
    progress_timers[task.id] = 0

# === Assignment Logic ===
def assign_tasks(mode):
    global last_assignment_log_time
    assignments.clear()

    if mode == 'pso':
        result = get_pso_assignment(agents, tasks)
    elif mode == 'ga':
        result = get_ga_assignment(agents, tasks)
    else:
        result = fuzzy_assignment()

    assignments.update(result)
    assignment_history.append(assignments.copy())

    # Log assignment scores periodically
    now = time.time()
    if now - last_assignment_log_time >= ASSIGNMENT_LOG_INTERVAL:
        print("\n=== Assignment Results ===")
        for aid, tid in assignments.items():
            agent = next((a for a in agents if a.id == aid), None)
            task = next((t for t in tasks if t.id == tid), None)
            if agent and task:
                dist = ((agent.x - task.x)**2 + (agent.y - task.y)**2)**0.5
                score = get_fuzzy_assignment(agent.health, dist, task.urgency)
                print(f"✅ Agent {aid} assigned to Task {tid} with Score {score:.2f} and Distance {dist:.2f}")
        last_assignment_log_time = now

# === Fuzzy Assignment Function ===
def fuzzy_assignment():
    heap, result = [], {}
    used_agents, used_tasks = set(), set()
    for agent in agents:
        for task in tasks:
            dist = ((agent.x - task.x)**2 + (agent.y - task.y)**2)**0.5 / agent.speed
            score = get_fuzzy_assignment(agent.health, dist, task.urgency)
            heapq.heappush(heap, (-score, agent.id, task.id))
    while heap and len(used_agents) < len(agents):
        _, aid, tid = heapq.heappop(heap)
        if aid not in used_agents and tid not in used_tasks:
            result[aid] = tid
            used_agents.add(aid)
            used_tasks.add(tid)
    return result

# Perform initial assignment
assign_tasks(current_mode)

# === Draw Battlefield Grid and Entities ===
def draw():
    screen.fill(WHITE)
    mx, my = pygame.mouse.get_pos()
    gx, gy = mx // CELL_SIZE, my // CELL_SIZE

    # Draw grid
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            pygame.draw.rect(screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

    max_urgency = max([t.urgency for t in tasks], default=0)
    blink_intensity = int((time.time() * 4) % 2) * 50

    # Draw tasks
    for task in tasks:
        color = RED
        if task.urgency >= max_urgency:
            color = (255, blink_intensity, blink_intensity)
        pygame.draw.circle(screen, color, (task.x * CELL_SIZE + 25, task.y * CELL_SIZE + 25), 15)
        screen.blit(font.render(f"T{task.id}", True, BLACK), (task.x * CELL_SIZE + 5, task.y * CELL_SIZE + 5))
    
    # Only show task tooltip if NO agent is on the same cell
        if task.x == gx and task.y == gy and not any(a.x == task.x and a.y == task.y for a in agents):
            screen.blit(font.render(f"Urgency: {round(task.urgency, 2)}", True, BLACK), (task.x * CELL_SIZE + 30, task.y * CELL_SIZE + 10))


    # Draw agents
    for agent in agents:
        color = YELLOW if agent.id == selected_agent_id else GREEN
        pygame.draw.circle(screen, color, (agent.x * CELL_SIZE + 25, agent.y * CELL_SIZE + 25), 15)
        screen.blit(font.render(f"A{agent.id}", True, BLACK), (agent.x * CELL_SIZE + 5, agent.y * CELL_SIZE + 5))
        if agent.x == gx and agent.y == gy:
            screen.blit(font.render(f"H:{agent.health} S:{int(agent.stamina)} Sp:{agent.speed}", True, BLACK), (agent.x * CELL_SIZE + 30, agent.y * CELL_SIZE + 10))


    # Draw assignment lines and task progress
    for aid, tid in assignments.items():
        agent = next(a for a in agents if a.id == aid)
        task = next((t for t in tasks if t.id == tid), None)
        if task:
            pygame.draw.line(screen, BLUE, (agent.x * CELL_SIZE + 25, agent.y * CELL_SIZE + 25), (task.x * CELL_SIZE + 25, task.y * CELL_SIZE + 25), 2)
            progress = progress_timers.get(task.id, 0) / TASK_DURATION
            pygame.draw.rect(screen, BLACK, (task.x * CELL_SIZE + 10, task.y * CELL_SIZE - 5, 30, 5))
            pygame.draw.rect(screen, GREEN, (task.x * CELL_SIZE + 10, task.y * CELL_SIZE - 5, 30 * progress, 5))

    # Display current mode
    screen.blit(font.render(f"Mode: {current_mode.upper()} (F/P/G)", True, BLACK), (10, WINDOW_HEIGHT - 30))
    pygame.display.flip()

# === Show Efficiency Chart ===
def show_charts():
    agent_ids = list(assignments.keys())
    fuzzy_scores, pso_scores, ga_scores, dist_list = [], [], [], []
    for aid in agent_ids:
        agent = next(a for a in agents if a.id == aid)
        tid = assignments[aid]
        task = next(t for t in tasks if t.id == tid)
        dist = ((agent.x - task.x)**2 + (agent.y - task.y)**2)**0.5
        dist_list.append(dist)
        fuzzy_scores.append(get_fuzzy_assignment(agent.health, dist, task.urgency))
        pso_scores.append(agent.health * 0.4 + task.urgency * 0.4 - dist * 0.2)
        ga_scores.append(agent.health * 0.5 + task.urgency * 0.3 - dist * 0.2)

    x = list(range(1, len(agent_ids) + 1))
    width = 0.2
    plt.figure(figsize=(14, 5))
    plt.subplot(1, 2, 1)
    plt.bar([i - width for i in x], fuzzy_scores, width=width, label='Fuzzy')
    plt.bar(x, pso_scores, width=width, label='PSO')
    plt.bar([i + width for i in x], ga_scores, width=width, label='GA')
    plt.title("Task Assignment Efficiency")
    plt.xlabel("Agent ID")
    plt.ylabel("Score")
    plt.xticks(x)
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.bar(x, dist_list, color='orange')
    plt.title("Agent to Task Distance")
    plt.xlabel("Agent ID")
    plt.ylabel("Distance")
    plt.xticks(x)
    plt.tight_layout()
    plt.show()

# === Show Assignment History Chart ===
def show_history_chart():
    if not assignment_history:
        print("No assignment history to show yet.")
        return
    timestamps = list(range(len(assignment_history)))
    data = {agent.id: [] for agent in agents}
    for snapshot in assignment_history:
        for aid in data:
            data[aid].append(snapshot.get(aid, None))
    plt.figure(figsize=(12, 6))
    for aid, task_ids in data.items():
        plt.plot(timestamps, task_ids, label=f"Agent {aid}", marker='o')
    plt.title("Assignment History")
    plt.xlabel("Event")
    plt.ylabel("Task ID")
    plt.xticks(timestamps)
    plt.legend()
    plt.grid(True)
    plt.show()

# === Main Game Loop ===
running = True
last_move_time = time.time()

while running:
    draw()
    now = time.time()

    # Dynamically add new tasks if under limit
    if now - last_task_add > TASK_ADD_INTERVAL and len(tasks) < TASK_LIMIT:
        x, y = get_unique_position()
        tid = max([t.id for t in tasks if isinstance(t.id, int)] + [0]) + 1
        task = Task(tid, 'Dynamic', x, y, urgency=random.randint(5, 10))
        tasks.append(task)
        task_timers[task.id] = now
        progress_timers[task.id] = 0
        assign_tasks(current_mode)
        last_task_add = now

    # Trigger reassignment if tasks are left unassigned or reach high urgency
    for task in tasks:
        if task.id not in assignments.values():
            task.urgency = min(10, task.urgency + 0.01)
            if task.urgency >= 10:
                assign_tasks(current_mode)

    # Agent movement and task progress updates
    if now - last_move_time >= 1:
        for agent in agents:
            tid = assignments.get(agent.id)
            if tid:
                task = next((t for t in tasks if t.id == tid), None)
                if task:
                    tx, ty = task.x, task.y
                    if (agent.x, agent.y) != (tx, ty):
                        dx = 1 if tx > agent.x else -1 if tx < agent.x else 0
                        dy = 1 if ty > agent.y else -1 if ty < agent.y else 0
                        agent.x += dx
                        agent.y += dy
                        agent.stamina = max(0, agent.stamina - 1)
                    else:
                        progress_timers[tid] = min(TASK_DURATION, progress_timers.get(tid, 0) + 1)
                        if progress_timers[tid] >= TASK_DURATION:
                            tasks[:] = [t for t in tasks if t.id != tid]
                            progress_timers.pop(tid, None)
                            task_timers.pop(tid, None)
                            assign_tasks(current_mode)
            else:
                agent.stamina = min(100, agent.stamina + 0.1)
        last_move_time = now

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                current_mode = 'fuzzy'
                assign_tasks(current_mode)
            elif event.key == pygame.K_p:
                current_mode = 'pso'
                assign_tasks(current_mode)
            elif event.key == pygame.K_g:
                current_mode = 'ga'
                assign_tasks(current_mode)
            elif event.key == pygame.K_c:
                show_history_chart()
            elif event.key == pygame.K_v:
                show_charts()
            elif event.key == pygame.K_q:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            gx, gy = mx // CELL_SIZE, my // CELL_SIZE
            for agent in agents:
                if agent.x == gx and agent.y == gy:
                    selected_agent_id = agent.id
                    break
            else:
                if selected_agent_id:
                    agent = next((a for a in agents if a.id == selected_agent_id), None)
                    if agent:
                        agent.x, agent.y = gx, gy
                        assign_tasks(current_mode)
                    selected_agent_id = None

pygame.quit()