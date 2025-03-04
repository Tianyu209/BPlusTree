class Record:
    """Record representing an NBA game with attributes from games.txt."""
    def __init__(self, game_date, team_id_home, pts_home, fg_pct_home, ft_pct_home, fg3_pct_home, ast_home, reb_home, home_team_wins):
        self.game_date = game_date
        self.team_id_home = int(team_id_home)
        self.pts_home = int(pts_home)
        self.FG_PCT_home = float(fg_pct_home)
        self.FT_PCT_home = float(ft_pct_home)
        self.FG3_PCT_home = float(fg3_pct_home)
        self.ast_home = int(ast_home)
        self.reb_home = int(reb_home)
        self.home_team_wins = int(home_team_wins)
    def serialize(self):
        return f"{self.game_date},{self.team_id_home},{self.pts_home},{self.FG_PCT_home},{self.FT_PCT_home},{self.FG3_PCT_home},{self.ast_home},{self.reb_home},{self.home_team_wins}"
    def size(self):
        return len(self.serialize().encode('utf-8'))

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
