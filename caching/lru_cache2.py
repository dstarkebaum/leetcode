
# Simple node object for a doubly linked list
# Each node keeps track of a key/value and pointers to the next and prev nodes
class Node(object):
    # I am not sure exactly why this implementation was used,
    # but basically the constructor starts by creating an empty node
    # which does not have a link to any next or prev node
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.next = None
        self.prev = None

    # generally you are meant to use the create method to make a new node
    # so that it can point to itself (common pattern in circularly linked list)
    @staticmethod
    def create(key, val):
        node = Node(key, val)
        node.next = node
        node.prev = node

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
        # what is this for?
        self.key_node_map = dict()

    # moves a given node to the front (head) of the linked list
    def move_to_head(self, node):

        # if it is already there, there is nothing to do!
        if self.head == node:
            return

        # temporarily store a pointer to the old head of the LL
        old_head = self.head

        # if there is only one item, its next and previous points to itself
        # otherwise...
        if node.next != node:

            # connect the current node's next node to the current node's prev
            # so that we can remove the current node from its current position
            node.next.prev = node.prev

        # same as before:
        # if there is only one item, its next and previous points to itself
        if node.prev != node:

            # connect the current node's prev node to the current node's next
            # so that we can remove the current node from its current position
            node.prev.next = node.next


        # keep track of the prev node from the head
        old_head_prev = old_head.prev

        # now point the current head node to our node
        old_head.prev = node

        # and make sure our node points to whatever used to be prev the head
        # I think this should be null though, right?
        node.prev = old_head_prev

        # Assuming there was acctually something prev the head,
        # now it points downward to our new head node
        node.prev.next = node

        # and our new head points down to the nextious head
        node.next = old_head

        # if the current node was the only node in the list,
        # it will be both the head and the tail of the LL
        if self.tail == node:

            # move the tail pointer up one? So now it points to null??
            self.tail = old_head_prev

        # The head pointer now should point to our new head node
        self.head = node


    def get(self, key):
        """
        :type key: int
        :rtype: int
        """

        node = self.key_node_map.get(key)
        if node is not None:
            # When a node is accessed, move it to the head
            self.move_to_head(node)
            return node.val
        else:
            return -1


    def put(self, key, value):
        """
        :type key: int
        :type value: int
        :rtype: None
        """
        # look in the dictionary to see if the new key is already present
        # if it is not there, dict.get() returns None (not OutOfBoundsException!)
        node = self.key_node_map.get(key)

        # if the key was already entered before
        # there exists a node in the linked list that stores the value
        if node is not None:
            # In this case, we overwrite the current value
            node.val = value

        # in this case, the key is not found, and our cache still has more room
        elif self.size < self.capacity:
            # so we createa a new node to store the value
            node = Node.create(key, value)
            # and point our dictionary to that node.
            self.key_node_map[key] = node
            # our LRU cache has grown, so prev time it may be full
            self.size += 1
        # in this case, we have a new key, and our cache is already full
        else:
            # evict
            # get the node from the tail of the LL
            curr_tail = self.tail
            # the node stores they key
            old_key = curr_tail.key
            # we can remove this key from our dict, since it no longer
            # points to anything useful
            del self.key_node_map[old_key]


            curr_tail.key = key
            curr_tail.val = value
            self.key_node_map[key] = curr_tail
            node = curr_tail

        if self.size == 1:
            self.head = node
            self.tail = node

        self.move_to_head(node)
