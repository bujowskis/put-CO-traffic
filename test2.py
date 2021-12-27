import time
import inputreader

# firstly, we load the instance of a problem from a file

instance1 = inputreader.readInput("example-graphs/b.txt")
# instance now contains the data about the city and cars

# now, based on the instance, we specify the schedule that maximizes
# the prize

schedules_uniform = instance1.uniform_schedules()
schedules_uniform.export('schedule_1.txt')

# now evaluate the performance
start_time = time.time()
score1 = instance1.simulate(schedules_uniform, do_print=False)
print(score1)
print(f'time elapsed: {time.time() - start_time}')
