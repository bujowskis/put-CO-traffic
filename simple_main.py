import inputreader3


def main():
    """
    reads the instance from stdin, outputs the schedule to stdout
    """
    instance = inputreader3.readInputFromStdIn()

    schedules_greedy = instance.greedy()
    schedules_greedy.export()
    return 0
