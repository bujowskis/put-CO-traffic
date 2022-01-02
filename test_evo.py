from inputreader3 import readInput
import time

def test():
    instance1 = readInput("example-graphs/b.txt")
    start_time = time.time()
    schedules_evo, score_evo = instance1.evoKiller(pop_size=10, max_generations=1000)
    schedules_evo.export("schedules_evo.txt")
    print(f'score= {score_evo}')

    print(f'time elapsed: {time.time() - start_time}')


test()
