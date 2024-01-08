from src.algorithms import FirstComeFirstServe, RoundRobin, MultiLevelQueue, schedule_processes


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
