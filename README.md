# BPlusTree
## Implementation and Experiments

### Task 1: Storage Component  
Design and implement the storage component based on the settings described in Part 1 and store the data (which is about NBA games and will be described in Part 4).  

#### Requirements:
- Describe the content of a record, a block, and a database file.
- Report the following statistics:
  - The size of a record.
  - The number of records.
  - The number of records stored in a block.
  - The number of blocks for storing the data.

---

### Task 2: Indexing Component  
Design and implement the indexing component based on the settings described in Part 1 and build a B+ tree on the data described in Task 1 with the attribute `"FG_PCT_home"` as the key.

#### Requirements:
- Report the following statistics:
  - The parameter **n** of the B+ tree.
  - The number of nodes of the B+ tree.
  - The number of levels of the B+ tree.
  - The content of the root node (only the keys).

---

### Task 3: Search Operation  
Search for records with the attribute `"FG_PCT_home"` in the range **0.6 to 0.9** (both inclusively) using the B+ tree.

#### Requirements:
- Report the following statistics:
  - The number of index nodes accessed.
  - The number of data blocks accessed.
  - The average of `"FG_PCT_home"` for the records returned.
  - The running time of the retrieval process.
  - The number of data blocks accessed by a brute-force linear scan method (i.e., scanning the data blocks one by one) and its running time (for comparison).
