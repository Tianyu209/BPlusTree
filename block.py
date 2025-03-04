class Block:
    """Block representing a disk block containing records."""
    def __init__(self, block_size):
        self.block_size = block_size
        self.records = []
    def can_add(self, record):
        size_used = sum(r.size() for r in self.records) if self.records else 0
        return size_used + record.size() <= self.block_size
    def add_record(self, record):
        self.records.append(record)