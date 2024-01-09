import random
import numpy as np

from typing import Tuple, List
from abc import ABC, abstractmethod


class Process:
    def __init__(
        self, id: int, arrival_time: int, burst_time: int, priority: str = "low"
    ) -> None:
        self.id = id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority


class Algorithm(ABC):
    def __init__(self, name) -> None:
        self.name = name
        self.__steps = []

    def add_step(self, id: int, start: int, size: int) -> None:
        self.__steps.append({"id": id, "start": start, "size": size})

    @abstractmethod
    def schedule(self, processes):
        pass

    def get_steps(self):
        combined = []
        for step in self.__steps:
            if (
                combined
                and step["id"] == combined[-1]["id"]
                and step["start"] == combined[-1]["start"] + combined[-1]["size"]
            ):
                combined[-1]["size"] += step["size"]
            else:
                combined.append(step.copy())
        return combined


class FirstComeFirstServe(Algorithm):
    """
    processes must be sorted by arrival time
    """

    def __init__(self) -> None:
        super().__init__("FCFS")

    def schedule(self, processes) -> Tuple[int, int, int]:
        current_time = 0
        context_switches = 0
        wait_times = []

        for process in processes:
            if current_time < process.arrival_time:
                current_time = process.arrival_time

            first_response_time = current_time - process.arrival_time
            wait_times.append(first_response_time)
            self.add_step(process.id, current_time, process.burst_time)

            current_time += process.burst_time
            if process != processes[0]:
                context_switches += 1

        return context_switches, current_time, wait_times


class RoundRobin(Algorithm):
    """
    processes must be sorted by arrival time
    """

    def __init__(self, quantum: int) -> None:
        super().__init__("RoundRobin")

        self.quantum = quantum

    def schedule(self, processes) -> Tuple[int, int, int]:
        current_time = 0
        context_switches = 0
        process_queue = processes.copy()
        wait_times = [0] * len(processes)
        last_start_time = [0] * len(processes)

        while process_queue:
            _process = process_queue.pop(0)

            if current_time < _process.arrival_time:
                current_time = _process.arrival_time

            if current_time >= last_start_time[_process.id - 1]:
                wait_times[_process.id - 1] += (
                    current_time - last_start_time[_process.id - 1]
                )

            execution_time = min(_process.burst_time, self.quantum)
            _process.burst_time -= execution_time
            self.add_step(_process.id, current_time, execution_time)

            current_time += execution_time
            last_start_time[_process.id - 1] = current_time

            if _process.burst_time > 0:
                process_queue.append(_process)
                context_switches += 1

        return context_switches, current_time, wait_times


class MultiLevelQueue(Algorithm):
    def __init__(self, quantum: int) -> None:
        super().__init__("MLQ")
        self.quantum = quantum

    def schedule(self, processes) -> Tuple[int, int, int]:
        high_priority = [p for p in processes if p.priority == "high"]
        low_priority = [p for p in processes if p.priority == "low"]

        current_time = 0
        context_switches = 0
        wait_times = [0] * len(processes)
        last_start_time = [0] * len(processes)

        while high_priority or low_priority:
            next_process = None
            if high_priority and high_priority[0].arrival_time <= current_time:
                next_process = high_priority.pop(0)
            elif low_priority and low_priority[0].arrival_time <= current_time:
                next_process = low_priority.pop(0)

            if next_process:
                if next_process.priority == "high":
                    execution_time = min(next_process.burst_time, self.quantum)
                    next_process.burst_time -= execution_time
                    self.add_step(next_process.id, current_time, execution_time)

                    if current_time >= last_start_time[next_process.id - 1]:
                        wait_times[next_process.id - 1] += (
                            current_time - last_start_time[next_process.id - 1]
                        )

                    current_time += execution_time
                    last_start_time[next_process.id - 1] = current_time

                    if next_process.burst_time > 0:
                        high_priority.append(next_process)
                        context_switches += 1

                elif next_process.priority == "low":
                    execution_time = min(next_process.burst_time, 1)
                    next_process.burst_time -= execution_time
                    self.add_step(next_process.id, current_time, execution_time)

                    if current_time >= last_start_time[next_process.id - 1]:
                        wait_times[next_process.id - 1] += (
                            current_time - last_start_time[next_process.id - 1]
                        )

                    wait_times[next_process.id - 1] += (
                        current_time - next_process.arrival_time
                    )

                    current_time += execution_time
                    last_start_time[next_process.id - 1] = current_time

                    if next_process.burst_time > 0:
                        low_priority.insert(0, next_process)
            else:
                current_time += 1

        return context_switches, current_time, wait_times


