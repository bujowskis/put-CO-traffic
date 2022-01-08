import inputreader3
import time


def main():
    files = ["a.txt", "b.txt", "c.txt", "d.txt", "e.txt", "f.txt"]
    for file in files:
        instance = inputreader3.readInput(f'example-graphs/{file}')
        print(f'{file}')
        start = time.time()
        schedules = instance.advancedGreedy()
        print(f'\ttime: {time.time() - start}')
        score = instance.simulate(schedules)
        print(f'\tscore: {score}')


main()