import inputreader3


# todo - export schedules
# todo - see the differences; explain in README.md why greedy not always the best approach
def main():
    # todo - see the differences; explain why greedy not always the best approach
    files = ["a.txt", "b.txt", "c.txt", "d.txt", "e.txt", "f.txt"]
    print("Started generating schedules\n")
    for file in files:
        print(file)
        instance = inputreader3.readInput(f'example-graphs/{file}')

        print("***** *** intelligent uniform ***** ***")
        schedules_uniform = instance.intelligent_uniform_schedules()
        print(f'\tscore = {instance.simulate(schedules_uniform)}')

        print("***** *** greedy ***** ***")
        schedules_greedy = instance.greedy()
        print(f'\tscore = {instance.simulate(schedules_greedy)}')

        print("***** *** evoKiller ***** ***")
        schedules_evo, evo_score = instance.evoKiller(12)
        print(f'\tscore = {instance.simulate(schedules_evo)}\n')

    return 0


main()
