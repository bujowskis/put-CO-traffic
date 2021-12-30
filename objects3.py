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


class Car:
    def __init__(self, path, car_id):
        self.path = path
        self.last_idx = len(path) - 1  # index of the last street
        self.current_position = 0  # index relative to the position in path
        self.next_time = 0
        self.car_id = car_id  # todo - most probably unnecessary

    def crossIntersection(self, curr_time, do_print):
        """
        car is in front of the queue, has the green light, crosses the intersection,
        enters the next street in it's path
        """
        self.path[self.current_position+1].addCar(self, curr_time, do_print)
        self.current_position += 1  # FIXME will it help??


class Intersection:
    def __init__(self, id: int):
        self.id = id
        self.streets_in = set()


class Schedules:
    """
    Schedule is a DICTIONARY of sequences of turning the lights on and off

    schedules_dict is the "readable" form - a dictionary with items in such form for each intersection:
        - key: intersection_id
        - value: list of tuples: (street_name, duration)

    schedules_functional is the "functional" form - a dictionary of tuples representing the schedule in form
                                                            (total_time, streets_intervals)
    streets_intervals - dictionary with items in form:
                                                        street: (start_green, end_green)
    """
    def __init__(self):
        self.schedules_dict = {}
        self.schedules_functional = {}

    def add_schedule(self, intersection_id, data):
        self.schedules_dict[str(intersection_id)] = data

    def add_functional_schedule(self):
        """
        run after adding all schedules in "readable" form, generates "functional" schedules based on readable ones
        """
        for intersection, tuples in self.schedules_dict:
            street_intervals = {}
            start = 0
            for street, duration in tuples:
                street_intervals[street] = (start, start + duration - 1)
                start += duration
            self.schedules_functional[intersection] = (start, street_intervals)  # at this point start = total time

    def update_readable(self):
        """
        run to change the "readable" schedule based on changes in the "functional" one
        """
        pass  # todo - probably needed for xxx algorithm

    def timeTillGreen(self, intersection: int, street: Street, time_now: int) -> int:
        # todo - consider some optimization techniques
        #   - check if it's the only active street in the schedule
        total_time, interval_dict = self.schedules_functional[intersection]
        start, end = interval_dict[street]
        cycle_time = time_now % total_time  # map current time to time in the cycle
        if start <= cycle_time:
            if cycle_time <= end:
                return 0  # green now in the cycle
            else:
                # was already green in this cycle; loop over until its time for it again
                return total_time - cycle_time + start
        else:
            # it will be green still in this cycle
            return start - cycle_time

    def export(self, filename):
        with open(filename, 'w') as out_file:
            out_file.write(f'{len(self.schedules_dict.keys())}\n')  # todo - calculate how many (do we need that?)
            for intersection_id in self.schedules_dict.keys():
                out_file.write(f'{intersection_id}\n{len(self.schedules_dict[intersection_id])}\n')
                for i in self.schedules_dict[intersection_id]:
                    out_file.write(f'{i[0].name} {i[1]}\n')
