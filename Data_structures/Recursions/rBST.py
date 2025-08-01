class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None  

class BST:
    def __init__(self):
        self.root = None

    def __r_insert(self, node, value):
        if node is None:
            return Node(value)
        if value == node.value:
            return node
        if value > node.value:
            node.right = self.__r_insert(node.right, value)
        else:
            node.left = self.__r_insert(node.left, value)
        return node

    def _r_insert(self, value):
        if self.root == None:
            self.root = Node(value)
        self.root = self.__r_insert(self.root, value)

    def __r_contains(self, node, value):
        if node is None:
            return False
        if value == node.value:
            return True
        if value > node.value:
            return self.__r_contains(node.right, value)
        else:
            return self.__r_contains(node.left, value)

    def _r_contains(self, value):
        return self.__r_contains(self.root, value)   

    def min_val(self, node):
        while node.left is not None:
            node = node.left
        return node.value
    
    def max_val(self, node):
        while node.right is not None:
            node = node.right
        return node.value    

    def __r_delete_node(self, node, value):
        if node is None:
            return None
        if value < node.value:
            node.left = self.__r_delete_node(node.left, value)
        elif value > node.value:
            node.right = self.__r_delete_node(node.right, value)
        else:
            if node.left == None and node.right == None:
                return None
            elif node.left == None:
                node= node.right
            elif node.right == None:
                node = node.left
            else:
                sub_tree_min = self.min_val(node.right)
                node.value = sub_tree_min
                node.right = self.__r_delete_node(node.right, sub_tree_min)
        return node        
    
    def _r_delete_node(self, value):
        self.root = self.__r_delete_node(self.root, value)


                     
    def __print_in_order(self, node):
        if node:
           self.__print_in_order(node.left)
           print(node.value, end=" ")
           self.__print_in_order(node.right)

    def print_tree(self):
        if self.root is None:
           print("Tree is empty.")
        else:
           self.__print_in_order(self.root)
           print()

myTree = BST()
myTree._r_insert(47)
myTree._r_insert(21)
myTree._r_insert(76)
myTree._r_insert(18)
myTree._r_insert(27)
myTree._r_insert(52)
myTree._r_insert(82)

print('BST Contains 52:', myTree._r_contains(52))
print('BST Contains: 40:', myTree._r_contains(40))

print("Root:", myTree.root.value)
print("Root ->left:", myTree.root.left.value)
print("Root -> right:", myTree.root.right.value)
myTree.print_tree()
myTree._r_delete_node(21)
myTree.print_tree()
print(myTree.min_val(myTree.root))
print(myTree.min_val(myTree.root.right))
print(myTree.max_val(myTree.root))