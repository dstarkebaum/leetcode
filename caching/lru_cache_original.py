class Node(object):
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.left = None
        self.right = None

    @staticmethod
    def create(key, val):
        node = Node(key, val)
        node.left = node
        node.right = node

        return node


class LRUCache(object):

    def __init__(self, capacity):
        """
        :type capacity: int
        """
        self.head = None     # most recently used
        self.tail = None     # least recently used
        self.capacity = capacity
        self.size = 0
        self.key_node_map = dict()

    def move_to_top(self, node):
        if self.head == node:
            return
        curr_top = self.head

        if node.left != node:
            node.left.right = node.right
        if node.right != node:
            node.right.left = node.left

        old_curr_top_right = curr_top.right
        curr_top.right = node
        node.right = old_curr_top_right
        node.right.left = node
        node.left = curr_top

        if self.tail == node:
            self.tail = old_curr_top_right

        self.head = node


    def get(self, key):
        """
        :type key: int
        :rtype: int
        """
        node = self.key_node_map.get(key)
        if node is not None:
            self.move_to_top(node)
            return node.val
        else:
            return -1


    def put(self, key, value):
        """
        :type key: int
        :type value: int
        :rtype: None
        """
        node = self.key_node_map.get(key)
        if node is not None:
            node.val = value
        elif self.size < self.capacity:
            node = Node.create(key, value)
            self.key_node_map[key] = node
            self.size += 1
        else:
            # evict
            curr_tail = self.tail
            old_key = curr_tail.key
            del self.key_node_map[old_key]

            curr_tail.key = key
            curr_tail.val = value
            self.key_node_map[key] = curr_tail
            node = curr_tail

        if self.size == 1:
            self.head = node
            self.tail = node

        self.move_to_top(node)
