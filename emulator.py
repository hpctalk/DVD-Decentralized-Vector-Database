from mpi4py import MPI
import numpy as np
import json
from Block import Block
from Node import Node
from SharedStorage import SharedStorage
from ProofOfVectorEmbedding import proof_of_vector_embedding
import datetime      # To keep track of time, as each block has its own timestamp (exact date and time at which the block is created)
import hashlib       # For finding hashes for the blocks
import requests
import dvd  # Assuming dvd is a module or library for handling the vector database

# DVD setup
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

def add_data_to_dvd(client, vector_data):
    for vector in vector_data:
        properties = {
            "fossilFuelandIndustry": vector[0],
            "landUseChangeEmissions": vector[1],
            "atmosphericGrowth": vector[2],
            "oceanSink": vector[3],
            "landSink": vector[4],
            "budgetImbalance": vector[5]
        }
        client.data_object.create(
            data_object=properties,
            class_name=CLASS_NAME,
        )

def query_dvd(client, query):
    return client.query.get(class_name=CLASS_NAME, properties=query)

def update_dvd_entry(client, object_id, updated_properties):
    client.data_object.update(
        data_object=updated_properties,
        class_name=CLASS_NAME,
        uuid=object_id
    )

def delete_dvd_entry(client, object_id):
    client.data_object.delete(class_name=CLASS_NAME, uuid=object_id)

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # DVD Client initialization
    client = dvd.Client(DVD_URL)

    # Root node initializes DVD class schema
    if rank == 0:
        create_dvd_class()

    comm.Barrier()  # Ensure all nodes wait until the class is created

    # Initialize shared storage and nodes
    shared_storage = SharedStorage()
    nodes = [Node(i) for i in range(size)]

    # Load vector data from JSON URL
    json_file_url = 'http://example.com/path/to/global-carbon-budget.json'
    vector_data = load_vector_data_from_json(json_file_url)
    total_vectors = vector_data.shape[0]

    # Calculate the batch size for each node
    batch_size = 200  # Local cache limit for each node
    start_index = rank * batch_size
    end_index = start_index + batch_size if rank != size - 1 else total_vectors

    # Ensure not to exceed the total vectors
    end_index = min(end_index, total_vectors)

    # Each node gets its own batch of vectors
    local_vectors = vector_data[start_index:end_index]

    # Create blocks with local vectors and add to shared storage
    for i in range(0, len(local_vectors), batch_size):
        batch_vectors = local_vectors[i:i + batch_size]
        block = Block(vector_data=batch_vectors)
        shared_storage.add_block(block)

        # Add vector data to DVD
        for vector in batch_vectors:
            properties = {
                "fossilFuelandIndustry": vector[0],
                "landUseChangeEmissions": vector[1],
                "atmosphericGrowth": vector[2],
                "oceanSink": vector[3],
                "landSink": vector[4],
                "budgetImbalance": vector[5]
            }
            client.data_object.create(properties, CLASS_NAME)

    # Call the proof_of_vector_embedding function
    proof_of_vector_embedding(block, nodes, shared_storage)

    # Save shared storage to a file (emulating a shared storage saving)
    if rank == 0:
        with open('shared_blockchain.json', 'w') as f:
            json.dump([block.__dict__ for block in shared_storage.get_blocks()], f)

if __name__ == "__main__":
    main()
