from typing import List

from src.algorithms import Algorithm, Process, Scheduler
from src.algorithms import FirstComeFirstServe, RoundRobin, MultiLevelQueue


def create_test_processes() -> List[Process]:
    processes = [
        Process(1, 0, 2, "low"),
        Process(2, 2, 4, "high"),
        Process(3, 2, 3, "low"),
        Process(4, 10, 4, "high"),
        
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
    mlq = MultiLevelQueue(quantum=1)

    schedule_processes(fcfs)
    print(fcfs.get_steps())
    schedule_processes(rr)
    print(rr.get_steps())
    schedule_processes(mlq)
    print(mlq.get_steps())

if __name__ == "__main__": 
    main()
