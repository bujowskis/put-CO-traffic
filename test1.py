import instance as ins
import inputreader

# firstly, we load the instance of a problem from a file

instance1 = inputreader.readInput("example-graphs/a.txt")
# instance now contains the data about the city and cars

# now, based on the instance, we specify the schedule that maximizes
# the prize

schedules_uniform = instance1.uniform_schedules()
schedules_uniform.export('schedule_1.txt')

# now evaluate the performance
score1 = instance1.simulate(schedules_uniform, do_print=True)
print(score1)


print("\n\n\n\n")

instance2 = inputreader.readInput("example-graphs/a1.txt")
schedules_uniform2 = instance2.uniform_schedules()
print(schedules_uniform == schedules_uniform2)
schedules_uniform2.export('schedule_2.txt')
score2 = instance2.simulate(schedules_uniform2, do_print=True)
print(score2)


instance3 = inputreader.readInput("example-graphs/a3.txt")
schedules_uniform3 = instance3.uniform_schedules()
print(schedules_uniform == schedules_uniform3)
schedules_uniform3.export('schedule_2.txt')
score3 = instance3.simulate(schedules_uniform3, do_print=True)
print(score3)