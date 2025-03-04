from record import Record
from block import Block
class DBFile:
    """Database file representing a collection of blocks storing records."""
    def __init__(self, block_size):
        self.block_size = block_size
        self.blocks = []
        self.block_access_count = 0
    def add_record(self, record):
        if not self.blocks:
            self.blocks.append(Block(self.block_size))
        last_block = self.blocks[-1]
        if not last_block.can_add(record):
            new_block = Block(self.block_size)
            new_block.add_record(record)
            self.blocks.append(new_block)
        else:
            last_block.add_record(record)
    def get_all_records(self):
        records = []
        for block in self.blocks:
            records.extend(block.records)
        return records
    def read_block(self, index):
        self.block_access_count += 1
        return self.blocks[index]
    def reset_access_count(self):
        self.block_access_count = 0

def load_records(file_path):
    """Load records from the given file path and return a list of Record objects."""
    records = []
    with open(file_path, 'r') as f:
        next(f)
        for line in f:
            parts = line.strip().split()
            if len(parts) < 9:
                continue
            record = Record(parts[0], parts[1], parts[2], parts[3], parts[4], parts[5], parts[6], parts[7], parts[8])
            records.append(record)
    return records
