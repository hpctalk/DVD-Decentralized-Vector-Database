from mpi4py import MPI
import numpy as np
from collections import deque
from blockchain_vector_indexing import BlockchainVectorIndexing
from block import Block  # Assuming Block class is defined in block.py in the same directory
import datetime      # To keep track of time, as each block has its own timestamp (exact date and time at which the block is created)
import json          # For encoding the blocks before hashing them
import hashlib       # For finding hashes for the blocks
import weaviate
import timeit

class LightweightVectorInMemoryDataManager:
    def __init__(self, max_blocks, similarity_metric_selector):
        self.max_blocks = max_blocks
        self.B_i = deque()  # In-memory block list
        self.I = {}  # Index structure
        self.blockchain_indexing = BlockchainVectorIndexing([], similarity_metric_selector)

    def calculate_relevance_score(self, block):
        return np.random.rand()  # Placeholder for relevance score calculation

    def replace_block(self, b_o, b):
        self.B_i.remove(b_o)
        self.B_i.append(b)

    def append_block(self, b):
        if len(self.B_i) >= self.max_blocks:
            self.B_i.popleft()
        self.B_i.append(b)

    def Vector_Block_Manager(self, C_i, b):
        b_o = min(self.B_i, key=self.calculate_relevance_score)
        if self.calculate_relevance_score(b_o) < self.calculate_relevance_score(b):
            self.replace_block(b_o, b)
        else:
            self.append_block(b)
        self.blockchain_indexing.V = list(self.B_i)
        self.blockchain_indexing.index_vectors()
