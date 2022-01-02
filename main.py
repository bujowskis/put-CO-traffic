import inputreader3
import objects3 as obj
import instance3 as ins
import time

# main program
# todo


def main():
    # todo - see the differences; explain why greedy not always the best approach
    # firstly, we load the instance of a problem from a file
    files = ["a.txt", "b.txt", "c.txt", "d.txt", "e.txt", "f.txt"]
    files1 = ["a.txt", "e.txt"]  # todo - remove after done testing
    print("***** *** greedy ***** ***")
    for file in files:
        print(file)
        instance = inputreader3.readInput("example-graphs/{}".format(file))
        schedules_greedy = instance.greedy()
        # schedules_greedy.export(f'{file[0]}-greedy.txt')
        start_time = time.time()
        score1 = instance.simulate(schedules_greedy)
        end_time = time.time()
        score2 = instance.simulate(schedules_greedy)  # todo - remove; this checks if simulate() cleanup works
        end_time2 = time.time()
        print(f'score1: {score1},\t\t time: {end_time - start_time}\nscore2: {score2},\t\t time2: {end_time2 - end_time}\n')

    print("\n***** *** intelligent uniform ***** ***")
    for file in files:
        print(file)
        instance = inputreader3.readInput("example-graphs/{}".format(file))
        schedules_intelligent = instance.intelligent_uniform_schedules()
        # schedules_intelligent.export(f'{file[0]}-intelligent.txt')
        start_time = time.time()
        score1 = instance.simulate(schedules_intelligent)
        end_time = time.time()
        score2 = instance.simulate(schedules_intelligent)  # todo - remove; this checks if simulate() cleanup works
        end_time2 = time.time()
        print(f'score1: {score1},\t\t time: {end_time - start_time};\nscore2: {score2},\t\t time2: {end_time2 - end_time}\n')

    return 0


main()
