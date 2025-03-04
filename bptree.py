class LeafNode:
    """Leaf node of a B+ tree storing keys and associated records."""
    def __init__(self, order):
        self.order = order
        self.keys = []
        self.values = []
        self.next = None
    def insert(self, key, value):
        idx = 0
        while idx < len(self.keys) and self.keys[idx] < key:
            idx += 1
        self.keys.insert(idx, key)
        self.values.insert(idx, value)
    def split(self):
        mid = len(self.keys) // 2
        new_leaf = LeafNode(self.order)
        new_leaf.keys = self.keys[mid:]
        new_leaf.values = self.values[mid:]
        self.keys = self.keys[:mid]
        self.values = self.values[:mid]
        new_leaf.next = self.next
        self.next = new_leaf
        return new_leaf, new_leaf.keys[0]

class InternalNode:
    """Internal node of a B+ tree storing keys and child pointers."""
    def __init__(self, order):
        self.order = order
        self.keys = []
        self.children = []
    def insert_child(self, key, child):
        idx = 0
        while idx < len(self.keys) and self.keys[idx] < key:
            idx += 1
        self.keys.insert(idx, key)
        self.children.insert(idx + 1, child)
    def split(self):
        mid = len(self.keys) // 2
        new_internal = InternalNode(self.order)
        new_internal.keys = self.keys[mid+1:]
        new_internal.children = self.children[mid+1:]
        up_key = self.keys[mid]
        self.keys = self.keys[:mid]
        self.children = self.children[:mid+1]
        return new_internal, up_key

class BPTree:
    """B+ tree implementation for indexing records based on FG_PCT_home."""
    def __init__(self, order):
        self.order = order
        self.root = LeafNode(order)
        self.index_access_count = 0
    def insert(self, key, value):
        root = self.root
        if isinstance(root, LeafNode):
            root.insert(key, value)
            if len(root.keys) == self.order:
                new_leaf, new_key = root.split()
                new_root = InternalNode(self.order)
                new_root.keys = [new_key]
                new_root.children = [root, new_leaf]
                self.root = new_root
        else:
            self._insert_internal(root, key, value)
    def _insert_internal(self, node, key, value):
        if isinstance(node, LeafNode):
            node.insert(key, value)
            if len(node.keys) == self.order:
                new_leaf, new_key = node.split()
                return new_key, new_leaf
            return None
        else:
            self.index_access_count += 1
            idx = 0
            while idx < len(node.keys) and key >= node.keys[idx]:
                idx += 1
            result = self._insert_internal(node.children[idx], key, value)
            if result is not None:
                new_key, new_child = result
                node.insert_child(new_key, new_child)
                if len(node.keys) == self.order:
                    new_internal, up_key = node.split()
                    return up_key, new_internal
            return None
    def bulk_load(self, records):
        """Bulk load the B+ tree from a sorted list of records using FG_PCT_home as key."""
        sorted_records = sorted(records, key=lambda r: r.FG_PCT_home)
        leaf_capacity = self.order - 1
        leaves = []
        current_leaf = LeafNode(self.order)
        for record in sorted_records:
            key = record.FG_PCT_home
            if len(current_leaf.keys) < leaf_capacity:
                current_leaf.keys.append(key)
                current_leaf.values.append(record)
            else:
                leaves.append(current_leaf)
                current_leaf = LeafNode(self.order)
                current_leaf.keys.append(key)
                current_leaf.values.append(record)
        leaves.append(current_leaf)
        for i in range(len(leaves) - 1):
            leaves[i].next = leaves[i + 1]
        level_nodes = leaves
        while len(level_nodes) > 1:
            new_level = []
            internal_capacity = self.order
            i = 0
            while i < len(level_nodes):
                group = level_nodes[i:i + internal_capacity]
                if len(group) == 1:
                    new_level.append(group[0])
                else:
                    new_node = InternalNode(self.order)
                    new_node.children = group
                    new_node.keys = [child.keys[0] for child in group[1:]]
                    new_level.append(new_node)
                i += internal_capacity
            level_nodes = new_level
        self.root = level_nodes[0]
    def search_range(self, key_min, key_max):
        """Search the B+ tree for records with keys in the given range. Returns a tuple (records, index_nodes_accessed)."""
        records = []
        self.index_access_count = 0
        node = self.root
        while not isinstance(node, LeafNode):
            self.index_access_count += 1
            idx = 0
            while idx < len(node.keys) and key_min >= node.keys[idx]:
                idx += 1
            node = node.children[idx]
        while node is not None:
            self.index_access_count += 1
            for k, v in zip(node.keys, node.values):
                if k > key_max:
                    return records, self.index_access_count
                if k >= key_min:
                    records.append(v)
            node = node.next
        return records, self.index_access_count
    def count_nodes(self):
        """Return the total number of nodes in the B+ tree."""
        nodes = []
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            nodes.append(node)
            if not isinstance(node, LeafNode):
                for child in node.children:
                    queue.append(child)
        return len(nodes)
    def tree_levels(self):
        """Return the number of levels in the B+ tree."""
        levels = 0
        node = self.root
        while not isinstance(node, LeafNode):
            levels += 1
            node = node.children[0]
        return levels + 1
    def get_root_keys(self):
        """Return the keys contained in the root node."""
        return self.root.keys
    def save_tree(self, filename):
        """Save the B+ tree to disk using pickle."""
        import pickle
        with open(filename, 'wb') as f:
            pickle.dump(self.root, f)
