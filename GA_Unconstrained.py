#chosen parameters:
#house size (small, medium, large)
#insulation quality (poor, normal, good)
#heating type (pellets, oil, electric, geothermal)
#target temperature (integer between 16 and 22 degrees)
#control type (normal, aggressive, energy_saver)

#initializing one singular solution
class Heating_System:
    def __init__(self, size, insulation, heating_type, target_temp, control_type):
        self.size = size
        self.insulation = insulation
        self.heating_type = heating_type
        self.target_temp = target_temp
        self.control_type = control_type

    #string representation of our heating system
    def __repr__(self):
        return (f"HeatingSystem(size={self.size}, "
                f"insulation={self.insulation}, "
                f"heating={self.heating_type}, "
                f"target={self.target_temp}, "
                f"controlType={self.control_type})")


# calculating heat loss for my simulation model
def heat_loss(indoor, outdoor, size, insulation):
    loss = 0
    if (outdoor > indoor):  # if it is hotter outside than inside, the house shouldn't lose any heat
        return loss
    else:
        heat_loss = indoor - outdoor
        if (size == "small"): #small houses lose less heat than large houses, so their multiplier is smaller
            heat_loss = heat_loss * 0.2
        elif (size == "medium"):
            heat_loss = heat_loss * 0.3
        elif (size == "large"):
            heat_loss = heat_loss * 0.4
        if (insulation == "poor"): #houses with poor insulation lose more heat, so their multiplier is larger
            heat_loss = heat_loss * 0.4
        elif (insulation == "normal"):
            heat_loss = heat_loss * 0.3
        elif (insulation == "good"):
            heat_loss = heat_loss * 0.2
        return heat_loss


# determines whether we turn the heat on or not
def control_decision(indoor, target, control_type):
    if (control_type == "normal"):  # normal heating, uses moderate amount of energy, attempts to keep indoor temp within 2 degrees of target temp
        if (indoor < target - 2):
            return True
        return False
    elif (control_type == "aggressive"):  # if the house is below the target temperature, the control will start heating
        if (indoor < target):
            return True
        return False
    elif (control_type == "energy_saver"):  # uses less energy at cost of comfort, attempts to keep indoor temp within 4 degrees of target temp
        if (indoor < target - 4):
            return True
        return False


# determines how much power is used by each heating type, which is divided to find how much the temperature of the house changes
def heating_power(heating_type):
    if (heating_type == "oil"):  # I did some research to find which heating systems use the most and least energy
        return 3500
    elif (heating_type == "electric"):  # the actual values are (not incredibly accurate) estimations of watts
        return 2500
    elif (heating_type == "pellets"):
        return 1800
    elif (heating_type == "geothermal"):
        return 1200
    else:
        return "invalid heating type."


# actually simulating the behavior of the heating system
def simulate(system, temps):
    indoor_temp = system.target_temp
    energy = 0
    comfort_pen = 0

    for out_temp in temps:
        heat_loss_found = heat_loss(indoor_temp, out_temp, system.size, system.insulation)  # determine heat loss using our function

        # determine if heating is on using our function
        heating_on = control_decision(indoor_temp, system.target_temp, system.control_type)

        heat_gained = 0
        if (heating_on):
            heat_gained = (heating_power(system.heating_type)) / 2000  # determines the temperature increase caused by the heating system
            energy += heating_power(system.heating_type)  # determines the amount of watts used to heat the house

        # updates indoor temperature based on changes in heat found above
        indoor_temp = indoor_temp - heat_loss_found + heat_gained

        # finding and assigning a penalty for comfort and increasing penalty for big temperature swings
        deviation = abs(indoor_temp - system.target_temp)
        if (abs(heat_gained - heat_loss_found) > 3):
            deviation *= 1.2
        comfort_pen += deviation

    #modifiers to make fitness function slightly more accurate, based on real world assumptions
    if (system.heating_type == "geothermal"):
        comfort_pen *= 1.1
    elif (system.heating_type == "oil"):
        comfort_pen *= 0.9
    if (system.control_type == "aggressive"):
        energy *= 1.05

    return (energy, comfort_pen)

def heating_cost(energy, heating_type): #determine the cost of the energy used, to help determine fitness
    unit_price = 0
    if(heating_type=="oil"): #I did some research to find which heating systems are the most expensive per unit
        unit_price = 0.011   #and this is the order I found
    elif(heating_type=="electric"): #these are not actual prices, but closer to proportional cost (not completely accurate)
        unit_price = 0.0105
    elif(heating_type=="pellets"):
        unit_price = 0.0095
    elif(heating_type=="geothermal"):
        unit_price = 0.009
    else:
        return "invalid heating type."
    cost = energy * unit_price
    return cost

def get_fitness(system, temps): #returns fitness value, smaller = better
    #weights
    energy_weight = 0.004 #needs to be small because energy is measured in thousands
    cost_weight = 0.4 #other weights can be more normal sizes, since they are not starting with such large values
    comfort_weight = 0.5 #we want each element of the fitness value to have roughly the same amount of influence
    (energy, comfort_pen) = simulate(system, temps)
    cost = heating_cost(energy, system.heating_type)
    fitness = (energy_weight * energy) + (cost_weight * cost) + (comfort_weight * comfort_pen)
    return fitness


