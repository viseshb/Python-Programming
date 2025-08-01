class Node: 
    def __init__(self,value):
        self.value = value
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self, value):
        new_node = Node(value)
        self.head = new_node
        self.tail = new_node
        self.length = 1

    def printList(self):
        temp = self.head
        while temp:
            print(temp.value)
            temp = temp.next

    def append(self,value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.length+=1
        return True  

    def pop(self):
        if self.length == 0:
            return None
        temp = self.tail
        if self.length == 1:
            self.head = None
            self.tail = None
        else:            
            self.tail = self.tail.prev
            self.tail.next = None
            temp.prev = None
        self.length-=1
        return temp.value   

    def prepend(self,value):
        new_node = Node(value)
        if self.length == 0:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node        
            self.head = new_node      
        self.length +=1
        return True

    def popFirst(self):
        if self.length == 0:
            return None
        temp = self.head
        if self.length == 1:
            self.head = None
            self.tail = None
        else:            
            self.head = temp.next
            self.head.prev = None
            temp.next = None
        self.length-=1
        return temp.value       
    
    def get (self,index):
        if index < 0 or index >= self.length:
            return None
        temp = self.head
        if index < self.length/2:
            for _ in range(index):
                temp = temp.next    
        else:
            temp = self.tail    
            for _ in range(self.length-1, index, -1):
                temp = temp.prev  
        return temp.value      
    
    def set_value(self, index, value):
        temp = self.head
        for _ in range(index):
            if not temp:
                return False
            temp = temp.next
        if temp:
            temp.value = value
            return True
        return False    
    
    def insert_value(self, index, value):
        new_node = Node(value)    
    
        if index < 0 or index > self.length:
            return False    
    
        if index == 0:
       
            if self.head is None:
               self.head = new_node
               self.tail = new_node
            else:
               new_node.next = self.head
               self.head.prev = new_node
               self.head = new_node
            self.length += 1
            return True    
    
        if index == self.length:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
            self.length += 1
            return True
    
    
        before = self.head
        for _ in range(index - 1):
            before = before.next
        after = before.next

        new_node.next = after
        new_node.prev = before
        before.next = new_node
        after.prev = new_node

        self.length += 1
        return True
    

    def remove(self,index):
        
    # Validate the index
        if index < 0 or index >= self.length:
            return None

    # If there's only one node, remove it and return it
        if self.length == 1:
            temp = self.head
            self.head = None
            self.tail = None
            self.length -= 1
            return temp

    # Remove from the beginning (head)
        if index == 0:
            temp = self.head
            self.head = self.head.next
            self.head.prev = None
            temp.next = None  # Clear the pointer of removed node
            self.length -= 1
            return temp

    # Remove from the end (tail)
        if index == self.length - 1:
            temp = self.tail
            self.tail = self.tail.prev
            self.tail.next = None
            temp.prev = None  # Clear the pointer of removed node
            self.length -= 1
            return temp

    # Remove from the middle
        temp = self.head
        for _ in range(index):
            temp = temp.next

    # Bypass the node to be removed
        temp.prev.next = temp.next
        temp.next.prev = temp.prev
    # Clean up the removed node's pointers
        temp.next = None
        temp.prev = None

        self.length -= 1
        return temp 
    
    def swap_first_last(self):
        if not self.head or not self.head.next:
            return None
        
        first = self.head
        temp = self.head

        while temp.next:
            temp = temp.next

        first.value, temp.value = temp.value, first.value



      

my_doubly_LL = DoublyLinkedList(7)
# my_doubly_LL.prepend(8)
my_doubly_LL.append(6)
my_doubly_LL.append(5)
my_doubly_LL.printList()
print("The value of the Node at index is:", my_doubly_LL.get(3))
my_doubly_LL.set_value(2, 100)
my_doubly_LL.printList()
print("--------------------")
my_doubly_LL.swap_first_last()
my_doubly_LL.printList()


# my_doubly_LL.printList()
# print(my_doubly_LL.popFirst())
# print(my_doubly_LL.popFirst())
# print(my_doubly_LL.popFirst())

# print(my_doubly_LL.popFirst())





# print(my_doubly_LL.pop())
# print(my_doubly_LL.pop())

# print(my_doubly_LL.pop())

         
