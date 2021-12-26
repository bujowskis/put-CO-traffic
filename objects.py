from queue import SimpleQueue


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
        car_reaches_dest = self.updateHeadingCar(do_print, curr_time)

        if not self.queue.empty():
            car = self.queue.get()
            car.crossIntersection(curr_time, do_print)


        return car_reaches_dest

    def addCar(self, new_car, curr_time, do_print):
        new_car: Car
        # new_car.driving = self.drive_time
        if do_print:
            print(f'car {new_car.car_id} added to street {self.name}')
        if self.heading_car is not None:
            assert(self.drive_time > 0)
            # self.heading_car.driving = self.drive_time ?? don't know why i'd put it here
            last_car_so_far = self.last_car
            last_car_so_far.on_tail = (new_car, curr_time - last_car_so_far.time_I_entered_the_street)
        else:
            self.heading_car = new_car
            self.last_car = new_car
            new_car.driving = self.drive_time
        new_car.time_I_entered_the_street = curr_time

    def updateHeadingCar(self, do_print, curr_time):
        self.heading_car: Car
        """
        if the car that is in front reaches the end of the street, then add it to
        queue, make the second car the heading one
            (But if the street is the last one in the path, then add points to
            the score, delete the car)
        Else, update the driving time
        """

        car_reaches_dest = False
        if self.heading_car is not None:
            time_of_driving = curr_time - self.heading_car.time_I_entered_the_street

            # if the car just crossed the intersection, it shouldn't move further
            # in this turn (it was already added to the street
            if self.heading_car.time_I_entered_the_street != curr_time:


               #self.heading_car.driving -= 1
                time_of_driving = curr_time - self.heading_car.time_I_entered_the_street
                if do_print:
                    print(f'car {self.heading_car.car_id} has '
                          f'{time_of_driving} secs to pass road {self.name}')

            # if heading car has reached the end of the street
            #if self.heading_car.driving <= 0:


            # FIXME - use while loop to iterate over all tailing cars as long
            # as they also passed the street, (do the below operation for all
            # such cars)
            # it usually happens that some streets have the red light,
            # but there are some cars driving by them

            # then, just when the street finally has green light
            # add the cars to the queue as long a

            if time_of_driving >= self.drive_time:
                # if it is the last street in car's path
                if self.heading_car.current_position == self.heading_car.last_idx:
                    car_reaches_dest = True
                    if do_print:
                        print(f'car {self.heading_car.car_id} '
                              f'ends at {self.heading_car.path[-1].name}')
                else:
                    self.queue.put(self.heading_car)


                if self.heading_car.on_tail is not None:
                    temp_time = self.heading_car.on_tail[1]
                    self.heading_car = self.heading_car.on_tail[0]
                    self.heading_car.driving = temp_time
                else:
                    self.heading_car = None
                    self.last_car = None
        else:  # if there is no car driving through the street:
            pass
        return car_reaches_dest


class Car:
    def __init__(self, path, car_id):
        self.path = path
        self.last_idx = len(path) - 1  # index of the last street
        self.current_position = 0  # index relative to the position in path
        self.on_tail = None  # becomes tuple of form (Car_behind, offset in seconds)
        self.driving = 0  # used for leading cars, indicated how many seconds until end of street
        self.time_I_entered_the_street = 0
        self.car_id = car_id

    def crossIntersection(self, curr_time, do_print):
        """
        car is in front of the queue, has the green light, crosses the intersection,
        enters the next street in it's path
        """
        self.path[self.current_position+1].addCar(self, curr_time, do_print)
        self.current_position +=1 ## FIXME will it help??




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

        self.number_of_street_that_has_green = \
            (self.number_of_street_that_has_green + 1) % self.n_streets_in_schedule
        self.time_to_change_lights = self.schedule[self.number_of_street_that_has_green][1]


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


