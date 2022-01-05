from inputreader3 import readInput
import time

def test():
    instance1 = readInput("example-graphs/f.txt")
    start_time = time.time()
    schedules_evo, score_evo = instance1.evoKiller(pop_size=12, timeout=30)
    schedules_evo.export("schedules_evo.txt")
    print(f'score= {score_evo}')

    print(f'time elapsed: {time.time() - start_time}')

    instance1 = readInput("example-graphs/f.txt")
    schedule_greedy = instance1.greedy()
    score_greedy = instance1.simulate(schedule_greedy)
    print(f'greedy score = {score_greedy}')

test()
