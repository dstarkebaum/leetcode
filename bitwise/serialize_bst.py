# https://leetcode.com/problems/serialize-and-deserialize-bst/discuss/93224/Concise-iterative-Python-solution-using-stack-beat-99.

class Codec:


ALPHABET = u"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_.~"
BASE = len(ALPHABET)

def encode(n):
    if n == 0:
        return ALPHABET[0].encode('ascii')
    stack = []

    while n:
        quotient, remainder = divmod(n, BASE)
        stack.append(ALPHABET[remainder])
    return ''.join(stack).encode('ascii')[::-1]


    def serialize(self, root):
        result, stack = [], []
        # not really necessary, but helps with understanding
        # we will keep track of a single node as we traverse the tree
        # and we just start at the root of the tree
        node = root

        # as long as we have nodes left in our stack or tree
        while stack or node:
            # if there are remaining nodes in the (left branch of the) tree
            if node:
                # get the value and store it in the result list
                result.append(node.val)
                # store a reference to the current node in the stack
                stack.append(node)
                # move on to the next node, starting from the left
                # if we reach the end, node.left will be null
                # so we will skip this step in the next round
                node = node.left

            # in this case, we have traversed as far left as possible
            # so we have to start popping nodes off the stack
            # This means we are taking a step back up the tree
            # and going one step down the right branch next
            else:

                # get the last element from the list/stack
                # this is an O(1) operation, since we don't have to shift order
                node = stack.pop()

                # take one step down the right branch
                node = node.right

        # Now the entire tree is stored in a list
        # in order of root -> left -> right
        # so finally, we join the results together
        # with whatever delimiter we want (space in this case)
        # this will implicitly call str(val) on every element in the result
        return ' '.join(result)

    def deserialize(self, data):
        # if there is no data, there is nothing to load!
        if not data:
            return None

        # I guess the BST is supposed to holt integers...
        data = map(int, data.split(' '))

        stack = []

        # the first value goes to the root
        root = node = TreeNode(data[0])

        # now loop through the data after the first entry
        for val in data[1:]:

            # if the value is less than the current node
            # then go left!
            if val < node.val:
                # create a new node do the left
                # and store the value there
                node.left = TreeNode(val)
                # store the current node in the stack
                # so we can come back after we hit the end
                # of the left branch
                stack.append(node)

                # step into the left branch and continue the loop
                node = node.left

            # val is larger than the current node's val
            else:

                # keep popping off nodes from the stack (backing up the tree)
                # as long as the val is bigger than node.val
                # at the end, node should point to the last node
                # with a value smaller than val
                # and it should be removed from the stack
                while stack and stack[-1].val < val:

                    node = stack.pop()
                # now we create a new node to the right (since val > node.val)
                node.right = TreeNode(val)

                # and we step into that node for the next iteration
                node = node.right

        # now the tree is complete, so we return a reference to the root
        return root
