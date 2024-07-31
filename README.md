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

**Install required Python packages:**

pip install numpy requests mpi4py

## VDB Setup
Ensure your VDB (DVD) service is running and accessible. You can run this service directly on your machine or use a cloud-based service.


**proof_of_vector_embedding.py**

def proof_of_vector_embedding(block, nodes, shared_storage):
    # Implement the vector embedding validation and consensus logic
    pass

**emulator.py:** The Emulator should be called for processing the vector data

## Running the MPI Program
Start the VDB service: Ensure your VDB (DVD) service is running and accessible.
mpiexec -n 4 python emulator.py

## Verification
VDB Interface: Check the VDB interface at http://localhost:8080 to ensure the data is being added.
Results: Verify the results from the MPI processes and the data in the VDB
