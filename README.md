# Football Optimization Project

This project optimizes football team alignments for Atlético de Madrid using Genetic Algorithms. The algorithm selects optimal player formations against hypothetical opponent types—\textit{attacker, defensive, and combined teams}—while balancing both player performance and cost minimization.

## Installation Steps

### 1. Clone the Repository
```bash
git clone <repo-link>
```

### 2. Go to the Project Directory
```bash
cd project_name
```

### 3. Create and Activate the Virtual Environment
```bash
python -m venv venv

# On Linux/Mac
source venv/bin/activate

# On Windows
.\venv\Scripts\activate
```

### 4. Install the Project Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the Project
```bash
python genetic_football.py
```

## ⚙️ Requirements
- Dataset: `fifa23.csv` (Ensure this file is located in the root or `data/` directory)
- The Scrip will automatically download the dataset if `fifa23.csv` is not found.

## 📄 Additional Notes
- If new Python packages are added, update `requirements.txt` with:
```bash
pip freeze > requirements.txt
```

- To deactivate the virtual environment:
```bash
deactivate
```

## 🗂️ Project Structure
```
project_name/
├── venv/                # Virtual environment (excluded from sharing)
├── src/                 # Python source code
├── data/                # Dataset files
├── requirements.txt     # Python dependencies
├── README.md            # Project instructions
└── genetic_football.py  # Entry point of the project
```

## 💡 Project Highlights
- **Genetic Algorithm (GA)** for lineup optimization.
- Fitness function balances performance and cost.
- Visualizes optimal player formations using Matplotlib.
- Supports multiple football formations.
- Displays total spending for each lineup.
