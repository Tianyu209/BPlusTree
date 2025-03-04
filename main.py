import time
from storage import Record, DBFile, load_records
from bptree import BPTree
import pandas as pd

def build_storage(records, block_size):
    """Build storage by creating a DBFile and adding records."""
    db = DBFile(block_size)
    for record in records:
        db.add_record(record)
    return db

def build_index_iterative(db, order):
    """Build a B+ tree using the iterative insertion method."""
    tree = BPTree(order)
    for record in db.get_all_records():
        tree.insert(record.FG_PCT_home, record)
    tree.fix_leaf_links()
    return tree

def get_data_block_accesses(db, records):
    """Simulate data block accesses for a list of records by counting unique blocks accessed."""
    accessed = set()
    for i, block in enumerate(db.blocks):
        for record in block.records:
            if record in records:
                accessed.add(i)
    return len(accessed)

def linear_scan(db, key_min, key_max):
    """Perform a linear scan over all blocks to find records with FG_PCT_home in the given range."""
    results = []
    db.reset_access_count()
    start = time.time()
    for i in range(len(db.blocks)):
        block = db.read_block(i)
        for record in block.records:
            if key_min <= record.FG_PCT_home <= key_max:
                results.append(record)
    end = time.time()
    return results, db.block_access_count, end - start

def print_report(storage_stats, iterative_index_stats, bulk_index_stats, iterative_search_stats, bulk_search_stats, linear_search_stats,boolean):
    """Print report statistics for storage, indexing, and search operations."""
    print("Storage Component Statistics:")
    print("Record size:", storage_stats["record_size"])
    print("Total number of records:", storage_stats["total_records"])
    print("Number of records per block:", storage_stats["records_per_block"])
    print("Total number of blocks:", storage_stats["total_blocks"])
    print("")
    if boolean:
        print("Iterative B+ Tree Statistics:")
        print("B+ tree order (n):", iterative_index_stats["order"])
        print("Total number of index nodes:", iterative_index_stats["index_nodes"])
        print("Number of levels in B+ tree:", iterative_index_stats["levels"])
        print("Root node keys:", iterative_index_stats["root_keys"])
        print("")
    print("Bulk Loading B+ Tree Statistics:")
    print("B+ tree order (n):", bulk_index_stats["order"])
    print("Total number of index nodes:", bulk_index_stats["index_nodes"])
    print("Number of levels in B+ tree:", bulk_index_stats["levels"])
    print("Root node keys:", bulk_index_stats["root_keys"])
    print("")
    if boolean:
        print("Search Operation Statistics (Iterative B+ Tree):")
        print("Number of index nodes accessed:", iterative_search_stats["index_nodes_accessed"])
        print("Number of data blocks accessed:", iterative_search_stats["data_blocks_accessed"])
        print("Average FG_PCT_home of returned records:", iterative_search_stats["average_fg_pct_home"])
        print("B+ tree search running time (seconds):", iterative_search_stats["bptree_search_time"])
        print("")
    print("Search Operation Statistics (Bulk Loading B+ Tree):")
    print("Number of index nodes accessed:", bulk_search_stats["index_nodes_accessed"])
    print("Number of data blocks accessed:", bulk_search_stats["data_blocks_accessed"])
    print("Average FG_PCT_home of returned records:", bulk_search_stats["average_fg_pct_home"])
    print("B+ tree search running time (seconds):", bulk_search_stats["bptree_search_time"])
    print("")
    print("Search Operation Statistics (Linear Scan):")
    print("Number of data blocks accessed:", linear_search_stats["data_blocks_accessed"])
    print("Linear scan running time (seconds):", linear_search_stats["linear_scan_time"])

def main(bool):
    """Main function to run storage and indexing operations and print report statistics."""
    records = load_records("data/games.txt")
    block_size = 4096
    db = build_storage(records, block_size)
    record_size = records[0].size() if records else 0
    total_records = len(records)
    records_per_block = len(db.blocks[0].records) if db.blocks else 0
    total_blocks = len(db.blocks)
    storage_stats = {
        "record_size": record_size,
        "total_records": total_records,
        "records_per_block": records_per_block,
        "total_blocks": total_blocks
    }
    order = 4
    tree_iterative = build_index_iterative(db, order)
    iterative_index_nodes = tree_iterative.count_index_nodes()
    iterative_levels = tree_iterative.tree_levels()
    iterative_root_keys = tree_iterative.get_root_keys()
    iterative_index_stats = {
        "order": order,
        "index_nodes": iterative_index_nodes,
        "levels": iterative_levels,
        "root_keys": iterative_root_keys
    }
    tree_bulk = BPTree(order)
    tree_bulk.bulk_load(db.get_all_records())
    tree_bulk.fix_leaf_links()
    bulk_index_nodes = tree_bulk.count_index_nodes()
    bulk_levels = tree_bulk.tree_levels()
    bulk_root_keys = tree_bulk.get_root_keys()
    bulk_index_stats = {
        "order": order,
        "index_nodes": bulk_index_nodes,
        "levels": bulk_levels,
        "root_keys": bulk_root_keys
    }
    key_min = 0.6
    key_max = 0.9
    start_iterative = time.time()
    iterative_records, iterative_index_nodes_accessed = tree_iterative.search_range(key_min, key_max)
    end_iterative = time.time()
    iterative_search_time = end_iterative - start_iterative
    iterative_data_blocks_accessed = get_data_block_accesses(db, iterative_records)
    iterative_avg_fg_pct_home = sum(r.FG_PCT_home for r in iterative_records) / len(iterative_records) if iterative_records else 0
    iterative_search_stats = {
        "index_nodes_accessed": iterative_index_nodes_accessed,
        "data_blocks_accessed": iterative_data_blocks_accessed,
        "average_fg_pct_home": iterative_avg_fg_pct_home,
        "bptree_search_time": iterative_search_time
    }
    start_bulk = time.time()
    bulk_records, bulk_index_nodes_accessed = tree_bulk.search_range(key_min, key_max)
    end_bulk = time.time()
    bulk_search_time = end_bulk - start_bulk
    bulk_data_blocks_accessed = get_data_block_accesses(db, bulk_records)
    bulk_avg_fg_pct_home = sum(r.FG_PCT_home for r in bulk_records) / len(bulk_records) if bulk_records else 0
    bulk_search_stats = {
        "index_nodes_accessed": bulk_index_nodes_accessed,
        "data_blocks_accessed": bulk_data_blocks_accessed,
        "average_fg_pct_home": bulk_avg_fg_pct_home,
        "bptree_search_time": bulk_search_time
    }
    linear_records, linear_data_blocks_accessed, linear_scan_time = linear_scan(db, key_min, key_max)
    linear_search_stats = {
        "data_blocks_accessed": linear_data_blocks_accessed,
        "linear_scan_time": linear_scan_time
    }
    print_report(storage_stats, iterative_index_stats, bulk_index_stats, iterative_search_stats, bulk_search_stats, linear_search_stats,bool)
    df = pd.read_csv("data/games.txt", sep="\t", header=0)
    flt = df[(df["FG_PCT_home"]>=0.6) & (df["FG_PCT_home"]<=0.9)]["FG_PCT_home"]
    print(f"The real average is: {sum(flt)/flt.count()}")

if __name__ == "__main__":
    main(False)
