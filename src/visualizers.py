import matplotlib.pyplot as plt
import os

def draw_soccer_field():
    fig, ax = plt.subplots(figsize=(12, 8))

    # Pitch Outline & Centre Line
    plt.plot([0, 0, 100, 100, 0], [0, 100, 100, 0, 0], color="white")
    plt.plot([50, 50], [0, 100], color="white")

    # Left Penalty Area
    plt.plot([0, 0, 18, 18, 0], [30, 70, 70, 30, 30], color="white")
    
    # Right Penalty Area
    plt.plot([100, 100, 82, 82, 100], [30, 70, 70, 30, 30], color="white")

    # Left 6-yard Box
    plt.plot([0, 0, 6, 6, 0], [40, 60, 60, 40, 40], color="white")
    
    # Right 6-yard Box
    plt.plot([100, 100, 94, 94, 100], [40, 60, 60, 40, 40], color="white")

    # Prepare Circles: Center circle and penalty spots
    centre_circle = plt.Circle((50, 50), 10, color="white", fill=False)
    centre_spot = plt.Circle((50, 50), 0.5, color="white")
    left_penalty_spot = plt.Circle((11, 50), 0.5, color="white")
    right_penalty_spot = plt.Circle((89, 50), 0.5, color="white")

    # Adding circles to the plot
    ax.add_patch(centre_circle)
    ax.add_patch(centre_spot)
    ax.add_patch(left_penalty_spot)
    ax.add_patch(right_penalty_spot)

    fig.patch.set_facecolor('xkcd:forest green')
    
    # Hide axis
    plt.axis('off')
    
    return ax

# Realistic visualization coordinates
visual_positions = {
    'GK': (5, 50), 'LB': (20, 30), 'CB1': (20, 45), 'CB2': (20, 55), 'CB3': (20, 70), 'RB': (20, 80),
    'CDM': (35, 50), 'CM1': (50, 35), 'CM2': (50, 65), 'CM3': (50, 50),
    'LM': (60, 20), 'RM': (60, 80), 'CAM1': (65, 40), 'CAM2': (65, 60),
    'LW': (80, 20), 'RW': (80, 80), 'ST': (90, 50), 'ST1': (90, 40), 'ST2': (90, 60)
}

# Visualization
def visualize_lineup(solution,opponent, title):
    ax = draw_soccer_field()
    for _, player in solution['players'].iterrows():
        role = player['Assigned Role']
        x, y = visual_positions.get(role, (0, 0))
        plt.scatter(x, y, color='blue', s=300)
        plt.text(x, y, player['Full Name'], ha='center', va='center', color='white', fontsize=10, fontweight='bold')
    plt.title(title)
        # Define file name format
    filename = f"Against_{opponent}_{solution['formation']}.png"
    save_path = os.path.join("data/results", filename)  # Save inside the 'data' folder

    # Save the figure
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()