import random

# function that creates a random solution in the space, to be used in creation of full population
def random_solution():
    size = random.choice(["small", "medium", "large"])
    insulation = random.choice(["poor", "normal", "good"])
    heating_type = random.choice(["pellets", "oil", "electric", "geothermal"])
    target_temp = random.randint(16, 22)
    control_type = random.choice(["normal", "aggressive", "energy_saver"])

    return Heating_System(size, insulation, heating_type, target_temp, control_type)


# initializing population of random solutions of a chosen size
def initialize_population(size):
    return [random_solution() for _ in range(size)]


# selecting solutions based on fitness
def selection(pop, fit_scores):
    selected = []
    pop_size = len(pop)

    for x in range(int(pop_size / 2)):  # only select half of the size so that we can add the more fit solutions to the next generation
        competitors = random.sample(range(pop_size), 2)  # pick 2 solutions to compete, better will be chosen
        winner = competitors[0]
        for i in competitors:
            if (fit_scores[i] < fit_scores[winner]):  # the better of the two solutions will be selected
                winner = i
        selected.append(pop[winner])

    return selected


def crossover(p1, p2):  # chooses the child's attributes randomly based on the parents' attributes
    if (random.random() < 0.5):
        size = p1.size
    else:
        size = p2.size
    if (random.random() < 0.5):
        insulation = p1.insulation
    else:
        insulation = p2.insulation
    if (random.random() < 0.5):
        h_type = p1.heating_type
    else:
        h_type = p2.heating_type
    if (random.random() < 0.5):
        target = p1.target_temp
    else:
        target = p2.target_temp
    if (random.random() < 0.5):
        control = p1.control_type
    else:
        control = p2.control_type
    return Heating_System(size, insulation, h_type, target, control)


def mutate(solution, mutation_rate):
    if (random.random() < mutation_rate):
        solution.target_temp += random.uniform(-2, 2)
        solution.target_temp = max(16, min(22, solution.target_temp))  # need to make sure the mutated value stays within original range
    if (random.random() < mutation_rate):  # categorical variables get assigned a random value if they do mutate
        solution.size = random.choice(["small", "medium", "large"])
    if (random.random() < mutation_rate):
        solution.insulation = random.choice(["poor", "normal", "good"])
    if (random.random() < mutation_rate):
        solution.heating_type = random.choice(["pellets", "oil", "electric", "geothermal"])
    if (random.random() < mutation_rate):
        solution.control_type = random.choice(["normal", "aggressive", "energy_saver"])
    return solution

def evaluate_solution(system, temps): #evaluates a single solution, giving the energy used, cost, and comfort penalty, to help analyze different solutions
    energy, comfort_pen = simulate(system, temps)
    cost = heating_cost(energy, system.heating_type)
    fitness = get_fitness(system, temps)
    return {
        "system": system,
        "fitness": fitness,
        "energy": energy,
        "cost": cost,
        "comfort": comfort_pen
    }

