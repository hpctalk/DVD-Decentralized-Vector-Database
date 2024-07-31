from Block import Block  # Importing Block to manage blocks
import datetime      # To keep track of time, as each block has its own timestamp (exact date and time at which the block is created)
import json          # For encoding the blocks before hashing them
import hashlib       # For finding hashes for the blocks
import weaviate
import timeit

class Blockchain:
    def __init__(self):
        self.blocks = []

    def add_block(self, block):
        if not isinstance(block, Block):
            raise ValueError("Input must be an instance of Block class.")
        
        self.blocks.append(block)

    def contains(self, block):
        if not isinstance(block, Block):
            raise ValueError("Input must be an instance of Block class.")
        
        return any((block.get_vector_data() == b.get_vector_data()).all() for b in self.blocks)

    def get_blocks(self):
        return self.blocks