class Scheduler:
    def __init__(self) -> None:
        self.processes = []
        self.metrics = {}

    def add_process(self, process) -> None:
        self.processes.append(process)

    def run_algorithm(self, algorithm, display=True) -> None:
        context_switches, current_time, wait_times = algorithm.schedule(self.processes)
        self.calculate_metrics(context_switches, current_time, wait_times)
        if display:
            self.display_metrics(algorithm.name)

    def calculate_metrics(
        self, context_switches: int, current_time: int, wait_times: int
    ) -> None:
        total_turnaround_time = 0
        for process in self.processes:
            total_turnaround_time += wait_times[process.id - 1] + process.burst_time

        average_wait_time = sum(wait_times) / len(self.processes)
        average_turnaround_time = total_turnaround_time / len(self.processes)
        throughput = len(self.processes) / current_time
        fairness_index = np.std(wait_times)

        self.metrics = {
            "average_wait_time": average_wait_time,
            "average_turnaround_time": average_turnaround_time,
            "throughput": throughput,
            "fairness_index": fairness_index,
            "context_switches": context_switches,
        }

    def set_processes(self, processes) -> None:
        self.processes = processes

    def get_metrics(self) -> dict:
        return self.metrics

    def display_metrics(self, name) -> None:
        print(f"Evaluating {name}")
        for metric, value in self.metrics.items():
            print(f"{metric.replace('_', ' ').title()}: {value:.2f} Einheiten")
        print()


def create_test_processes() -> List[Process]:
    processes = [
        Process(1, 0, 2, "low"),
        Process(2, 2, 4, "high"),
        Process(3, 2, 3, "low"),
        Process(4, 10, 4, "high"),
    ]
    return processes


def create_processes(
    num_processes: int = 100,
    mean_burst_time: int = 3,
    std_dev_burst: float = np.sqrt(5),
    percentage_high_priority: float = 0.1,
) -> List[Process]:
    processes = []

    base_arrival_time = 0
    for i in range(num_processes):
        burst_time = max(
            1, int(round(np.random.normal(mean_burst_time, std_dev_burst)))
        )
        priority = "high" if random.random() < percentage_high_priority else "low"
        arrival_time = max(0, int(base_arrival_time))

        process = Process(
            id=i + 1,
            arrival_time=arrival_time,
            burst_time=burst_time,
            priority=priority,
        )
        processes.append(process)

        base_arrival_time += max(0, round(random.uniform(-2, 5)))

    return processes


def create_linechart_metrics(
    algorithms: List[Algorithm],
    steps: int = 10,
    stepsize: int = 1_000,
    metric: str = "average_turnaround_time",
) -> List[np.ndarray]:
    dataset = []
    processes = []
    for algorithm in algorithms:
        stats = []
        for _ in range(steps):
            processes.extend(create_processes(num_processes=stepsize))
            scheduler = Scheduler()
            scheduler.set_processes(processes)
            scheduler.run_algorithm(algorithm, display=False)
            metrics = scheduler.get_metrics()
            stats.append(metrics[metric])
        dataset.append(np.array(stats))
    return dataset


def schedule_processes(algorithm: Algorithm, processes=None) -> None:
    scheduler = Scheduler()

    if not processes:
        processes = create_test_processes()

    for process in processes:
        scheduler.add_process(process)

    scheduler.run_algorithm(algorithm)

    return algorithm.get_steps()
