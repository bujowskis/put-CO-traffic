# put-CO-traffic
Repository for Combinatorial Optimization laboratory classes project - Traffic signaling problem statement for the Online Qualifications of Hash Code 2021

[The pdf explaining the tasks and problems of the project](https://storage.googleapis.com/coding-competitions.appspot.com/HC/2021/hashcode_2021_online_qualification_round.pdf)

## Foreword
We both had a good time working on this project. We spent some valuable time on all the things needed to make it into reality - modeling, coding and optimizing our code.

Unfortunately, we **did not finish it the way we wanted**. For our "more intelligent" algorithm, we went with Evolutionary Algorithms. The problem is, the evaluation function does not work fast enough for EA to work as it should, as the amount of generations the algorithm can go through is way too small, compared to what it usually needs.

Because of that, in most cases the results could be better, especially in the case of the instance described by `d.txt`. They are not bad though, and they're quite nice compared to the submissions to the original Hash Code competition.

Having that in mind, due to the upcoming session examination of the 3rd semester of the AI degree we're taking, we leave the project the way it is. **For now**.

Honestly, the whole project is really nice, and we're looking forward towards (potentially) revisiting it once we have some spare time to do that. In case we do, we're thinking of two ways to approach it:
1. try to optimize our code in Python in such way it's fast enough to apply a full-fledged Evolutionary Algorithm (or use some other workaround, like approximate evaluation or modeling it more like a typical flow network)
2. write it in some faster language (probably C/C++)

Regardless of the option we go for, the most important thing we're trying to convey is - **the project certainly sparked our curiosity and inspired us to do more towards this direction**.

## How it's done
### The inner structure & Evaluation
For clarity, we modeled the whole thing in object programming manner, trying to use the most appropriate structures for specific tasks to make it work as fast as possible. We still see a lot of things that could be improved though, and that's **exactly** why we're thinking of revisiting it again in the future.

The evaluation function considers each car in each iteration separately, but there are a lot of optimization things we used to speed up the process, such as boolean fields of each car indicating if it can be skipped in a given iteration, or skipping the iterations when we're sure there would be no changes happening. Unfortunately, that's still not enough for true EA. But keep in mind, we have a few ideas on what to try out next.

### The algorithms
**IMPORTANT** - see the last section of README to see the additional `advanced greedy` algorithm, and `order`.

In total, there are three algorithms we used for generating the schedules, among which the one yielding the best result is chosen (which in all cases boiled down to Evolutionary Algorithm).
#### Intelligent uniform
The most simple intelligent heuristic algorithm we could think of. It assigns 1 second of green light to each street **which is used by at least one car** in its corresponding intersection. That way, no street with a car is completely blocked.
#### Greedy
A more advanced, greedy-like heuristic. It iterates over all intersections, and assigns each of the incoming street time of green light which is proportional to how many cars go through all the other streets in that intersection.

Precisely, it normalizes the total car count by dividing it by the least total car count of some street in that intersection (which is still positive). Then the obtained value is rounded to the nearest integer, and that's exactly the amount of green time for a street. That way, the streets which are used more get a longer time

Consider the following example:
```
intersection 10
incoming streets (street_name, total_cars_count):
(street1, 0)
(street2, 10)
(street3, 13)
(street4, 17)
(street5, 44)

lowest_positive = 10

assigned times:
  street1: 0      # no time for unused streets
  street2: 1      # always 1 for the street considered lowest_positive
  street3: 1      # as much as lowest_positive, since the difference is not significant enough
  street4: 2      # the difference big enough to assign double the green time
  street5: 4      # the difference is relatively very big
```
#### evoKiller
Since there have been some compromises made considering a regular Evolutionary Algorithm couldn't be implemented given the execution time, we like to refer to this algorithm as a `Evolutionary-Algorithm-inspired Heuristic-Aided Search`. Why? It sounds ***sciency and cool***. Oh, and also it helps to get the underlying idea.
- Evolutionary-Algorithm-inspired - there exists a diverse population of **individuals** (schedules), which are chosen to be altered and introduced to the next **generations**
- Heuristic-Aided - the **mutation** is done using an additional parameter - **requests**. It's basicaly the waiting time of cars on a given street during the simulation's span. The mutation tries to address the problem by adding green time to the streets with the biggest requests (since these seem to need it the most), and decreasing it for streets with the least requests (as these may potentially not need it that much)
- Search - rather self explanatory, really

## Running the program
`main.py` is, as the name suggests, the main function which is to be run. It accepts up to 4 command line parameters, 1 of which is mandatory. The other 3 ones alter some parameters of `evoKiller`.
1. **path** to the text file containing problem instance (mandatory)
2. max **timeout time** (optional, 300s (5min) by default)
3. **population size** (optional, 12 by default)
4. **maximum number of iterations without improvement** (optional, 100 by default)

Basically, (depending what python you're using), running the program boils down to:
```
python3 b.txt
```
which is equivalent to:
```
python3 b.txt 300 12 100
```

### Solutions
The schedules generated using this version of the project and the default `evoKiller` parameters should be available in this repository, in directories `schedules` and `schedules-best`. The first one contains schedules generated using all three algorithms, whereas the latter only the ones yielding the best result, chosen from the three algorithms (which as we said, are basically the results of `evoKiller`).

## The interesting case of d.txt
This particular instance was by far the biggest pain in the ass. It always took the longest time to evaluate, up to the point when the number of generations `evoKiller` went through seemed like a joke. Nonetheless, the biggest curiosity about it is that **greedy yields 0 score for it**.

Why is that? After some thoughts we've had and analysis of the file, the answer is very intuitive. There are two factors greedy-like approach struggles with.
1. the number of incoming streets is high
2. there is some street with relatively low total cars count, and some streets with relatively great total cars count

Consider the following example:
```
intersection 15
incoming streets (street_name, total_cars_count):
(street1, 0)
(street2, 10)
(street3, 90)
(street4, 86)
(street5, 45)
(street6, 32)
(street7, 71)

lowest_positive = 10


assigned times:
  street1: 0
  street2: 1
  street3: 9
  street4: 9
  street5: 5
  street6: 3
  street7: 7

cycle_length = 34
```

In such case, the total cycle length of switching the lights in such an intersection becomes really long, and if there are lots of such intersections, eventually it may happen that all the cars will be stuck waiting for green light most of the time, potentially all the way to the most extreme point of no cars getting through at all. We're convinced that's exactly what happens in case of `d.txt`.

## Advanced greedy
This is the improvement for greedy algorithm that came to my mind while I was writing the explanation to what are the pitfalls of regular greedy algorithm we implemented. It expored the "greedy-like space" more, which proved to be a little better than `evoKiller` in case of `e.txt`. Unfortunately, that's the only such case.

The algorithm is explained in more detail in the docstrings. In general, on top of what regular greedy algorithm does, this one sequentially cuts out the streets with the lowest total car counts, and then tries out the variations of them in which the proportion between total cars count relative to the lowest total cars count is sequentially increased, up to point in which all of the remaining streets are assigned 1 second each.

Output for `e.txt`
```
***** *** Started generating schedules:
	intelligent uniform...
		done, obtained score: 684817
	greedy...
		done, obtained score: 693052
	advanced greedy...
		done, obtained score: 706968
	evoKiller...
		done, obtained score: 692667
***** *** All schedules generated
***** *** the best score obtained: 706968, by advanced greedy
	exporting this schedule...
	(done)

Process finished with exit code 0
```

## Order
An additional add-on which can be used by any algorithm, as it's applicable to `Schedules` type object directly. The idea is to order which streets appear first in every cycle, based on how many cars are waiting on the streets at the beginning of the simulation. It's the most simple heuristic which does some ordering, and it's easy to understand - in most cases, it makes the most sense to let the street with the highest initial cars count go first in the schedule.

The idea could surely be implemented in more advanced manner, and I daresay it may be what most of our algorithms are missing - namely, searching the neighbourhood of schedules with shuffled order of streets in the cycle. It's something definitiely worth trying out in the future, but for now we stick to it's simplistic version, which is still very good. In most cases, it **improved the obtained scores by anything between 1-300k points**.

## What now?
As mentioned before, for now the repository will become dormant, and we're thinking of revisiting it once again in the future. It was a nice journey and we definitely learnt a lot along the way. We're looking forward to more such projects.
