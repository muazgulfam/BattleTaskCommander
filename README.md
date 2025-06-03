# 🪖 Battlefield Simulation Project

A Python-based battlefield simulation that models intelligent agents completing tasks in a dynamic, grid-based environment. This project integrates **AI optimization algorithms** (Particle Swarm Optimization, Genetic Algorithm), **Fuzzy Logic**, and various real-time decision-making mechanics to simulate autonomous multi-agent coordination. The simulation features autonomous agents—representing soldiers or units—tasked with completing objectives of varying urgency, complexity, and expiration times. At its core, the system compares three intelligent optimization techniques: Fuzzy Logic, **Particle Swarm Optimization** (PSO), and **Genetic Algorithms** (GA). Each algorithm is responsible for deciding how tasks should be assigned among available agents to maximize performance metrics such as efficiency, response time, and resource utilization. Users act as commanders and can switch between AI strategies in real time to observe how each approach handles the same scenario differently. The simulation includes a visual grid-based battlefield where agents move, make decisions, and respond to environmental changes, while live performance charts offer immediate feedback on algorithm effectiveness. Designed as a learning and experimentation tool, the project aims to demonstrate how heuristic and bio-inspired algorithms can solve complex, multi-agent coordination problems in real-world scenarios like military logistics, disaster response, and industrial automation.
    [Project Repo](https://github.com/muazgulfam/Battle_Task_Commander)

---

## 🧠 AI Concepts Demonstrated

- **Swarm Intelligence**: Agents coordinate task assignment through decentralized decision-making, inspired by the collective behavior of natural swarms.
- **Heuristic Optimization**: Real-time optimization using Particle Swarm Optimization (PSO) and Genetic Algorithm (GA) to assign tasks efficiently.
- **Fuzzy Logic Reasoning**: Agents make soft, human-like decisions under uncertainty by evaluating urgency, distance, and stamina using fuzzy rules.
- **Agent-Based Modeling**: Each agent operates independently with its own state and logic, creating emergent global behavior through local interactions.
- **Task Scheduling & Adaptation**: Agents respond dynamically to changing task urgency, stamina levels, and competition for tasks, showcasing adaptive AI behavior.


## 📌 Project Features

### ✅ Agent-Based System
- Multiple autonomous **agents** (soldiers) operate on a 10x10 grid.
- Each agent has:
  - **Stamina** (float): Decreases when moving, increases when idle.
  - **Speed** (int): Determines how fast an agent reaches tasks.
  - **Current Target**: The task they are moving towards.
  - **State**: Idle, Moving, Working.
- Agents can switch to **higher-priority tasks** if conditions change.
- Animated movements using linear interpolation for smooth transitions.

---

### 🧠 AI Techniques

#### 🔹 Particle Swarm Optimization (PSO)
- Agents are "particles" exploring optimal task-agent mappings.
- Fitness Function:
  - Minimizes distance to task.
  - Maximizes task urgency.
  - Penalizes low stamina agents.
- Implemented using the `pyswarm` library.

#### 🔹 Genetic Algorithm (GA)
- Agents and tasks encoded as genes; task-agent matches evolve.
- Uses:
  - Roulette wheel selection
  - Single-point crossover
  - Mutation (random reassignment)
- Fitness based on same criteria as PSO.
- Implemented using the `pyeasyga` library.

#### 🔹 Fuzzy Logic
- Fuzzy Inference System evaluates:
  - **Distance** (near, medium, far)
  - **Urgency** (low, medium, high)
  - **Stamina** (low, high)
- Output: Task Priority Score
- Rule base allows nuanced decisions even under uncertainty.

---

### 🔁 Task System

- Tasks randomly spawn on the grid with:
  - Random **urgency** (1–10)
  - **Expiration time**: Removed if not picked up quickly.
  - **Progress bar** shown when an agent is working on it.
- Max concurrent tasks: **10**
- Task reassignment:
  - Expired or interrupted tasks are added back to the task pool.

---

### 👥 Multi-Agent Coordination

- Each agent independently makes assignment decisions based on the current global state.
- Agents **avoid task duplication** through shared knowledge of task status.
- No centralized controller — coordination emerges through smart local decisions.

---

### 🔄 Adaptive Behavior

- Agents dynamically adapt using:
  - Real-time optimization (PSO/GA).
  - Fuzzy logic to reassess priorities mid-movement.
  - Stamina-based thresholds to force rest cycles.
- Task urgency can cause agents to **re-prioritize** their assignments even in motion.

---

### 🎮 Visualization and UI

- Built with **Pygame**, features include:
  - Grid-based battlefield (10x10 cells)
  - Color-coded urgency indicators
  - Hover-tooltips:
    - Agents: stamina, speed
    - Tasks: urgency, time remaining
  - Visual history of completed tasks and reassignments
  - Smooth animations for agent movement

---

## 🧩 Technologies Used

| Tool/Library   | Purpose                           |
|----------------|------------------------------------|
| Python 3.x     | Core language                     |
| Pygame         | Graphics, animation, event loop   |
| pyswarm        | Particle Swarm Optimization       |
| pyeasyga       | Genetic Algorithm                 |
| NumPy          | Math operations, vector handling  |
| Custom Fuzzy   | Fuzzy logic decision engine       |

---

## 🚀 Getting Started

# 🧠 BattleTask Commander: AI Task Allocation Simulation

A Python-based interactive battlefield simulation where agents complete tasks using different optimization strategies: **Fuzzy Logic**, **Particle Swarm Optimization (PSO)**, and **Genetic Algorithm (GA)**.

---

## 🧬 Features

- 🔁 **Switch between AI modes** (Fuzzy, PSO, GA) in real-time.
- 📊 **Live visual performance charts** for comparison.
- 🧭 **Agent movement and task prioritization** logic.
- ⚔️ **Interactive battlefield grid** with agents and dynamic tasks.

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/Battle_Task_Commander.git
cd battlefield-simulation
```

### 2️⃣ Install Dependencies

If you have a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

Otherwise, install manually:

```bash
pip install pygame pyswarm pyeasyga numpy
```

---

## 🛠️ Run the Simulation

To launch the simulation, use:

```bash
python main.py
```

---

## 🎮 Controls

| Key     | Action                                                             |
|---------|--------------------------------------------------------------------|
| `P`     | Switch to **Particle Swarm Optimization (PSO)** mode              |
| `G`     | Switch to **Genetic Algorithm (GA)** mode                         |
| `F`     | Switch to **Fuzzy Logic** mode                                    |
| `C`     | Show **Agent History** chart                                      |
| `V`     | Show **Algorithm Performance Comparison** chart                   |
| `ESC`   | Exit the simulation                                               |

> 💡 *You can toggle between AI strategies at runtime. Visual output updates instantly to reflect the current mode.*

---

## 📁 Project Structure

```plaintext
battlefield-simulation/
├── main.py                # Entry point for the simulation
├── agent.py               # Agent class: stamina, movement, decision-making
├── task.py                # Task class: urgency, expiration, progress
├── battlefield.py         # Battlefield logic and grid layout
├── pso_engine.py          # PSO algorithm for task assignment
├── ga_engine.py           # Genetic Algorithm for task assignment
├── fuzzy_logic.py         # Fuzzy Logic engine for scoring
├── ui.py                  # Visualization, tooltips, charts
├── utils.py               # Helper functions (e.g., distance calculations)
└── assets/                # (Optional) Fonts, images, etc.
```

---

## 🖥️ Tips for Best Experience

- Use a Python-friendly IDE like **VS Code** or **PyCharm**.
- Run via terminal to ensure full `pygame` support.
- Avoid multitasking during simulation to prevent lag.
- If you experience choppy animations:
  - Lower agent/task count.
  - Close background apps.
  - Switch to high-performance mode on your system.

---

## 💡 Future Enhancements

> Planned features to elevate this project:

### 🔄 Reinforcement Learning Integration
- Add **Q-Learning** or **DQN** for smarter, reward-based learning agents.

### 🧭 Pathfinding with Obstacles
- Implement **A\*** or **Dijkstra’s algorithm** for realistic navigation.

### 📊 Analytics Dashboard
- Visualize stats using `matplotlib`, `seaborn`, or web dashboards:
  - Task completion time
  - Agent fatigue
  - Mode performance metrics

### 🎯 Agent Specialization
Introduce specialized roles:
- 👨‍⚕️ **Medics** – prioritize health-related tasks  
- 🔧 **Engineers** – handle technical or structural tasks  
- 🔍 **Scouts** – faster agents with less stamina

### 💾 Save & Load Simulation
- Save/load simulation states for testing or analysis.

### 🧪 Scenario-based Testing
- Predefined edge-case scenarios:
  - High urgency spikes
  - Isolated clusters
  - Low stamina agents

### ⚙️ Parameter Customization UI
- GUI to tune:
  - Agent/task count
  - Optimization method
  - Speed/stamina range
  - Urgency scaling

### 🌐 Multiplayer or Networked Mode
- Allow multiple users or AI strategies to compete/collaborate.

---

## 🤝 Contributions Welcome

Pull requests and feature ideas are appreciated!  
Open an issue to discuss your ideas or enhancements.

---

## 📚 Research Article References and Relevance

The development of **BattleTask Commander**—a dynamic AI-driven task allocation simulator in a battlefield environment—draws significant inspiration from foundational research in multi-agent coordination, swarm intelligence, and decision-making under uncertainty. Below are key academic references that guided both the design and algorithmic choices of this project:

---

### 1️⃣ [**A Novel Multi-Agent Simulation Based Particle Swarm Optimization Algorithm** – *Shuhan Du*](https://ieeexplore.ieee.org/document/8450076)

**🧠 Relevance to Project:**  
This paper presents a simulation-enhanced PSO variant tailored for complex multi-agent environments. In **BattleTask Commander**, the PSO module is inspired by the behavioral modeling proposed in this study. Specifically, it guided the formation of a fitness function that balances task urgency and agent stamina, enabling agents to collaboratively converge on optimal task assignments in real-time. The adaptive velocity adjustment and convergence strategies outlined in the paper were particularly influential in simulating responsive and intelligent agent movement.

---

### 2️⃣ [**Research on Maneuver Decision-Making of Multi-Agent Adversarial Game in a Random Interference Environment** – *Shiguang Hu*](https://ieeexplore.ieee.org/document/9690295)

**🧠 Relevance to Project:**  
This work investigates multi-agent decision-making in environments with unpredictable interference—akin to real-world battlefields. Its strategic framework informed the **Fuzzy Logic** engine in BattleTask Commander, where agents must make high-stakes decisions despite limited information and conflicting priorities. The concept of **adversarial game theory under uncertainty** helped refine the logic rules for agent prioritization, stamina decay handling, and conflict avoidance in task zones where competition between agents for resources occurs.

---

### 3️⃣ [**Particle Swarm Optimization Based Leader-Follower Cooperative Control in Multi-Agent Systems** – *Xin Wang*](https://ieeexplore.ieee.org/document/8070477)

**🧠 Relevance to Project:**  
Xin Wang’s research contributes a cooperative PSO framework using leader-follower dynamics, ideal for formations and group behavior. While **BattleTask Commander** does not yet explicitly implement leader-follower architecture, this paper shaped future plans for introducing **agent specialization and hierarchy** (e.g., Medics, Engineers, Scouts). The coordination model described in this paper serves as the theoretical backbone for enhancing agent cooperation, especially in tasks requiring synchronization or prioritization based on role capabilities.

---

## 🔍 Summary

These research articles collectively influenced the **AI behavior modeling**, **optimization strategies**, and **simulation realism** of BattleTask Commander. Their theoretical contributions are reflected in the system’s intelligent task assignment, robust performance metrics, and adaptable multi-agent interactions. The project not only validates these academic principles but also extends them into an engaging, real-time simulation context with user-controlled strategy switching and performance visualization.


## 🙌 Acknowledgments

- Concepts inspired by:
  - **Swarm Intelligence**
  - **Multi-Agent Systems**
  - **Heuristic Optimization**
- Libraries and tools:
  - [`pyswarm`](https://github.com/tisimst/pyswarm) – PSO
  - [`pyeasyga`](https://github.com/remiomosowon/pyeasyga) – GA
  - [`pygame`](https://www.pygame.org/) – Visualization engine

> Thanks to the open-source community and research that helped shape this project.

---


