import random
import datetime      # To keep track of time, as each block has its own timestamp (exact date and time at which the block is created)
import json          # For encoding the blocks before hashing them
import hashlib       # For finding hashes for the blocks
import weaviate
import timeit

class Block:
    def __init__(self, block_id, hit_ratio, temperature_data, humidity_data, wind_speed_data, precipitation_data):
        self.block_id = block_id
        self.hit_ratio = hit_ratio
        self.temperature_data = temperature_data
        self.humidity_data = humidity_data
        self.wind_speed_data = wind_speed_data
        self.precipitation_data = precipitation_data
    
    def __lt__(self, other):
        return self.hit_ratio < other.hit_ratio
    
    def __repr__(self):
        return (f"Block ID: {self.block_id}, Hit Ratio: {self.hit_ratio}, "
                f"Temperature Data: {self.temperature_data}, Humidity Data: {self.humidity_data}, "
                f"Wind Speed Data: {self.wind_speed_data}, Precipitation Data: {self.precipitation_data}")
