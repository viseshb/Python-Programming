class Node:
    def __init__(self,value):
        self.value = value
        self.next = None

class LinkedList:
    def __init__(self, value):
        new_node = Node(value)
        self.head = new_node
        self.tail = new_node
        self.length =1 
    
    def printList(self):
        temp = self.head
        while temp is not None:
          print(temp.value)
          temp = temp.next

    def append(self,value):
       new_node = Node(value)
       if self.head is None:
          self.head = new_node
          self.tail = new_node
       else:
          self.tail.next =new_node
          self.tail =new_node
       self.length +=1
       return True      
    
    def pop(self):
        if self.length == 0:
          return None
        temp =self.head
        pre =self.head
        while temp.next is not None:
          pre= temp
          temp = temp.next
        self.tail =pre
        self.tail.next =None
        self.length-=1
        if self.length == 0:
           self.head =None
           self.tail =None
        return temp.value           

    def prepend(self,value):
       new_node = Node(value)
       if self.head == None:
          self.head = new_node
          self.tail = new_node
       else:
          new_node.next = self.head
          self.head =new_node 
       self.length+=1
       return True  
    
    def pop_first(self):
       if self.length == 0:
          return None
       temp = self.head
       self.head = self.head.next
       temp.next = None
       self.length -=1
       if self.length == 0:
          self.tail = None
       return temp.value   
    
    def get(self, index):
       if index < 0 or index > self.length:
          return None
       temp = self.head
       for _ in range(index):
          temp =temp.next
       return temp 
    
    def set_value(self, index, value):
         temp = self.get(index)
         if temp:
           temp.value = value
           return True
         return False


    def insert_value(self, index, value):
         if index < 0 or index > self.length:
            return False
         if index == 0:
            return self.prepend(value)
         if index == self.length:
            return self.append(value)
         new_node = Node(value)
         temp = self.get(index -1 )
         new_node.next = temp.next
         temp.next = new_node
         self.length+=1
         return True
            

    def delete_value(self,index):
       if index < 0 or index >= self.length:
            return False
       if index == 0:
            return self.pop_first()
       if index == self.length-1:
            return self.pop()
       prev = self.get(index -1 )
       temp = prev.next
       prev.next = temp.next
       temp.next = None
       self.length-=1
       return temp
       
    def reverse(self):
        temp = self.head
        self.head = self.tail
        self.tail = temp
        after = temp.next
        before = None
        for _ in range(self.length):
           after = temp.next
           temp.next = before
           before =temp
           temp = after  

    def middleNode(self, head):
      slow = head
      fast = head

      while fast and fast.next:
          slow = slow.next
          fast = fast.next.next
      return slow     


    def deleteMiddle(self, head):
        if head is None or head.next is None:
            return None 
        slow = head
        fast = head
        prev = None

        while fast and fast.next:
            prev = slow
            slow = slow.next
            fast = fast.next.next
        prev.next = slow.next      
        return head     


            
               
           


my_LinkedList = LinkedList(4)
my_LinkedList.append(1)
my_LinkedList.append(2)
my_LinkedList.append(3)
#my_LinkedList.prepend(2)
my_LinkedList.set_value(1,4)
my_LinkedList.insert_value(2,60)


print('Before Head:', my_LinkedList.head.value)
print('Before Tail:', my_LinkedList.tail.value)
print('Before Length:', my_LinkedList.length)

my_LinkedList.printList()
print('Print element at the index 4 is ', my_LinkedList.get(4))
#print('Element Popped first is:', my_LinkedList.pop_first())
my_LinkedList.delete_value(3)
#print('Element Popped', my_LinkedList.pop())

print('After Head:', my_LinkedList.head.value)
print('After Tail:', my_LinkedList.tail.value)
print('After Length:', my_LinkedList.length)
my_LinkedList.reverse()
my_LinkedList.printList()

 


