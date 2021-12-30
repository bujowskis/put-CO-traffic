from queue import SimpleQueue
from typing import List, Any, Union


class Street:
    def __init__(self, name, drive_time):
        self.name = name
        self.drive_time = drive_time
        self.queue = SimpleQueue()  # stores cars that are waiting
        self.light_is_green = False
        self.heading_car = None
        self.last_car = None
        self.cars_total = 0  # FIXME: may be redundant

    def performAction(self, curr_time, do_print):
        """
        1) "move" the car that is in the front (heading_car)
            if the car already passed the entire street, add it
            to the queue and update heading_car
        2) check if there is any car in the queue
            If there is, let this car cross the intersection
        """
        timestamps = self.updateHeadingCar(do_print, curr_time)

        if not self.queue.empty():
            car = self.queue.get()
            car.crossIntersection(curr_time, do_print)  # FIXME: crossing the intersection should
                                                        # take 1 second (now it is instant)

        return timestamps

    def addCar(self, new_car, curr_time, do_print):
        new_car: Car
        # new_car.driving = self.drive_time
        if do_print:
            print(f'car {new_car.car_id} will be added to street {self.name} in next second')
        if self.heading_car is not None:

            # self.heading_car.driving = self.drive_time ?? don't know why i'd put it here
            last_car_so_far = self.last_car
            last_car_so_far.on_tail = (new_car, curr_time - last_car_so_far.time_I_entered_the_street)
        else:
            self.heading_car = new_car
            self.last_car = new_car
        # when the car crosses  the intersection, it has no tail
        new_car.on_tail = None
        new_car.time_I_entered_the_street = curr_time + 1  # here we state that crossing the
        # intersection takes one second

    def updateHeadingCar(self, do_print, curr_time) -> list or None:
        self.heading_car: Car

        # current_car = self.heading_car
        timestamps: list[int] = []

        # if there is no car on the street or the heading car has just crossed the
        # intersection:
        if self.heading_car is None or self.heading_car.time_I_entered_the_street == curr_time:
            return None


        # the time the car should finish driving through current street
        timestamp = self.heading_car.time_I_entered_the_street + self.drive_time

        # just print how much time the car still needs
        if do_print:
            print(f'car {self.heading_car.car_id} has '
                  f'{timestamp - curr_time} secs to pass road {self.name}')



        # the following procedure has to be executed for all cars that have
        # finished driving through a given street:
        #current_car = self.heading_car

        while timestamp <= curr_time:
            # so if the car has already drove through the entire street:

            # if it is the last street in car's path
            if self.heading_car.current_position == self.heading_car.last_idx:
                if do_print:
                    print(f'car {self.heading_car.car_id} '
                          f'ends at {self.heading_car.path[-1].name} when time= {timestamp}')
                timestamps.append(timestamp)

            else:  # if it is not the last street in the car's path:
                self.heading_car.on_tail = None  # unlink the tail
                self.queue.put(self.heading_car)

            # now check the next car

            # if the current car is the last one:
            if self.heading_car.on_tail is None:
                self.heading_car = None
                self.last_car = None
                break

            else:
                if do_print:
                    print(f'    next car is car {self.heading_car.on_tail[0].car_id}')
                self.heading_car, offset = self.heading_car.on_tail
                timestamp += offset

        return timestamps

    def finalStreetCheck(self, curr_time, do_print) -> list or None:
        # fixme: remove duplicated code when everything works
        """
        Returns list of timestamps, in which cars have finished their paths
        """
        # pretty similar to updateHeadingCar method
        timestamps = []
        self.heading_car: Car  # todo - hmm??
        if self.heading_car is None:
            return None

        timestamp = self.heading_car.time_I_entered_the_street + self.drive_time
        while timestamp <= curr_time:
            # so if the car has already drove through the entire street:

            # if it is the last street in car's path
            if self.heading_car.current_position == self.heading_car.last_idx:
                if do_print:
                    print(f'finally, car {self.heading_car.car_id} '
                          f'ends at {self.heading_car.path[-1].name} when time = {timestamp}')
                timestamps.append(timestamp)

            else:  # if it is not the last street in the path:
                pass

            # now check the next car

            # if the current car is the last one:
            if self.heading_car.on_tail is None:
                self.heading_car = None
                self.last_car = None
                break

            else:
                self.heading_car, offset = self.heading_car.on_tail
                timestamp += offset

        return timestamps





    # def updateHeadingCar(self, do_print, curr_time):
    #     self.heading_car: Car
    #     """
    #     if the car that is in front reaches the end of the street, then add it to
    #     queue, make the second car the heading one
    #         (But if the street is the last one in the path, then add points to
    #         the score, delete the car)
    #     Else, update the driving time
    #
    #     This function should return:
    #         the list of timestamps in which cars have finished their driving
    #         or None if no car has finished in a given iteration
    #     """
    #
    #     #car_reaches_dest = False
    #     cars_timestamps = []
    #     if self.heading_car is not None:
    #         time_of_driving = curr_time - self.heading_car.time_I_entered_the_street
    #
    #         # if the car just crossed the intersection, it shouldn't move further
    #         # in this turn (it was already added to the street
    #         if self.heading_car.time_I_entered_the_street != curr_time:
    #
    #
    #            #self.heading_car.driving -= 1
    #             time_of_driving = curr_time - self.heading_car.time_I_entered_the_street
    #             if do_print:
    #                 print(f'car {self.heading_car.car_id} has '
    #                       f'{time_of_driving} secs to pass road {self.name}')
    #
    #         # if heading car has reached the end of the street
    #         #if self.heading_car.driving <= 0:
    #
    #
    #         # FIXME - use while loop to iterate over all tailing cars as long
    #         # as they also passed the street, (do the below operation for all
    #         # such cars)
    #         # it usually happens that some streets have the red light,
    #         # but there are some cars driving by them
    #
    #         # then, just when the street finally has green light
    #         # add the cars to the queue as long a
    #
    #         if time_of_driving >= self.drive_time:
    #             # if it is the last street in car's path
    #             if self.heading_car.current_position == self.heading_car.last_idx:
    #                 car_reaches_dest = True
    #                 if do_print:
    #                     print(f'car {self.heading_car.car_id} '
    #                           f'ends at {self.heading_car.path[-1].name}')
    #             else:
    #                 self.queue.put(self.heading_car)
    #
    #
    #             if self.heading_car.on_tail is not None:
    #                 temp_time = self.heading_car.on_tail[1]  # FIXME - it is offset, not time
    #                 self.heading_car = self.heading_car.on_tail[0]
    #                 self.heading_car.driving = temp_time   # FIXME - not using `driving` variable anymore
    #             else:
    #                 self.heading_car = None
    #                 self.last_car = None
    #     else:  # if there is no car driving through the street:
    #         pass
    #     return car_reaches_dest


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

    def crossIntersection(self, curr_time, do_print):
        """
        car is in front of the queue, has the green light, crosses the intersection,
        enters the next street in it's path
        """
        self.path[self.current_position+1].addCar(self, curr_time, do_print)
        self.current_position +=1 ## FIXME will it help??

    def changeState(self, t):
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

            # return the time in which the current car is expected to cross the intersection
            # (assuming the light is always green!) TODO - predict light switches
            return t + len(self.path[self.current_position].queue)

        elif self == current_street.queue[0]:
            # try to cross the intersection:
            pass # TODO
        else: # car not in front of the queue -> check how many cars in front
            pass # TODO



class Intersection:
    def __init__(self, id: int):
        self.id = id
        self.streets_in = set()
        self.number_of_street_that_has_green = 0  # according to the position in schedule
        self.n_streets_in_schedule = 0
        self.schedule = None
        #self.cycle_length = 0
        self.time_to_change_lights = 0
        # todo - maybe lights state

    def switchLights(self):
        """
        function used to overwrite street_that_has_green and
        update time_to_change_lights
        """
        if self.number_of_street_that_has_green == self.n_streets_in_schedule - 1:
            self.number_of_street_that_has_green = 0
        else:
            self.number_of_street_that_has_green += 1
        self.time_to_change_lights = self.schedule[self.number_of_street_that_has_green][1]

        # todo - switch-case?
        # todo - if no_of_green = streets_in_schedule: no_of_green = 0 ?
        # self.number_of_street_that_has_green = \
        #     (self.number_of_street_that_has_green + 1) % self.n_streets_in_schedule
        # self.time_to_change_lights = self.schedule[self.number_of_street_that_has_green][1]


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


