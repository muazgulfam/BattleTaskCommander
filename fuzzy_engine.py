import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

health = ctrl.Antecedent(np.arange(0, 101, 1), 'health')
distance = ctrl.Antecedent(np.arange(0, 10, 1), 'distance')
urgency = ctrl.Antecedent(np.arange(0, 11, 1), 'urgency')
assign = ctrl.Consequent(np.arange(0, 11, 1), 'assign')

#Membership Function
health.automf(3)
distance.automf(3)
urgency.automf(3)

assign['low'] = fuzz.trimf(assign.universe, [0, 0, 5])
assign['medium'] = fuzz.trimf(assign.universe, [2, 5, 8])
assign['high'] = fuzz.trimf(assign.universe, [5, 10, 10])

# Fuzzy rules
# Valid labels with automf(3) are: 'poor', 'average', 'good'
rule1 = ctrl.Rule(health['good'] & distance['poor'] & urgency['good'], assign['high'])
rule2 = ctrl.Rule(health['average'] & distance['poor'] & urgency['average'], assign['medium'])
rule3 = ctrl.Rule(health['poor'] | distance['good'], assign['low'])


# Control system
task_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
task_simulator = ctrl.ControlSystemSimulation(task_ctrl)

# Assignment function
def get_fuzzy_assignment(health_val, distance_val, urgency_val):
    task_simulator.input['health'] = health_val
    task_simulator.input['distance'] = distance_val
    task_simulator.input['urgency'] = urgency_val
    task_simulator.compute()
    return task_simulator.output['assign']
