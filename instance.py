from objects import *


# contains all objects needed for the simulation
class Instance:
    """
    Contains all the information describing the simulation
    """
    def __init__(self):
        self.duration = 0           # (1 <= D <= 10^4)
        self.no_intersections = 0   # (2 <= I <= 10^5)
        self.no_streets = 0         # (2 <= S <= 10^5)
        self.no_cars = 0            # (1 <= V <= 10^3)
        self.bonus = 0              # (1 <= F <= 10^3)
        self.streets = dict()
        # self.cars = set()
        self.intersections = None   # list
        self.schedules = None  # todo - is even needed? we generate schedules_dict using greedy and xxx
        self.time = 0

    def simulate(self, schedules: Schedules, do_print=False) -> int:
        """
        Simulates the instance specified by Instance's parameters, using the given schedule



        :return: obtained score
        """

        """
        Procedure:
            In each second iterate over all intersections that has their schedule specified
                (since if no schedule for a given intersections --> all lights red forever -->
                no possibility to move)
                
            For each scheduled intersection
            1. check if the lights should switch --> 
            2. do the action (car in front of the queue crosses and appears at the beginning of
               next street of it's path)
               
            We iterate over schedules_dict, not intersections, because some of intersections have no 
            schedule, and iterating over intersections would lead to performing redundant steps
        """

        # load the schedules to the intersections
        active_intersections = []
        for intersection_id, data in schedules.schedules_dict.items():
            active_intersections.append(self.intersections[int(intersection_id)])
            active_intersections[-1].schedule = data
            active_intersections[-1].n_streets_in_schedule = len(data)
            active_intersections[-1].time_to_change_lights = data[0][1]
            #active_intersections[-1].cycle_length = sum(duration for _, duration in data)


        cur_time = 0
        score = 0
        while cur_time < self.duration:
            # first, check if it is needed to switch lights
            for i in active_intersections:
                if i.time_to_change_lights <=0:
                    i.switchLights()
                else:
                    i.time_to_change_lights -= 1






            cur_time += 1

        return score




    def uniform_schedules(self) :
        """
        this function returns the simplest schedule, that is, each street on each intersection
        has the green light for 1 second
        """
        schedules = Schedules()
        for i in self.intersections:
            data = []
            for street in i.streets_in:
                data.append((street, 1))    # schedule will store the reference to street objects, not
                                            # only their names
            schedules.add_schedule(i.id, data)

        return schedules



    def greedy(self) -> set:
        """
        Generates schedules_dict for the intersections of the instance specified by Instance's parameters using greedy
        algorithm

        :return: set of schedules_dict for the intersections
        """
        schedules = set()
        # todo

        return schedules

    def xxx(self) -> set:  # todo - choose algorithm
        """
        Generates schedules_dict for the intersections of the instance specified by Instance's parameters using todo

        :return: set of schedules_dict for the intersections
        """
        schedules = set()
        # todo

        return schedules
