import numpy as np

from typing import Tuple
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

    @abstractmethod
    def schedule(self, processes):
        pass


class FirstComeFirstServe(Algorithm):
    def __init__(self) -> None:
        super().__init__("FCFS")

    def schedule(self, processes) -> Tuple[int, int, int]:
        current_time = 0
        context_switches = 0
        wait_times = []

        for process in processes:
            if current_time < process.arrival_time:
                current_time = process.arrival_time

            wait_time = current_time - process.arrival_time
            wait_times.append(wait_time)

            current_time += process.burst_time
            if process != processes[0]:
                context_switches += 1

        return context_switches, current_time, wait_times


class RoundRobin(Algorithm):
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
            process = process_queue.pop(0)

            if current_time < process.arrival_time:
                current_time = process.arrival_time

            if current_time >= last_start_time[process.id - 1]:
                wait_times[process.id - 1] += (
                    current_time - last_start_time[process.id - 1]
                )

            execution_time = min(process.burst_time, self.quantum)
            process.burst_time -= execution_time
            current_time += execution_time
            last_start_time[process.id - 1] = current_time

            if process.burst_time > 0:
                process_queue.append(process)
                context_switches += 1

        return context_switches, current_time, wait_times


class MultiLevelQueue(Algorithm):
    def __init__(self, quantum: int) -> None:
        super().__init__("MLQ")

        self.quantum = quantum

    def schedule(self, processes) -> Tuple[int, int, int]:
        # Separate processes by priority
        high_priority = [p for p in processes if p.priority == "high"]
        low_priority = [p for p in processes if p.priority == "low"]

        current_time = 0
        context_switches = 0
        wait_times = [0] * len(processes)
        last_start_time = [0] * len(processes)

        while high_priority or low_priority:
            # Select the next process based on priority and arrival time
            next_process = None
            if high_priority and (
                not low_priority or high_priority[0].arrival_time <= current_time
            ):
                next_process = high_priority.pop(0)
            elif low_priority and (
                not high_priority or low_priority[0].arrival_time <= current_time
            ):
                next_process = low_priority.pop(0)

            if next_process:
                if next_process.priority == "high":
                    wait_times[next_process.id - 1] = (
                        current_time - next_process.arrival_time
                    )
                    current_time += next_process.burst_time
                else:
                    # Mimic Round Robin scheduling for low priority
                    execution_time = min(next_process.burst_time, self.quantum)
                    if current_time >= last_start_time[next_process.id - 1]:
                        wait_times[next_process.id - 1] += (
                            current_time - last_start_time[next_process.id - 1]
                        )
                    next_process.burst_time -= execution_time
                    current_time += execution_time
                    last_start_time[next_process.id - 1] = current_time

                    if next_process.burst_time > 0:
                        low_priority.append(next_process)
                        context_switches += 1  # Count context switch for RR

            else:
                current_time += 1

        # Adjust context switches for the first process
        if context_switches > 0 and low_priority:
            context_switches -= 1

        return context_switches, current_time, wait_times


class Scheduler:
    def __init__(self) -> None:
        self.processes = []
        self.metrics = {}

    def add_process(self, process) -> None:
        self.processes.append(process)

    def run_algorithm(self, algorithm) -> None:
        context_switches, current_time, wait_times = algorithm.schedule(self.processes)
        self.calculate_metrics(context_switches, current_time, wait_times)
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

    def display_metrics(self, name) -> None:
        print(f"Evaluating {name}")
        for metric, value in self.metrics.items():
            print(f"{metric.replace('_', ' ').title()}: {value:.2f} Einheiten")
        print()