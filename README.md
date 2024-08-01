# DVD---Decentralized Vector Database powered by high-performance blockchain protocol for reliable scientific computing
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

pip install numpy requests mpi4py weaviate

### DVD Setup
Ensure your vector database (DVD) service is running and accessible. You can run this service directly on your machine, on a HPC cluster or use a cloud-based service.


**proof_of_vector_embedding.py**

def proof_of_vector_embedding(block, nodes, shared_storage):
    # Implement the vector embedding validation and consensus logic
    pass

**emulator.py:** The Emulator should be called for processing the vector data

**emulator_query.py:** The Emulator should be called for querying the vector data

### Running the MPI Program
Start the VDB service: Ensure your DVD service is running and accessible.

**Add vector object:** mpiexec -n <number_of_nodes> python emulator.py, Here `number_of_nodes` indicates the size of the blockchain network.

**Query vector object:** mpiexec -n <number_of_nodes> python emulator_query.py

## Docker Quick Start
**Create Dockerfile:**
Create a Dockerfile to set up the necessary environment for your application.

Use an official Python runtime as a parent image: FROM python:3.8-slim

Set the working directory in the container: WORKDIR /app

Install required system packages and MPI:  RUN apt-get update && \
    apt-get install -y build-essential openmpi-bin openmpi-common libopenmpi-dev

Install required Python packages:  RUN pip install numpy requests mpi4py weaviate

Copy the current directory contents into the container at /app:  COPY . /app

Make ports available to the world outside this container:  EXPOSE 8080

Define environment variable:  ENV NAME World

Run the command on container startup:  CMD ["mpiexec", "-n", "4", "python", "emulator.py"]

**Create Docker Compose File:**
To manage multiple Docker containers for different services, create a docker-compose.yml file

**Prepare the Project Directory:**
Ensure your project directory has the necessary files:

Dockerfile
docker-compose.yml
emulator.py
emulator_query.py
proof_of_vector_embedding.py
requirements.txt (optional, for additional Python dependencies)

**Build and Run the Docker Containers:**
Open a terminal, navigate to your project directory, and execute the following commands.

Build the Docker image: docker-compose build

Run the Docker containers: docker-compose up

**Running the MPI Program**
Add Vector Object:  docker-compose run dvd mpiexec -n <number_of_nodes> python emulator.py

Query Vector Object: docker-compose run dvd_query mpiexec -n <number_of_nodes> python emulator_query.py

Replace <number_of_nodes> with the desired number of MPI nodes.

### Verification
DVD Interface: Check the DVD interface at http://localhost:8080 to ensure the data is being added.
Results: Verify the results from the MPI processes and the data in the VDB

### Notes:
**In-memory Caching:** Each MPI node caches up to 200 blocks of vector data locally. Adjust the batch size as needed.

**Shared Storage:** Shared storage is emulated using a JSON file (shared_blockchain.json) where the blockchain data is saved. This file can be accessed and shared among all nodes.

**Vector-Database**: The blockchain database is saved to shared_blockchain.json. This file can be found in the directory where the script is run. To distribute this file among nodes in a real-world scenario, consider using a distributed file system or a shared network drive.
