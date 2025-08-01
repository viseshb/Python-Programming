class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class Queue:
    def __init__(self, value):
        new_node = Node(value)
        self.first = new_node
        self.last = new_node
        self.length = 1

    def print_Queue(self):
        temp = self.first
        while temp:
            print(temp.value)
            temp = temp.next

    def Enqueue(self, value):
        new_node = Node(value)
        if not self.first:
            self.first = new_node
            self.last = new_node
        else:
            self.last.next = new_node
            self.last = new_node   
        self.length +=1
        return True    

    def dequeue(self):
        if not self.first:
            return None
        temp = self.first
        self.first = self.first.next
        temp.next = None
        self.length -=1     
        if not self.first:
            self.last = None   
        return temp.value     


my_queue = Queue(5)
my_queue.Enqueue(6)
my_queue.Enqueue(7)
my_queue.Enqueue(8)
print("Queue before dequeue:")
my_queue.print_Queue()
print("dequeued element:")
print(my_queue.dequeue())
print("Queue After dequeue:")
my_queue.print_Queue()



