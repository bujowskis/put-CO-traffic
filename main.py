import inputreader3
import objects3 as obj
import instance3 as ins
import time

# main program
# todo


def main():
    # fixme - see the differences; greedy acts concerning
    # firstly, we load the instance of a problem from a file
    files = ["a.txt", "b.txt", "c.txt", "d.txt", "e.txt", "f.txt"]
    print("***** *** greedy ***** ***")
    for file in files:
        print(file)
        instance = inputreader3.readInput("example-graphs/{}".format(file))
        schedules_greedy = instance.greedy()
        start_time = time.time()
        score = instance.simulate(schedules_greedy)
        print(score)
        print("\ttime elapsed: {}".format(time.time() - start_time))

    print("\n***** *** intelligent uniform ***** ***")
    for file in files:
        print(file)
        instance = inputreader3.readInput("example-graphs/{}".format(file))
        schedules_greedy = instance.intelligent_uniform_schedules()
        start_time = time.time()
        score = instance.simulate(schedules_greedy)
        print(score)
        print("\ttime elapsed: {}".format(time.time() - start_time))

    return 0


main()
