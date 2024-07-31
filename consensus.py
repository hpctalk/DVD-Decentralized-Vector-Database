from mpi4py import MPI
import numpy as np
from Block import Block  # Importing Block to create blocks
from Node import Node  # Importing Node to validate blocks
from SharedStorage import SharedStorage  # Importing SharedStorage to manage shared storage
import datetime      # To keep track of time, as each block has its own timestamp (exact date and time at which the block is created)
import json          # For encoding the blocks before hashing them
import hashlib       # For finding hashes for the blocks
import weaviate
import timeit

class Consensus:
    def __init__(self, shared_storage, total_nodes):
        if not isinstance(shared_storage, SharedStorage):
            raise ValueError("Shared storage must be an instance of SharedStorage class.")
        
        self.shared_storage = shared_storage
        self.total_nodes = total_nodes
        self.votes = set()
        self.counter = 0

    def vector_consensus(self, block, node):
        if not isinstance(block, Block):
            raise ValueError("Block must be an instance of Block class.")
        
        if not isinstance(node, Node):
            raise ValueError("Node must be an instance of Node class.")
        
        if not self.shared_storage.block_exists(block):
            if node.validate_block(block):
                self.votes.add(node.node_id)
                self.counter += 1

                if len(self.votes) > self.total_nodes / 2:
                    return True  # Consensus achieved

            if self.counter >= self.total_nodes / 2:
                if len(self.votes) <= self.total_nodes / 2:
                    self.shared_storage.add_block(block)
                return False  # Consensus not achieved

        return False  # Block already exists or consensus not achieved

