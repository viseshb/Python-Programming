class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, value):
        node =Node(value)
        if self.root is None:
            self.root = node
            return True
        temp = self.root
        while True:
            if node.value == temp.value:
                return False
            if node.value > temp.value:
                if temp.right is None:
                    temp.right = node
                    return True
                temp = temp.right
            if node.value < temp.value:
                if temp.left is None:
                    temp.left = node
                    return True
                temp = temp.left



    def DFS_In_Order(self):
        results = []
        def traverse(node):
            if node.left is not None:
                traverse(node.left)
            results.append(node.value)
            if node.right is not None:
                traverse(node.right)                                    
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
print(myTree.DFS_In_Order())      