#main genetic algorithm function, which creates a population, selects parents, creates offspring, and mutates offspring for a chosen number of generations
def genetic_algorithm(size, generations, temps):
    population = initialize_population(size)
    best_history = []
    mean_history = []
    for gen in range(generations):
        fitness_scores = []
        for sol in population:  # finding fitness of each solution
            fitness = get_fitness(sol, temps)
            fitness_scores.append(fitness)

        # getting information to help analyze convergence
        best = min(fitness_scores)
        mean = sum(fitness_scores) / len(fitness_scores)
        best_history.append(best)
        mean_history.append(mean)

        selected_parents = selection(population, fitness_scores)  # selecting best parents

        offspring = []
        for i in range(int(size / 2)):  # creating new children using crossover, only creates 1/2 the size to leave room for the fit parents
            parents = random.sample(selected_parents, 2)
            child = crossover(parents[0], parents[1])
            offspring.append(child)

        for c in offspring:  # introduce random mutation to next generation
            mutate(c, 0.1)

        population = offspring  # assign half-sized next generation as population, starting the cycle again
        population.extend(selected_parents)  # allow best parents to survive into next generation

        #creating lists to hold the different values of each parameter in the population
        all_sizes=[]
        all_insulations=[]
        all_heating_types=[]
        all_target_temps=[]
        all_control_types=[]
        #adding the different values of each parameter to the lists
        for sol in population:
            if((sol.size not in all_sizes)): all_sizes.append(sol.size)
            if((sol.insulation not in all_insulations)): all_insulations.append(sol.insulation)
            if((sol.heating_type not in all_heating_types)): all_heating_types.append(sol.heating_type)
            all_target_temps.append(sol.target_temp)
            if((sol.control_type not in all_control_types)): all_control_types.append(sol.control_type)
        avg_tt = sum(all_target_temps) / len(all_target_temps)

        #printing the number of different values of parameters and avg temperature to analyze population diversity
        print("Number of sizes: " + str(len(all_sizes))
              + ", Number of insulations: " + str(len(all_insulations))
              + ", Number of heating types: " + str(len(all_heating_types))
              + ", Average target temp: " + str(avg_tt)
              + ", Number of control types: " + str(len(all_control_types)))

    #recomputing fitness of final population to find the true best solution
    final_results = [evaluate_solution(sol, temps) for sol in population]

    print('\nFinal Population Diversity:')
    #creating lists to hold the different values of each parameter in the final population
    all_sizes = []
    all_insulations = []
    all_heating_types = []
    all_target_temps = []
    all_control_types = []
    #adding the different values of each parameter to the lists
    for sol in population:
        if ((sol.size not in all_sizes)): all_sizes.append(sol.size)
        if ((sol.insulation not in all_insulations)): all_insulations.append(sol.insulation)
        if ((sol.heating_type not in all_heating_types)): all_heating_types.append(sol.heating_type)
        all_target_temps.append(sol.target_temp)
        if ((sol.control_type not in all_control_types)): all_control_types.append(sol.control_type)
    avg_tt = sum(all_target_temps) / len(all_target_temps)

    #printing the number of different values of parameters and avg temperature to analyze final population diversity
    print("Number of sizes: " + str(len(all_sizes))
          + ", Number of insulations: " + str(len(all_insulations))
          + ", Number of heating types: " + str(len(all_heating_types))
          + ", Average target temp: " + str(avg_tt)
          + ", Number of control types: " + str(len(all_control_types)))

    print("\nTop 5 Solutions")
    #function to help sort the final results by fitness
    def get_fitness_value(result):
        return result["fitness"]

    #finding top 5 solutions based on fitness
    top5 = sorted(final_results, key=get_fitness_value)[:5]

    for r in top5:
        print(f"{r['system']} | "
              f"Fitness: {r['fitness']:.2f}, "
              f"Energy: {r['energy']:.2f}, "
              f"Cost: {r['cost']:.2f}, "
              f"Comfort: {r['comfort']:.2f}")

    #the best solution is the first one in the top 5, since they are sorted by fitness
    best_result = top5[0]

    print("\nBest Solution:")
    print(best_result["system"])
    print(f"Fitness: {best_result['fitness']:.2f}")
    print(f"Energy: {best_result['energy']:.2f}")
    print(f"Cost: {best_result['cost']:.2f}")
    print(f"Comfort penalty: {best_result['comfort']:.2f}")

    return best_history, mean_history

import pandas as pd
import matplotlib.pyplot as plt

weather_data = pd.read_csv("open-meteo-63.16N14.69E312m.csv", skiprows=3) #converting csv into temperature data I can use
temps = weather_data["temperature_2m (°C)"][:8760].tolist() #this includes time for one year, because there are 8760 hours in a year
best, mean = genetic_algorithm(60, 20, temps)

results = pd.DataFrame({ #saving results in a pandas dataframe
    "Generation": range(1, len(best) + 1),
    "Best Fitness Unconstrained": best,
    "Mean Fitness Unconstrained": mean
})
results.to_csv("fitness_results.csv", index=False) #saving results in a csv file

plt.plot(best, label="Best Fitness")
plt.plot(mean, label="Mean Fitness")

plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.legend()
plt.title("Heating System Convergence")

plt.savefig("Convergence.png")

#What type of systems perform best?
#in my algorithm, the best system came up most often during my tests. The best system is a small house
#with good insulation, geothermal heating, a normal control style, and a low target temperature.
#This is because a small house with good insulation has less heat loss then any other combination, so there is less heating need.
#Additionally, a low target temperature causes less heating need.
#And, geothermal heating is the cheapest, which lowers energy need and costs.
#Finally, a normal control style provides a healthy middle between comfort and energy use, which helps to keep the fitness value low.

#How important is insulation compared to heating system choice?
#insulation is more important than heating system choice because the insulation multiplier is applied to the heat loss amount
#every hour, which affects total energy and the comfort penalty. The heating system choice only affects the price of the energy
#and how fast the house gets heated

#Do different configurations perform similarly?
#based on my graph, there must be some configurations that perform similarly to the optimal solution,
#because the average value on the graph never converges to the best solution, so there have to be other solutions that are surviving
#because they are very close to the optimal solution.
#although the algorithm converges strongly toward one dominant solution,
#other near-optimal configurations do survive in the population with similar fitness values

#Are there trade-offs between cost and comfort?
#yes. One example of this considers the different options for control strategies. If you choose the aggressive control
#strategy, the temperature will stay close to the target, causing better comfort, but greater cost.
#if you choose the energy saver control strategy, it will save costs, but it will also reduce comfort.
#another example is the different options for heating types. If you choose oil, the house will heat faster
#but it will use more energy and be more expensive. If you choose geothermal heating, the house will heat slower,
#but it will use less energy and be less expensive.
