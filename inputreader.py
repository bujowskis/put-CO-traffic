import instance as ins
import objects as obj


def readInput(filepath) -> ins.Instance:
    """
    Reads the input file, returns all parameters necessary for the simulation

    :param filepath: path to the input text file
    :return: object of type Instance, with all the parameters assigned according to the specification in filepath
    """
    if filepath is None:
        raise Exception("no filepath provided")

    simulation = ins.Instance()
    with open(filepath, "r") as file:
        # first line
        line = file.readline().split()
        simulation.duration = int(line[0])
        simulation.no_intersections = int(line[1])
        simulation.no_streets = int(line[2])
        simulation.no_cars = int(line[3])
        simulation.bonus = int(line[4])

        # intersections
        simulation.intersections = [obj.Intersection(i) for i in range(simulation.no_intersections)]

        # streets
        for i in range(simulation.no_streets):
            line = file.readline().split()
            street = obj.Street(line[2], int(line[3]))
            simulation.intersections[int(line[1])].streets_in.add(street)
            simulation.streets[line[2]] = street

        # cars

        for i in range(simulation.no_cars):
            line = file.readline().split()
            path_strings = line[1:len(line)]
            car = obj.Car(streetObjectsAsPath(path_strings, simulation.streets), i+1)

            # first (beginning) street
            street = simulation.streets[line[1]]
            street.cars_total += 1
            street.queue.put(car)

            # rest of the streets
            for j in range(1, len(line)-1):  # no need to add to total count for the last street
                simulation.streets[line[j]].cars_total += 1

    return simulation


def streetObjectsAsPath(path_strings, streets_dict: dict):
    """
    Given the path represented as street names, returns the path represented
    by street objects
    """
    path_objects = []
    for street_string in path_strings:
        path_objects.append(streets_dict[street_string])
    return path_objects



