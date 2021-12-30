from queue import Queue
from typing import List, Any, Union


class Street:
    def __init__(self, name, drive_time):
        self.name = name
        self.drive_time = drive_time
        self.queue = Queue()  # stores cars that are waiting
        # self.light_is_green = False
        self.cars_total = 0  # used by greedy
        self.light_turn_on = -1
        self.light_turn_off = -1
        self.total_schedule_time = 0
        self.cars_entered = 0
        self.cars_left = 0

    def howMuchTimeToGreen(self, t):
        if self.light_turn_on <= t % self.total_schedule_time < self.light_turn_off:
            return t % self.total_schedule_time - self.light_turn_off  # light is green( return: for how many seconds yet)
        else:
            return t % self.total_schedule_time + self.light_turn_on

        # 9
        # s1(0, 3), s2(4, 5), s3(6, 8)
        # s2, 1
        # 1 < s2[0] = 4 -> 4 - 1
        # s2, 7
        # 7 > s2[2] = 5 -> 9 - 7 + s2[0] (4)



class Car:
    def __init__(self, path, car_id, cars_in_front_in_queue_when_entered):
        self.path = path
        self.last_idx = len(path) - 1  # index of the last street
        self.current_position = 0  # index relative to the position in path
        self.on_tail = None  # becomes tuple of form (Car_behind, offset in seconds)
        self.driving = False  # True if car is currently diving down some street
        self.time_I_entered_the_street = 0
        self.cars_in_front_in_queue_when_entered = cars_in_front_in_queue_when_entered
        self.car_id = car_id
        self.entered_as = 0

    def crossIntersection(self, do_print):
        """
        car is in front of the queue, has the green light, crosses the intersection,
        enters the next street in it's path
        """
        self.path[self.current_position].cars_left += 1
        next_street = self.path[self.current_position+1]
        next_street.put(self)
        next_street.cars_entered += 1
        self.current_position += 1
        self.entered_as = next_street.cars_entered
        return self.path[self.current_position].drive_time

    def changeState(self, t, do_print):
        """
        Returns 0, if in time t, car c finishes its path,
        otherwise - expected time of next action

        There are 3 options, either in time t:
            - car finishes driving down the street s, then must be added to the
            queue of street s (or return 0 if it;s the last street in the path)
            - is in front of the queue, or was expected to be in front of the queue
            then:
                - if it is in front of the queue -> try to cross intersection
                - if it is not in front of the queue: check how much time for lights to be
                switched, and try after that time
        """

        current_street = self.path[self.current_position]
        current_street: Street
        if self.driving:
            # if that value is true, we don't need to check any other conditions
            # we know that the car is just finishing driving down current street
            # so we can safely add it to the queue (there is no longer the need of
            # linking the cars on the street, since we have all the needed data in
            # "cars_actions" and order is for sure preserved

            # if the current street is the last one
            if self.current_position == self.last_idx:
                # todo - check if enough time to drive to end
                return 0


            # add the current car to the queue of the street
            current_street.queue.put(self)
            self.driving = False

            # return the time in which the current car is expected to cross the intersection
            # (assuming the light is always green!) TODO - predict light switches
            return t + len(self.path[self.current_position].queue)

        elif self == current_street.queue[0]:  # FIXME
            # try to cross the intersection:
            waiting_time = current_street.howMuchTimeToGreen(t)
            # if the light is green, then simply pass the intersection
            if waiting_time == 0:
                drive_time = self.crossIntersection(do_print)
                self.driving = True
                return t + drive_time


            # if the light is red, then check in how many seconds it will toru green and
            # add the car to the cars_actions after that time
            return t + waiting_time


        else: # car not in front of the queue -> check how many cars in front
            # check how many cars in front in the street's queue, and how much time to switch the lights
            # and how many cars can pass in one light switch, (maybe the light is green rn?)

            cars_in_front = self.entered_as - current_street.cars_left + 1
            waiting_time_to_next_green = current_street.howMuchTimeToGreen(t)
            if waiting_time_to_next_green < 0:  # light is green
                cars_to_pass = - waiting_time_to_next_green
                if cars_in_front < cars_to_pass: # our car will cross the intersection in this light switch
                    return t + cars_in_front + 1
                else: # our car won't manage to cross the intersection in this light switch
                    # then it has to wait
                    pass # TODO
            pass  # TODO

class Intersection:
    def __init__(self, id: int):
        self.id = id
        self.streets_in = set()
        self.total_schedule_time = 0
        self.n_streets_in_schedule = 0
        self.schedule = None

        # todo - maybe lights state

class Schedules:
    """
    Schedule is a DICTIONARY of sequences of turning the lights on and off
    for each intersection:
        - key: intersection_id
        - value: list of tuples: (street_name, duration)
    """

    def __init__(self):

        self.schedules_dict = {}     # key: intersection_id
                                # value: list of tuples: (street_name, duration)

    def add_schedule(self, intersection_id, data):
        self.schedules_dict[str(intersection_id)] = data

    # def updateIntersections(self):
    #     """
    #     invoking this function will update schedules_dict for all intersections,
    #     that have their schedule specified
    #     """
    #     for schedule in self.schedules_dict:
    #         pass
    #
    # def areValid(self):
    #     """
    #     checks if the set of schedules_dict is valid
    #     """
    #     pass

    def export(self, filename):
        with open(filename, 'w') as out_file:
            out_file.write(f'{len(self.schedules_dict.keys())}\n')  # todo - calculate how many
            for intersection_id in self.schedules_dict.keys():
                out_file.write(f'{intersection_id}\n{len(self.schedules_dict[intersection_id])}\n')
                for i in self.schedules_dict[intersection_id]:
                    out_file.write(f'{i[0].name} {i[1]}\n')


