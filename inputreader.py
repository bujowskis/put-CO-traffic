import simulation as sim
import objects as obj


def readInput(filepath) -> sim.Simulation:
    """
    Reads the input file, returns all parameters necessary for the simulation

    :param filepath: path to the input text file
    :return: todo - add all returns
    """
    if filepath is None:
        raise Exception("no filepath provided")

    simulation = sim.Simulation()
    with open(filepath, "r") as file:
        # first line
        line = file.readline().split()
        simulation.duration = int(line[0])
        simulation.no_intersections = int(line[1])
        simulation.no_streets = int(line[2])
        simulation.no_cars = int(line[3])
        simulation.bonus = int(line[4])

        # streets todo
        for i in range(simulation.no_streets):
            line = file.readline().split()
            simulation.streets.add(obj.Street())

        # cars todo

        # intersections todo

    return simulation
