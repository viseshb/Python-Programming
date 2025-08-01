class HashTable:
    def __init__(self, size = 7):
        self.data_map = [None] * size

    def hash(self, key):
        my_hash = 0
        for letter in key:
            my_hash = (my_hash + ord(letter)*23) % len(self.data_map)
        return my_hash

    def print_HT(self):
        for i, value in enumerate(self.data_map):
            print(i, ":" , value)

    def set(self, key ,value):
        index = self.hash(key)
        if self.data_map[index] == None:
            self.data_map[index] = []
        self.data_map[index].append([key, value])

    def get(self, key):
        index = self.hash(key)
        if self.data_map[index] is not None:
            for pair in self.data_map[index]:
                if pair[0] == key:
                    return pair[1]
        return None   
    
    # def get(self, key):                                      #We can either us this also for get function!!
    #     index = self.hash(key)
    #     if self.data_map[index] is not None:
    #         for i in range(len(self.data_map[index])):
    #             if self.data_map[index][i][0] == key:
    #                 return self.data_map[index][i]
    #     return None   

    def keys(self):
        all_keys =[]
        for i in range(len(self.data_map)):
            if self.data_map[i] is not None:
                for j in range(len(self.data_map[i])):
                    all_keys.append(self.data_map[i][j][0])       
        return all_keys       

    def values(self):
        all_values = []
        for i in range(len(self.data_map)):
            if self.data_map[i] is not None:
                for j in range(len(self.data_map[i])):
                    all_values.append(self.data_map[i][j][1])
        return all_values                 



my_HT = HashTable()

my_HT.set('Hello', 1000)
my_HT.set('Welcome', 2000)
my_HT.set('Bye',31000)
my_HT.set('Wsup', 1000)




my_HT.print_HT()
print(my_HT.keys())
print(my_HT.values())

print("Value of Wsup",my_HT.get('Wsup'))

          