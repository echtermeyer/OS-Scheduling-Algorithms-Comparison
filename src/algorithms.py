import copy
import random
import numpy as np

from typing import Tuple, List
from abc import ABC, abstractmethod

np.random.seed(1)
random.seed(1)


class SequenceDiagrammProcess:
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
        context_switches = 0  # Will be just the number of processes. First process is also counted as a context switch
        wait_times = []

        for process in processes:
            context_switches += 1

            # Only for edge case when the first process arrives after 0
            if current_time < process.arrival_time:
                current_time = process.arrival_time

            # Wait time is just the difference between the current time and the arrival time
            wait_times.append(current_time - process.arrival_time)
            self.add_step(process.id, current_time, process.burst_time)

            current_time += process.burst_time  # Execution until the end

        return context_switches, current_time, wait_times


class RoundRobin(Algorithm):
    """
    processes must be sorted by arrival time
    """

    def __init__(self, quantum: int) -> None:
        super().__init__("RoundRobin")

        self.quantum = quantum

    def schedule(
        self, processes: List[SequenceDiagrammProcess]
    ) -> Tuple[int, int, int]:
        current_time = 0
        context_switches = 0

        wait_times = [0] * len(processes)
        last_end_times = {process.id: process.arrival_time for process in processes}

        process_queue = copy.deepcopy(processes)

        last_process_id = -1
        while process_queue:
            current_process = process_queue.pop(0)

            # Only count context switches if the process is different
            if last_process_id != current_process.id:
                last_process_id = current_process.id
                context_switches += 1

            # Only for edge case when the first process arrives after 0
            if current_time < current_process.arrival_time:
                current_time = current_process.arrival_time

            execution_time = min(current_process.burst_time, self.quantum)
            self.add_step(current_process.id, current_time, execution_time)

            # Update wait times
            wait_times[current_process.id - 1] += (
                current_time - last_end_times[current_process.id]
            )
            last_end_times[current_process.id] = current_time + execution_time

            # Update times
            current_process.burst_time -= execution_time
            current_time += execution_time

            # Prepare for next iteration
            if current_process.burst_time > 0:
                inserted = False
                for i in range(len(process_queue)):
                    if process_queue[i].arrival_time > current_time:
                        process_queue.insert(i, current_process)
                        inserted = True
                        break
                if not inserted:
                    process_queue.append(current_process)

        return context_switches, current_time, wait_times


class MultiLevelQueue(Algorithm):
    def __init__(self, quantum: int) -> None:
        super().__init__("MLQ")
        self.quantum = quantum

    def schedule(self, processes) -> Tuple[int, int, int]:
        _processes = copy.deepcopy(processes)

        high_priority = [p for p in _processes if p.priority == "high"]
        low_priority = [p for p in _processes if p.priority == "low"]

        current_time = 0
        context_switches = 0
        wait_times = [0] * len(_processes)
        last_end_times = {process.id: process.arrival_time for process in _processes}

        last_process_id = -1
        while high_priority or low_priority:
            next_process = None
            if high_priority and high_priority[0].arrival_time <= current_time:
                next_process = high_priority.pop(0)
            elif low_priority and low_priority[0].arrival_time <= current_time:
                next_process = low_priority.pop(0)

            if next_process:
                # Use Round Robin for high priority processes
                if next_process.priority == "high":
                    # Only count context switches if the process is different
                    if last_process_id != next_process.id:
                        last_process_id = next_process.id
                        context_switches += 1

                    # Get the minimum between the burst time and the quantum. Update the burst time
                    execution_time = min(next_process.burst_time, self.quantum)
                    next_process.burst_time -= execution_time

                    # Update metrics
                    self.add_step(next_process.id, current_time, execution_time)
                    wait_times[next_process.id - 1] += (
                        current_time - last_end_times[next_process.id]
                    )
                    last_end_times[next_process.id] = current_time + execution_time

                    # Update times
                    current_time += execution_time

                    # Prepare for next iteration
                    if next_process.burst_time > 0:
                        inserted = False
                        for i in range(len(high_priority)):
                            if high_priority[i].arrival_time > current_time:
                                high_priority.insert(i, next_process)
                                inserted = True
                                break
                        if not inserted:
                            high_priority.append(next_process)

                # Use FCFS for low priority processes
                elif next_process.priority == "low":
                    # Only count context switches if the process is different
                    if last_process_id != next_process.id:
                        last_process_id = next_process.id
                        context_switches += 1

                    # Also use the minimum time unit. Reason for this is that we have to check if there will be a high-priority process arriving
                    execution_time = min(next_process.burst_time, 1)
                    next_process.burst_time -= execution_time

                    # Update metrics
                    self.add_step(next_process.id, current_time, execution_time)
                    wait_times[next_process.id - 1] += (
                        current_time - last_end_times[next_process.id]
                    )
                    last_end_times[next_process.id] = current_time + execution_time

                    # Update times
                    current_time += execution_time

                    # Prepare for next iteration
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

        # print(f"Wait times: {wait_times}, len: {len(self.processes)}")
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


def create_test_processes() -> List[SequenceDiagrammProcess]:
    processes = [
        SequenceDiagrammProcess(1, 0, 2, "low"),
        SequenceDiagrammProcess(2, 2, 4, "high"),
        SequenceDiagrammProcess(3, 2, 3, "low"),
        SequenceDiagrammProcess(4, 10, 4, "high"),
    ]
    return processes


# Think like all times are in milliseconds (ms)
def create_processes(
    num_processes: int = 100,
    mean_burst_time: int = 250,
    std_dev_burst: float = 600,
    percentage_high_priority: float = 0.2,
    arrival_time_variation: float = 100,  # Neue Variable für Ankunftszeitvariation
) -> List[SequenceDiagrammProcess]:
    processes = []
    base_arrival_time = 0
    for i in range(num_processes):
        burst_time = max(
            1, int(round(np.random.normal(mean_burst_time, std_dev_burst)))
        )
        priority = "high" if np.random.random() < percentage_high_priority else "low"

        # Anpassung der Ankunftszeit, um Clusterbildung zu simulieren
        arrival_time = max(
            0,
            int(
                base_arrival_time
                + np.random.uniform(-arrival_time_variation, arrival_time_variation)
            ),
        )

        process = SequenceDiagrammProcess(
            id=i + 1,
            arrival_time=arrival_time,
            burst_time=burst_time,
            priority=priority,
        )
        processes.append(process)

        base_arrival_time += max(
            0, round(np.random.uniform(0, 25 * arrival_time_variation))
        )

    return processes


def create_linechart_metrics(
    algorithms: List[Algorithm],
    steps: int = 10,
    stepsize: int = 1_000,
    metric: str = "average_turnaround_time",
) -> List[np.ndarray]:
    total_processes_needed = steps * stepsize
    all_processes = create_processes(num_processes=total_processes_needed)

    dataset = []
    for algorithm in algorithms:
        stats = []
        for step in range(steps):
            # Select the subset of processes for the current step
            processes = all_processes[: (step + 1) * stepsize]
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
