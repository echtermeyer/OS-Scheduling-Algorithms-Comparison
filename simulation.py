from typing import List

from src.algorithms import Algorithm, Process, Scheduler
from src.algorithms import FirstComeFirstServe, RoundRobin, MultiLevelQueue


def create_test_processes() -> List[Process]:
    processes = [
        Process(1, 0, 40, "low"),
        Process(2, 1, 3, "high"),
        Process(3, 2, 2, "low"),
        Process(4, 2, 4, "low"),
        Process(5, 3, 3, "low"),
        Process(6, 3, 2, "high"),
        Process(7, 6, 5, "high"),
        Process(8, 12, 3, "low"),
        Process(9, 12, 2, "high")
        
    ]
    return processes

def schedule_processes(algorithm: Algorithm) -> None:
    scheduler = Scheduler()
    processes = create_test_processes()

    for process in processes:
        scheduler.add_process(process)

    scheduler.run_algorithm(algorithm)

def main() -> None:
    fcfs = FirstComeFirstServe()
    rr = RoundRobin(quantum=2)
    mlq = MultiLevelQueue(quantum=2)

    schedule_processes(fcfs)
    schedule_processes(rr)
    schedule_processes(mlq)

if __name__ == "__main__": 
    main()
