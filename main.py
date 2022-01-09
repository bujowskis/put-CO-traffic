import inputreader3
import sys


def main():
    """
    Reads 4 command line parameters:
        1. path to the file containing problem instance
        2. max timeout time, 300s (5min) by default
        3. population size, 12 by default
        4. maximum number of iterations without improvement, 100 by default

    The generated schedules will be exported to the text files with self-explanatory names
    """
    arguments = len(sys.argv)
    if arguments == 2:
        timeout = 300
        popsize = 12
        max_no_impr = 100
        file_path = sys.argv[1]
        file_export_name = sys.argv[1].split('/').pop().split('.')[0]
    elif arguments == 3:
        popsize = 12
        max_no_impr = 100
        file_export_name = sys.argv[1].split('/').pop().split('.')[0]
        file_path = sys.argv[1]
        timeout = int(sys.argv[2])
    elif arguments == 4:
        max_no_impr = 100
        file_export_name = sys.argv[1].split('/').pop().split('.')[0]
        file_path = sys.argv[1]
        timeout = int(sys.argv[2])
        popsize = int(sys.argv[3])
    elif arguments == 5:
        file_export_name = sys.argv[1].split('/').pop().split('.')[0]
        file_path = sys.argv[1]
        timeout = int(sys.argv[2])
        popsize = int(sys.argv[3])
        max_no_impr = int(sys.argv[4])
    else:
        print("Wrong number of arguments provided")
        return -1

    instance = inputreader3.readInput(file_path)
    print("***** *** Started generating schedules:")

    print("\tintelligent uniform...")
    schedules_intelligent = instance.intelligent_uniform_schedules()
    score_intelligent = instance.simulate(schedules_intelligent)
    print(f"\t\tdone, obtained score: {score_intelligent}")

    print("\tadvanced greedy...")
    schedules_advanced_greedy = instance.advancedGreedy()
    score_advanced_greedy = instance.simulate(schedules_advanced_greedy)
    print(f"\t\tdone, obtained score: {score_advanced_greedy}")

    print("\tevoKiller...")
    if timeout < 10:
        print("\t\tYou're joking, right? Let's see if you get anything useful in under 10 seconds...")
    elif timeout < 120:
        print("\t\tIn case the results are not satisfactory, remember the default timeout is 300 seconds...")
    elif timeout < 300:
        print("\t\tIt will take a while. You can probably listen to a whole song while waiting.")
    elif timeout < 600:
        print(f"\t\tMaybe a short walk? You could try running 2km under {round(timeout / 60) + 2} minutes, I challenge you.")
    elif timeout < 1800:
        print("\t\tWow, you really want to see some serious count of generations.")
    elif timeout < 5400:
        print("\t\tTimeout time is getting little out of hand, you know...")
    elif timeout < 10800:
        print("\t\tIt might be a long one. You could watch a whole movie in that time.")
    elif timeout < 21600:
        print("\t\tJust remember to check on me later. Oh, and I hope the program is not interrupted.")
        print("\t\tIt would be such a waste if you didn't get the schedule after waiting so long...")
        print("\t\tWhat if I... \"accidentally\" stop it in the middle? Do you trust me? I want to play a game...")
    else:
        print("\t\tYour. Computer. Will. suffer.")
    schedules_evo, score_evo = instance.evoKiller(popsize, max_no_impr, timeout)
    score_evo = instance.simulate(schedules_evo)
    print(f"\t\tdone, obtained score: {score_evo}")

    print("***** *** All schedules generated")
    scores = [score_evo, score_advanced_greedy, score_intelligent]
    max_score = max(scores)
    # go in the order of increasing complexity
    if score_intelligent == max_score:
        print(f"***** *** the best score obtained: {score_evo}, by intelligent uniform")
        print("\texporting this schedule...")
        schedules_intelligent.exportToFile(f"{file_export_name}-best.txt")
        print("\t(done)")
    elif score_advanced_greedy == max_score:
        print(f"***** *** the best score obtained: {score_advanced_greedy}, by advanced greedy")
        print("\texporting this schedule...")
        schedules_advanced_greedy.exportToFile(f'{file_export_name}-best.txt')
        print("\t(done)")
    elif score_evo == max_score:
        print(f"***** *** the best score obtained: {score_evo}, by evoKiller")
        print("\texporting this schedule...")
        schedules_evo.exportToFile(f"{file_export_name}-best.txt")
        print("\t(done)")
    else:
        raise Exception("the impossible happened")

    return 0


main()
