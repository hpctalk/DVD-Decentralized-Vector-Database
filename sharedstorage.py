from Blockchain import Blockchain
from Block import Block
from mpi4py import MPI
import datetime      # To keep track of time, as each block has its own timestamp (exact date and time at which the block is created)
import json          # For encoding the blocks before hashing them
import hashlib       # For finding hashes for the blocks
import weaviate
import timeit

class SharedStorage:
    def __init__(self):
        self.blockchain = Blockchain()

    def add_block(self, block):
        if not isinstance(block, Block):
            raise ValueError("Input must be an instance of Block class.")
        
        self.blockchain.add_block(block)

    def block_exists(self, block):
        if not isinstance(block, Block):
            raise ValueError("Input must be an instance of Block class.")
        
        return self.blockchain.contains(block)

    def get_blockchain(self):
        return self.blockchain

    def sync_blockchain(self):
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        size = comm.Get_size()

        # Gather all blockchains from nodes
        all_blockchains = comm.gather(self.blockchain.get_blocks(), root=0)

        if rank == 0:
            # Flatten the list of lists of blocks into a single list of blocks
            all_blocks = [block for blockchain in all_blockchains for block in blockchain]

            # Remove duplicates based on the vector data
            unique_blocks = []
            seen_vectors = set()
            for block in all_blocks:
                vector_data_tuple = tuple(map(tuple, block.get_vector_data()))
                if vector_data_tuple not in seen_vectors:
                    seen_vectors.add(vector_data_tuple)
                    unique_blocks.append(block)

            # Sort blocks by some criterion if needed, e.g., timestamp
            unique_blocks.sort(key=lambda b: np.sum(b.get_vector_data()))

            # Create a new synchronized blockchain
            synced_blockchain = Blockchain()
            for block in unique_blocks:
                synced_blockchain.add_block(block)
            
            self.blockchain = synced_blockchain

        # Broadcast the synchronized blockchain to all nodes
        synced_blockchain = comm.bcast(self.blockchain, root=0)
        self.blockchain = synced_blockchain
