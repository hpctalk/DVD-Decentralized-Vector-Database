import requests
import json
import numpy as np

# URL of the JSON file hosted online
json_file_url = 'https://example.com/path/to/global-carbon-budget.json'

def load_vector_data_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        vectors = []
        for d in data:
            vector = [
                d["fossilFuelandIndustry"],
                d["landUseChangeEmissions"],
                d["atmosphericGrowth"],
                d["oceanSink"],
                d["landSink"],
                d["budgetImbalance"]
            ]
            vectors.append(vector)
        return np.array(vectors)
    else:
        raise Exception(f"Failed to load data from {url}. Status code: {response.status_code}")

def main():
    try:
        vector_data = load_vector_data_from_url(json_file_url)
        print("Data loaded successfully.")
        print(f"Shape of loaded vector data: {vector_data.shape}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
