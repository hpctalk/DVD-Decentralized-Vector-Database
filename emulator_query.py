from mpi4py import MPI
import numpy as np
import json
import hashlib
import requests
import dvd  # Assuming dvd is a module or library for handling the vector database
from SharedStorage import SharedStorage
from Node import Node
from Block import Block

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

def load_queries_from_json(json_file_url):
    response = requests.get(json_file_url)
    queries = response.json()
    return queries

def lightweight_query_manager(query, nodes, shared_storage, reverify=False):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Step 1: Find relevant data in in-memory blocks
    local_blocks = nodes[rank].block_list  # Local in-memory blocks
    M = find_data_in_memory(query, local_blocks)

    if not reverify:
        # Step 2: If re-verification is off
        if M is None:
            # Step 3: Find data in shared storage
            shared_blocks = shared_storage.get_blocks()
            M = find_data_in_shared_storage(query, shared_blocks)

        if M is not None:
            return M  # Return found data without further verification

    else:
        # Step 4: Re-verification process
        votes = []
        for node in nodes:
            if reverify_hash(M, node.expected_hash):
                votes.append(node)

        if len(votes) <= size // 2:
            # Step 5: Re-verify with shared storage
            shared_blocks = shared_storage.get_blocks()
            M = find_data_in_shared_storage(query, shared_blocks)
            if reverify_hash(M, shared_storage.expected_hash):
                votes.append(shared_storage)

            for node in nodes:
                if node not in votes:
                    update_ledger(node, Block(vector_data=M))

            M_v = 'valid'
        else:
            M_v = 'valid'

    if M is not None and M_v == 'valid':
        return M
    return None

def find_data_in_memory(query, local_blocks):
    # Implement this function to find data in local in-memory blocks
    for block in local_blocks:
        for vector in block.vector_data:
            if np.array_equal(vector, query):
                return vector
    return None

def find_data_in_shared_storage(query, shared_blocks):
    # Implement this function to find data in shared storage
    for block in shared_blocks:
        for vector in block.vector_data:
            if np.array_equal(vector, query):
                return vector
    return None

def reverify_hash(M, expected_hash):
    # Implement this function to reverify the hash of the data
    actual_hash = hashlib.sha256(json.dumps(M).encode()).hexdigest()
    return actual_hash == expected_hash

def update_ledger(node, block):
    # Implement this function to update the ledger of a node
    node.block_list.append(block)

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # DVD Client initialization
    client = dvd.Client(DVD_URL)

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

    # Load sample queries from JSON file
    query_file_url = 'http://example.com/path/to/sample-queries.json'
    queries = load_queries_from_json(query_file_url)

    # Example query (formatted as real vector objects)
    for query_data in queries:
        query = {
            "fossilFuelandIndustry": query_data[0],
            "landUseChangeEmissions": query_data[1],
            "atmosphericGrowth": query_data[2],
            "oceanSink": query_data[3],
            "landSink": query_data[4],
            "budgetImbalance": query_data[5]
        }

        # Run the Lightweight Query Manager
        result = lightweight_query_manager(query, nodes, shared_storage, reverify=True)

        if rank == 0:
            if result:
                print(f"Query result: {result}")
            else:
                print("No relevant data found.")

if __name__ == "__main__":
    main()
