class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, value):
        new_node = Node(value)
        if self.root is None:
            self.root=  new_node
            return True
        temp =self.root
        while True:
            if new_node.value == temp.value:
                return False
            if new_node.value < temp.value:
                if temp.left is None:
                    temp.left = new_node
                    return True
                temp = temp.left
            if new_node.value > temp.value:
                if temp.right is None:
                    temp.right = new_node
                    return True
                temp = temp.right

    def DFS_PreOrder(self):
        results = []
        def traverse(current_node):
            results.append(current_node.value)
            if current_node.left is not None:
                traverse(current_node.left)
            if current_node.right is not None:
                traverse(current_node.right)                
        traverse(self.root)
        return results
    


myTree = BST()
myTree.insert(47)    
myTree.insert(21)    
myTree.insert(76)    
myTree.insert(18)    
myTree.insert(27)    
myTree.insert(52)    
myTree.insert(82)
print(myTree.DFS_PreOrder())


