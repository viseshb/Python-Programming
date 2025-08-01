class MaxHeap:
    def __init__(self):
        self.heap = []

    def parent(self, index):
        return (index - 1) // 2

    def left_child(self, index):
        return 2 * index + 1

    def right_child(self, index):
        return 2 * index + 2

    def swap_index(self, index1, index2):
        self.heap[index1], self.heap[index2] = self.heap[index2], self.heap[index1]

    def insert(self, value):
        self.heap.append(value)
        current = len(self.heap) - 1
        while current > 0 and self.heap[current] > self.heap[self.parent(current)]:
            self.swap_index(current, self.parent(current))
            current = self.parent(current)

    def heapify_down(self, index):
        max_index = index
        while True:
            left_idx = self.left_child(index)
            right_idx = self.right_child(index)

            if left_idx < len(self.heap) and self.heap[left_idx] > self.heap[max_index]:
                max_index = left_idx
            if right_idx < len(self.heap) and self.heap[right_idx] > self.heap[max_index]:
                max_index = right_idx

            if max_index != index:
                self.swap_index(index, max_index)
                index = max_index
            else:
                break

    def remove(self):
        if len(self.heap) == 0:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()

        max_val = self.heap[0]
        self.heap[0] = self.heap.pop()
        self.heapify_down(0)
        return max_val



def heap_sort(arr, ascending=True):
    heap = MaxHeap()
    for val in arr:
        heap.insert(val)

    sorted_arr = []
    while heap.heap:
        sorted_arr.append(heap.remove())

    if ascending:
        return sorted_arr[::-1]  # ascending → reverse max-first order
    else:
        return sorted_arr        # descending → natural max-first order



maxHeap = MaxHeap()
maxHeap.insert(99)
maxHeap.insert(72)
maxHeap.insert(61)
maxHeap.insert(58)
print("MaxHeap after inserts:", maxHeap.heap)

maxHeap.insert(100)
print("After inserting 100:", maxHeap.heap)

maxHeap.insert(90)
print("After inserting 90:", maxHeap.heap)

print("Removed element:", maxHeap.remove())
print("Heap after removal:", maxHeap.heap)



print("\nOriginal array:", maxHeap.heap)

asc_sorted = heap_sort(maxHeap.heap, ascending=True)
print("Ascending sort:", asc_sorted)

desc_sorted = heap_sort(maxHeap.heap, ascending=False)
print("Descending sort:", desc_sorted)
