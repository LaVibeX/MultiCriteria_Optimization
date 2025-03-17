import kagglehub
import shutil
import os

def download_fifa_dataset():
    """
    Downloads the FIFA 23 dataset from Kaggle and moves it to the 'data' folder as 'fifa23.csv'.
    """
    target_folder = "data"
    os.makedirs(target_folder, exist_ok=True)

    # Define target path for the CSV file
    target_path = os.path.join(target_folder, "fifa23.csv")
    
    # Check if the dataset already exists
    if os.path.exists(target_path):
        print(f"Dataset already exists at: {target_path}")
        return target_path
    
    # Download the dataset
    print("Downloading FIFA 23 dataset from Kaggle...")
    path = kagglehub.dataset_download("sanjeetsinghnaik/fifa-23-players-dataset")

    # Locate the downloaded CSV file
    downloaded_file = next((file for file in os.listdir(path) if file.endswith('.csv')), None)

    # Move and rename the dataset file
    if downloaded_file:
        shutil.move(os.path.join(path, downloaded_file), target_path)
        print(f"Dataset downloaded and moved to: {target_path}")
    else:
        raise FileNotFoundError("No CSV file found in the downloaded dataset.")

    return target_path
