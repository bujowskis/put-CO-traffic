import inputreader3
import time


def main():
    files = ["a.txt", "b.txt", "c.txt", "d.txt", "e.txt", "f.txt"]
    for file in files:
        instance = inputreader3.readInput(f'example-graphs/{file}')
        print(f'{file}')

        print("uniform")
        start = time.time()
        schedules = instance.intelligent_uniform_schedules()
        print(f'\ttime: {time.time() - start}')
        score = instance.simulate(schedules)
        print(f'\tscore: {score}')
        schedules_ordered = schedules.order_initqueue_first()
        score = instance.simulate(schedules_ordered)
        print(f'\tscore (ordered): {score}')

        print("greedy")
        start = time.time()
        schedules = instance.greedy()
        print(f'\ttime: {time.time() - start}')
        score = instance.simulate(schedules)
        print(f'\tscore: {score}')
        schedules_ordered = schedules.order_initqueue_first()
        score = instance.simulate(schedules_ordered)
        print(f'\tscore (ordered): {score}')

        print("advanced greedy")
        start = time.time()
        schedules = instance.advancedGreedy()
        print(f'\ttime: {time.time() - start}')
        score = instance.simulate(schedules)
        print(f'\tscore: {score}')
        schedules_ordered = schedules.order_initqueue_first()
        score = instance.simulate(schedules_ordered)
        print(f'\tscore (ordered): {score}')


main()