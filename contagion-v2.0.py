'''
dN = E * p * N
'''
import random
import matplotlib.pyplot as plt

random.seed()

population_size = 10000
percent_isolated = 0

E = 3
p = 0.1

timesteps = 125 # days
number_of_simulations = 5

time_to_symptoms = 5
time_to_outcome = 10


def run_one_day(population, E, p):
	
	global time_to_symptoms
	global time_to_outcome
	
	for person in population:
		
		if person['infected'] == True:
			person['duration'] += 1
			
		if person['duration'] == time_to_symptoms:
			person['symptomatic'] = True
			person['isolating'] = True
			
		elif person['duration'] == time_to_outcome:
			person['immune'] = True
			person['infected'] = False
			person['symptomatic'] = False
			person['isolating'] = False
				
	not_isolating = []
	
	for person in population:
		if person['isolating'] == False:
			not_isolating += [person]
			
	for person in not_isolating:
		if person['infected'] == True:
			
			for encounter in range(E):
				other = random.choice(not_isolating)
				
				if other['immune'] == False:
			
					transmitted = random.uniform(0.0, 1.0)
					
					if transmitted <= p:
						other['infected'] = True
			
def count_infections(population):
	
	number_infected = 0
	number_showing_symptoms = 0

	for person in population:
		if person['infected'] == True:
			number_infected += 1
		if person['symptomatic'] == True:
			number_showing_symptoms += 1
				
	return [number_infected, number_showing_symptoms]

def run_one_simulation(E, p, timesteps):
	
	population = []

	global population_size
	global percent_isolated

	for i in range(population_size):
		person = { 'infected': False, 'duration': 0, 'symptomatic': False,
			'immune': False, 'isolating': False}
			
		population += [person]
		
	population[0]['infected'] = True	
	
	number_isolated = int(percent_isolated * population_size/100.0)

	for i in range(1,number_isolated):
		person = population[i]
		person['isolating'] = True
		
	infections_by_day = []

	for timestep in range(timesteps):
		run_one_day(population, E, p)
		
		infections_this_day = count_infections(population)
		
		infections_by_day += [infections_this_day]
		
		#print('Day: {} Infections: {}'.format(timestep, infections_this_day))
		
	return infections_by_day

results_all_runs = []

for i in range(number_of_simulations):
	
	print('Simulation {}'.format(i))
	
	results_this_run = run_one_simulation(E, p, timesteps)
	results_all_runs += [results_this_run]
	
number_of_infections = []
number_of_infections_w_symptoms = []

for i in range(timesteps):
	number_of_infections += [0.0]
	number_of_infections_w_symptoms += [0.0]

for result in results_all_runs:
	
	for i in range(timesteps):
		
		result_this_day = result[i]
		
		number_of_infections[i] += result_this_day[0]
		number_of_infections_w_symptoms[i] += result_this_day[1]
	
for i in range(timesteps):
	number_of_infections_w_symptoms[i] /= number_of_simulations
	number_of_infections[i] /= number_of_simulations
	number_of_infections[i] -= number_of_infections_w_symptoms[i]
	

for i in range(timesteps):
	print('Day {}: {} {}'.format(i, int(number_of_infections[i]),
		int(number_of_infections_w_symptoms[i])))
		
day_numbers = []
		
for i in range(timesteps):
	day_numbers += [i]
	
plt.plot(day_numbers, number_of_infections)
plt.plot(day_numbers, number_of_infections_w_symptoms)

plt.show()


	
