
# Simple node object for a doubly linked list
# Each node keeps track of a key/value and pointers to the next and prev nodes
class Node:
    def __init__(self, k, v):
        self.key = k
        self.val = v
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.dic = dict()
        # a neat trick where the cache object itself keeps track of the
        # head and tail directly (acting like a sentinel node)
        # self.prev refers to the front of the LL (most recently added)
        # and self.next refers to the end (next in line for deletion)
        self.prev = self.next = self

    # when you add a new node, put it in the front of the LL
    def _add(self, node):
        # self.prev refers to the old front of the LL
        p = self.prev
        # now that node points to our new node
        p.next = node

        # the cache object must update its pointer so the front points to our new node
        self.prev = node

        # and our new node's prev to the old front of the LL
        node.prev = p
        # and the next points to the cache object (like a sentinel)
        node.next = self

    # when removing a node, you just bypass the pointers to it
    # and let the garbage collector handle the rest
    def _remove(self, node):
        p = node.prev
        n = node.next
        p.next = n
        n.prev = p

    # when you access a key, you need to move that node to the front
    # so it will not be deleted soon
    def get(self, key):
        # first check if the key even exists!
        if key in self.dic:
            # if it was found, get a pointer to the correct node from the dict
            n = self.dic[key]
            # then remove all links to that node
            self._remove(n)
            # and add it to the front of the LL
            self._add(n)
            # finally, return the value that was asked for
            return n.val

        # if the key was not found return -1
        return -1

    # When you put a new value in, you also move it to the front of the list
    def put(self, key, value):
        # if the value was already found
        if key in self.dic:
            # we want to remove links to the node that currenly holds its value
            # so that we can just recreate it at the front of the LL
            self._remove(self.dic[key])
        # make a new node to store the key/value pair
        n = Node(key, value)

        # add that node to the LL (inserting it to the front)
        self._add(n)
        # point the dictionary to that new node
        # note that if the key already existed, we are just reassigning its value
        self.dic[key] = n

        # If we added a new entry to our dictionary, we may be over capacity now
        if len(self.dic) > self.capacity:
            # in that case, we want to remove the last node added
            # which will be referenced by self.next (the tail of the LL)
            n = self.next
            # then we remove the pointers to that node
            self._remove(n)
            # and remove it from the dictionary
            # at this point, there will really be no more pointers to that node
            # and the garbage collector will get rid of it.
            del self.dic[n.key]
