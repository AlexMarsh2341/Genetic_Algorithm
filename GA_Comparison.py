import pandas as pd
from matplotlib import pyplot as plt

#extract data from both csv files and store in lists for plotting
unconstrained_results = pd.read_csv("fitness_results.csv")
constrained_results = pd.read_csv("constrained_fitness_results.csv")

unconstrained_best = unconstrained_results["Best Fitness Unconstrained"].tolist()
unconstrained_mean = unconstrained_results["Mean Fitness Unconstrained"].tolist()
constrained_best = constrained_results["Best Fitness Constrained"].tolist()
constrained_mean = constrained_results["Mean Fitness Constrained"].tolist()

plt.plot(unconstrained_best, label="Unconstrained Best")
plt.plot(unconstrained_mean, label="Unconstrained Mean")
plt.plot(constrained_best, label="Constrained Best")
plt.plot(constrained_mean, label="Constrained Mean")

plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.title("Fitness Comparison: Constrained vs Unconstrained")
plt.legend()
plt.savefig("Comparison.png")

#Do solutions change?
#Yes, the solutions do change. The constrained version of the algorithm is designed to find solutions that
#satisfy certain constraints, which may lead to different optimal solutions compared to the unconstrained version.
#The unconstrained version may find solutions that are optimal in terms of fitness but do not meet the constraints,
#while the constrained version will focus on finding solutions that meet the constraints,
#even if they are not as optimal in terms of fitness.

#Are solutions more realistic?
#Yes, the solutions found by the constrained version of the algorithm are more realistic because the
#constraints are designed to reflect real-world limitations and requirements.
#By adding constraints, the algorithm is forced to find solutions that are actually feasible in the real world.

#Does performance improve or degrade?
#The performance of the algorithm may degrade slightly when constraints are added,
#as it may take longer to find solutions that satisfy the constraints, depending on how long the while loops
#take to generate a valid solution.

#Does convergence change?
#The convergence of the algorithm does not change significantly when constraints are added, with both the original and
#constrained versions showing similar convergence paths and usually converging to one result by generation 10.
#This is because the actual process of the genetic algorithms are the same, with the only difference being
#the addition of constraints in the constrained version, which just limits the solution space.

#Does the search space effectively shrink?
#Yes, the search space effectively shrinks when constraints are added, as the algorithm is only able to explore
#solutions that satisfy the constraints, since any solution that does not meet the constraints is regenerated.

#How does diversity change?
#When constraints are added, the diversity of the solutions seems to decrease, since the algorithm is limited to
#the exploration of a smaller search space, leading to more similar solutions being found in later generations.
#Additionally, the mutation function is more limited in the constrained version, with some mutations being
#off-limits due to the constraints, which also contributes to the decrease in diversity.

#Optimal solutions?
#In the constrained algorithm, the program sometimes converges to different potential optimal solutions,
#unlike the unconstrained version, which always converges to the same solution. The unconstrained algorithm
#usually converges to a small house with good insulation, pellet heating, an energy saving control style,
#and a target temperature of 16 degrees. This solution has the lowest fitness cost out of all the potential
#optimal solutions, at approximately 71500. However, it may also converge to a system where all parameters are
#the same, except for the control style, which is normal, a system where all parameters are the same, except for
#the target temperature, which is 17 degrees, or a system where all parameters are the same, except the target
#temperature, which is 18 degrees. Overall, the target temperature seems to be the most variable parameter
#within the potential optimal solutions.
#The best system from the original algorithm, a small house with good insulation, geothermal heating,
#a normal control style, and a low target temperature, is not permitted because of our first constraint,
#which bans small houses from using geothermal heating.

#Do constraints improve solution quality or only realism?
#In this case, the constraints do not improve solution quality in terms of fitness cost, as the unconstrained system
#produced optimal solutions with lower fitness costs than the constrained system. However, the constraints are
#more realistic, as they prevent the algorithm from finding solutions that would not be feasible in the real world.

#Are some solutions no longer reachable?
#Yes, some solutions are no longer reachable when constraints are added, as the algorithm is only able to explore
#solutions that satisfy the constraints. For example, the best solution from the original algorithm, a small house
#with good insulation, geothermal heating, a normal control style, and a low target temperature, is no longer reachable
#because of the constraint that bans small houses from using geothermal heating.

#Does the algorithm behave differently?
#The algorithm itself does not behave differently in terms of its process, as the genetic algorithm is still the same,
#with only minor differences in the mutation and crossover aspects of the algorithm to make sure that invalid solutions
#are not generated. The only difference is that the valid search space is now limited by the constraints given.

#Can a solution be optimal but invalid?
#Yes. A solution can be optimal in terms of fitness cost, but if it does not satisfy the constraints,
#it is considered invalid and cannot be accepted as a solution. For example, the best solution from the
#original algorithm, a small house with good insulation, geothermal heating, a normal control style, and
#a low target temperature, is optimal in terms of fitness cost but is invalid due to the constraint
#that bans small houses from using geothermal heating.

#When should constraints be hard vs soft?
#Constraints should be hard when they represent absolute limitations or requirements that cannot be violated,
#such as safety regulations or physical limitations. Soft constraints can be used when they represent preferences
#or guidelines that can be violated to some extent, such as cost or performance targets. In this case, the
#constraints I added are hard constraints, as they represent limitations on the types of solutions that
#are feasible in the real world.

#How does representation affect performance?
#The representation of the solutions can affect the performance of the algorithm, as it can influence how easily
#the algorithm can explore the search space and find optimal solutions. For example, if the representation
#is too complex or too simple, it may make it more difficult for the algorithm to find optimal solutions. In this case,
#the representation of the solutions is relatively simple, with only a few parameters, which allows the
#algorithm to explore the search space effectively and find optimal solutions. However, if the representation were
#more complex, with more parameters or more complex interactions between parameters, it may make it more
#difficult for the algorithm to find optimal solutions, as it would have to explore a larger search space and
#deal with more complex interactions between parameters.

#How does this relate to symbolic AI (LAB2)?
#The use of constraints in genetic algorithms can be related to symbolic AI in that both approaches involve
#the use of rules or constraints to guide the search for solutions. In symbolic AI, rules
#are used to represent knowledge and guide the reasoning process, while in genetic algorithms, constraints are
#used to limit the search space and guide the algorithm towards feasible solutions. Both approaches can be
#used to solve complex problems, but they do so in different ways, with symbolic AI relying
#on explicit rules and reasoning, while genetic algorithms rely on evolutionary processes and optimization.