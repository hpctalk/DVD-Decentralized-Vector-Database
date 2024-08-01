# DVD-Decentralized-Vector-Database powered by high-performance blockchain protocol for reliable scientific computing
## Quick Start

### Prerequisites

- **Python 3.0 or later**
- **MPI**: Ensure `mpiexec` is available (part of an MPI implementation).
- **Python Packages**:
  - `datetime`
  - `json`
  - `hashlib`
  - `requests`
  - `mpi4py`
  - `numpy`
  - `weaveate`
  - A library for your vector database (assuming it is `dvd` in your case).

**Install required Python packages:**

pip install numpy requests mpi4py

### DVD Setup
Ensure your vector database (DVD) service is running and accessible. You can run this service directly on your machine, on a HPC cluster or use a cloud-based service.


**proof_of_vector_embedding.py**

def proof_of_vector_embedding(block, nodes, shared_storage):
    # Implement the vector embedding validation and consensus logic
    pass

**emulator.py:** The Emulator should be called for processing the vector data

**emulator_query.py:** The Emulator should be called for querying the vector data

### Running the MPI Program
Start the VDB service: Ensure your VDB (DVD) service is running and accessible.

**Add vector object:** mpiexec -n <number_of_nodes> python emulator.py, Here `number_of_nodes` indicates the size of the blockchain network.

**Query vector object:** mpiexec -n <number_of_nodes> python emulator_query.py

### Verification
VDB Interface: Check the VDB interface at http://localhost:8080 to ensure the data is being added.
Results: Verify the results from the MPI processes and the data in the VDB

### Notes:
**In-memory Caching:** Each MPI node caches up to 200 blocks of vector data locally. Adjust the batch size as needed.

**Shared Storage:** Shared storage is emulated using a JSON file (shared_blockchain.json) where the blockchain data is saved. This file can be accessed and shared among all nodes.

**Vector-Database**: The blockchain database is saved to shared_blockchain.json. This file can be found in the directory where the script is run. To distribute this file among nodes in a real-world scenario, consider using a distributed file system or a shared network drive.
