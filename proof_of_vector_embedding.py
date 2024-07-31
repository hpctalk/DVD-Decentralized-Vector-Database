from mpi4py import MPI
import numpy as np
from Block import Block
from Node import Node
from SharedStorage import SharedStorage
from Blockchain import Blockchain
from Consensus import Consensus
import datetime      # To keep track of time, as each block has its own timestamp (exact date and time at which the block is created)
import json          # For encoding the blocks before hashing them
import hashlib       # For finding hashes for the blocks
import weaviate
import timeit

def vector_block_manager(C_i, b):
    b_o = min(C_i.get_recent_blocks(), key=lambda blk: np.sum(blk.get_vector_data()))
    if np.sum(b.get_vector_data()) > np.sum(b_o.get_vector_data()):
        C_i.replace_block(b_o, b)
    else:
        C_i.append_block(b)

def proof_of_vector_embedding(b, C, D):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    votes = set()
    C_l = []

    for i, node in enumerate(C):
        if rank == i:
            while len(votes) <= size / 2:
                if node.validate_block(b):
                    consensus = Consensus(D, size)
                    if consensus.vector_consensus(b, node):
                        votes.add(node.node_id)
                else:
                    C_l.append(node)
                break

    comm.Barrier()
    votes = comm.allgather(votes)
    votes = set().union(*votes)

    if len(votes) <= size / 2:
        if rank == 0:
            consensus = Consensus(D, size)
            if consensus.vector_consensus(b, Node(rank)):
                votes.add(0)
        comm.Barrier()
        votes = comm.allgather(votes)
        votes = set().union(*votes)

        if rank in [node.node_id for node in C_l]:
            D.sync_blockchain()

    if len(votes) > size / 2:
        if rank == 0:
            D.add_block(b)
        comm.Barrier()
        D_B = comm.bcast(D.get_blockchain(), root=0)
        for node in C:
            if b not in node.get_recent_blocks():
                vector_block_manager(node, b)

if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    shared_storage = SharedStorage()
    nodes = [Node(i) for i in range(size)]

    vector_data = np.random.rand(10, 128)  # 10 rows of 128-dimensional vectors
    block = Block(vector_data=vector_data)

    proof_of_vector_embedding(block, nodes, shared_storage)
