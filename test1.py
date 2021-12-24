import instance as ins
import inputreader

# firstly, we load the instance of a problem from a file

instance = inputreader.readInput("example-graphs/a.txt")
# instance now contains the data about the city and cars

# now, based on the instance, we specify the schedule that maximizes
# the prize

schedules_uniform = instance.uniform_schedules()
schedules_uniform.export('schedule_1.txt')

# now evaluate the performance
score = instance.simulate(schedules_uniform, do_print=True)
print(score)
