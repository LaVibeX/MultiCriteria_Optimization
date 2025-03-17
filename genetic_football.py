import pandas as pd
import random
import matplotlib.pyplot as plt
import os
from src.download_dataset  import download_fifa_dataset
from src.visualizers import visualize_lineup

# Check if the dataset exists, otherwise download it
dataset_path = "data/fifa23.csv"
if not os.path.exists(dataset_path):
    dataset_path = download_fifa_dataset()

# Load FIFA dataset
df = pd.read_csv(dataset_path)

# Filter for Atlético de Madrid avoid SettingWithCopyWarning
atletico = df[df['Club Name'] == 'Atlético de Madrid'].copy()

# Normalize the 'Value(in Euro)' column using .loc
atletico.loc[:, 'Normalized Cost'] = (
    (atletico['Value(in Euro)'] - atletico['Value(in Euro)'].min()) /
    (atletico['Value(in Euro)'].max() - atletico['Value(in Euro)'].min())
)
# Define formations and positions
formations = {
    '4-3-3': ['GK', 'LB', 'CB1', 'CB2', 'RB', 'CM1', 'CM2', 'CM3', 'LW', 'RW', 'ST'],
    '4-4-2': ['GK', 'LB', 'CB1', 'CB2', 'RB', 'LM', 'CM1', 'CM2', 'RM', 'ST1', 'ST2'],
    '4-3-2-1': ['GK', 'LB', 'CB1', 'CB2', 'RB', 'CM1', 'CM2', 'CM3', 'CAM1', 'CAM2', 'ST'],
    '3-4-3': ['GK', 'CB1', 'CB2', 'CB3', 'LM', 'CM1', 'CM2', 'RM', 'LW', 'RW', 'ST'],
    '4-5-1': ['GK', 'LB', 'CB1', 'CB2', 'RB', 'LM', 'CM1', 'CM2', 'CM3', 'RM', 'ST'],
    '4-1-4-1': ['GK', 'LB', 'CB1', 'CB2', 'RB', 'CDM', 'LM', 'CM1', 'CM2', 'RM', 'ST']
}

# Role stats mapping
role_stats = {
    'GK': 'Goalkeeper Reflexes',
    'CB1': 'Defending Total',
    'CB2': 'Defending Total',
    'CB3': 'Defending Total',
    'LB': 'Defending Total',
    'RB': 'Defending Total',
    'CDM': 'Defending Total',
    'CM1': 'Passing Total',
    'CM2': 'Passing Total',
    'CM3': 'Passing Total',
    'LM': 'Dribbling Total',
    'RM': 'Dribbling Total',
    'CAM1': 'Dribbling Total',
    'CAM2': 'Dribbling Total',
    'LW': 'Pace Total',
    'RW': 'Pace Total',
    'ST': 'Shooting Total',
    'ST1': 'Shooting Total',
    'ST2': 'Shooting Total'
}

# Opponent strengths
opponent_strength = {
    'attacker': {'Shooting Total': 1.0, 'Defending Total': 0.3},
    'defensive': {'Shooting Total': 0.3, 'Defending Total': 1.0},
    'combined': {'Shooting Total': 0.7, 'Defending Total': 0.7}
}

# Genetic Algorithm Components
def create_chromosome(formation):
    selected_players = []
    available_players = atletico.copy()

    for role in formations[formation]:
        stat = role_stats.get(role, 'Overall')
        player = available_players.sort_values(by=stat, ascending=False).iloc[0]
        player = player.copy()
        player['Assigned Role'] = role
        selected_players.append(player)
        available_players = available_players[available_players['Full Name'] != player['Full Name']]

    return {'formation': formation, 'players': pd.DataFrame(selected_players)}

def fitness(chromosome, opponent_type):
    performance = sum([
        opponent_strength[opponent_type].get('Shooting Total', 0.5) * player['Shooting Total'] +
        opponent_strength[opponent_type].get('Defending Total', 0.5) * player['Defending Total']
        for _, player in chromosome['players'].iterrows()
    ])
    
    # Sum of normalized costs (to minimize)
    total_cost = chromosome['players']['Normalized Cost'].sum()
    
    # Fitness with performance weight and cost penalty
    return performance - (0.5 * total_cost)  # Adjust the weight as needed

def crossover(parent1, parent2):
    split = len(parent1['players']) // 2
    child_players = pd.concat([
        parent1['players'].iloc[:split],
        parent2['players'].iloc[split:]
    ]).drop_duplicates(subset='Full Name').reset_index(drop=True)
    return {'formation': parent1['formation'], 'players': child_players}

def mutation(chromosome):
    if random.random() < 0.2:
        swap_index = random.randint(0, len(chromosome['players']) - 1)
        available_players = atletico[~atletico['Full Name'].isin(chromosome['players']['Full Name'])]
        if not available_players.empty:
            new_player = available_players.sample(1).iloc[0]
            new_player['Assigned Role'] = chromosome['players'].iloc[swap_index]['Assigned Role']
            chromosome['players'].iloc[swap_index] = new_player
    return chromosome

def run_genetic_algorithm(opponent_type):
    population = [create_chromosome(random.choice(list(formations.keys()))) for _ in range(30)]
    for _ in range(10):
        population.sort(key=lambda x: fitness(x, opponent_type), reverse=True)
        selected = population[:10]
        offspring = []

        while len(offspring) < len(population):
            parent1, parent2 = random.sample(selected, 2)
            child = crossover(parent1, parent2)
            child = mutation(child)
            offspring.append(child)

        population = offspring

    return max(population, key=lambda x: fitness(x, opponent_type))

# Run and visualize
for opponent in ['attacker', 'defensive', 'combined']:
    best_solution = run_genetic_algorithm(opponent)
    formation = best_solution['formation']
    total_cost = best_solution['players']['Value(in Euro)'].sum()

    print(f"\nBest Formation Against {opponent.capitalize()}: {formation}")
    print(f"Total Spending: €{total_cost:,.0f}")
    print(best_solution['players'][['Full Name', 'Assigned Role', 'Overall', 'Shooting Total', 'Defending Total', 'Value(in Euro)']])
    visualize_lineup(best_solution, f'Best Formation vs {opponent.capitalize()} Team')
