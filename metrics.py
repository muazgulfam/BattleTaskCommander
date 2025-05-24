import matplotlib.pyplot as plt

def plot_performance(task_efficiency, utilization, response_time):
    labels = ['Task Eff.', 'Utilization', 'Resp. Time']
    values = [task_efficiency, utilization, response_time]
    plt.bar(labels, values)
    plt.ylim(0, 100)
    plt.title("Live Metrics")
    plt.show()
