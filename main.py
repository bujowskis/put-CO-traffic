import inputreader3
import sys


def main():
    """
    Reads 3 command line parameters:
        1. max timeout time, 300s (5min) by default
        2. population size, 12 by default
        3. maximum number of iterations without improvement, 100 by default

    The generated schedules will be exported to stdout
    """
    arguments = len(sys.argv)
    if arguments == 1:
        timeout = 300
        popsize = 12
        max_no_impr = 100
    elif arguments == 2:
        popsize = 12
        max_no_impr = 100
        timeout = int(sys.argv[2])
    elif arguments == 3:
        max_no_impr = 100
        timeout = int(sys.argv[2])
        popsize = int(sys.argv[3])
    elif arguments == 4:
        timeout = int(sys.argv[2])
        popsize = int(sys.argv[3])
        max_no_impr = int(sys.argv[4])
    else:
        print("Wrong number of arguments provided")
        return -1

    instance = inputreader3.readInputFromStdIn()

    # try all three algorithms and choose the best
    schedules_intelligent = instance.intelligent_uniform_schedules()
    score_intelligent = instance.simulate(schedules_intelligent)

    schedules_advanced_greedy = instance.advancedGreedy()
    score_advanced_greedy = instance.simulate(schedules_advanced_greedy)

    schedules_evo, score_evo = instance.evoKiller(popsize, max_no_impr, timeout)
    score_evo = instance.simulate(schedules_evo)

    scores = [score_evo, score_advanced_greedy, score_intelligent]
    max_score = max(scores)

    # go in the order of increasing complexity
    if score_intelligent == max_score:
        schedules_intelligent.export()
    elif score_advanced_greedy == max_score:
        schedules_advanced_greedy.export()
    elif score_evo == max_score:
        schedules_evo.export()
    else:
        raise Exception("the impossible happened")

    return 0


main()
