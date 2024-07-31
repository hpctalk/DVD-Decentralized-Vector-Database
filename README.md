# DVD-Decentralized-Vector-Database
# Vector DB and Blockchain Setup with MPI

## Prerequisites

- **Python 3.0 or later**
- **MPI**: Ensure `mpiexec` is available (part of an MPI implementation).
- **Python Packages**:
  - `datetime`
  - `json`
  - `hashlib`
  - `requests`
  - `mpi4py`
  - `numpy`
  - A library for your VDB (assuming it is `dvd` in your case).

Install required Python packages:

```sh
pip install numpy requests mpi4py

## VDB Setup
Ensure your VDB (DVD) service is running and accessible. You can run this service directly on your machine or use a cloud-based service.

## Prepare Python Scripts
**block.py**

import numpy as np
import hashlib
import json
import datetime

class Block:
    def __init__(self, vector_data):
        self.timestamp = datetime.datetime.now()
        self.vector_data = np.array(vector_data)
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data_str = json.dumps(self.vector_data.tolist()) + str(self.timestamp)
        return hashlib.sha256(data_str.encode()).hexdigest()

    def get_vector_data(self):
        return self.vector_data
**node.py**
class Node:
    def __init__(self, id):
        self.id = id

    def validate_block(self, block):
        # Implement validation logic
        pass

**shared_storage.py**
class SharedStorage:
    def __init__(self):
        self.blockchain = []

    def add_block(self, block):
        self.blockchain.append(block)

    def get_blocks(self):
        return self.blockchain

**proof_of_vector_embedding.py**
def proof_of_vector_embedding(block, nodes, shared_storage):
    # Implement the vector embedding validation and consensus logic
    pass

**emulator.py: The Emulator should be called for processing the vector data**
from mpi4py import MPI
import numpy as np
import json
import requests
from Block import Block
from Node import Node
from SharedStorage import SharedStorage
from proof_of_vector_embedding import proof_of_vector_embedding

# Assuming DVD client is imported correctly
import dvd  

DVD_URL = 'http://localhost:8080'
CLASS_NAME = 'GlobalCarbonBudget'

def load_vector_data_from_json(json_file_url):
    response = requests.get(json_file_url)
    data = response.json()

    vectors = []
    for d in data:
        vector = [
            d["Fossil-Fuel-And-Industry"],
            d["Land-Use-Change-Emissions"],
            d["Atmospheric-Growth"],
            d["Ocean-Sink"],
            d["Land-Sink"],
            d["Budget-Imbalance"]
        ]
        vectors.append(vector)
    return np.array(vectors)

def create_dvd_class():
    client = dvd.Client(DVD_URL)
    class_obj = {
        "class": CLASS_NAME,
        "properties": [
            {"name": "year", "dataType": ["string"]},
            {"name": "fossilFuelandIndustry", "dataType": ["number"]},
            {"name": "landUseChangeEmissions", "dataType": ["number"]},
            {"name": "atmosphericGrowth", "dataType": ["number"]},
            {"name": "oceanSink", "dataType": ["number"]},
            {"name": "landSink", "dataType": ["number"]},
            {"name": "budgetImbalance", "dataType": ["number"]}
        ]
    }
    client.schema.create_class(class_obj)

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Initialize shared storage and nodes
    shared_storage = SharedStorage()
    nodes = [Node(i) for i in range(size)]

    # Load vector data from JSON URL
    json_file_url = 'http://example.com/path/to/global-carbon-budget.json'
    vector_data = load_vector_data_from_json(json_file_url)
    total_vectors = vector_data.shape[0]
    vector_dimension = vector_data.shape[1]

    # Calculate the batch size for each node
    batch_size = total_vectors // size
    start_index = rank * batch_size
    end_index = start_index + batch_size if rank != size - 1 else total_vectors

    # Each node gets its own batch of vectors
    local_vectors = vector_data[start_index:end_index]
    block = Block(vector_data=local_vectors)

    # Call the proof_of_vector_embedding function
    proof_of_vector_embedding(block, nodes, shared_storage)

if __name__ == "__main__":
    create_dvd_class()  # Create the class in DVD
    main()

## Running the MPI Program
Start the VDB service: Ensure your VDB (DVD) service is running and accessible.

Run the MPI program:
mpiexec -n 4 python emulator.py

## Verification
VDB Interface: Check the VDB interface at http://localhost:8080 to ensure the data is being added.
Results: Verify the results from the MPI processes and the data in the VDB
