class LFUCache:
    def __init__(self, capacity: int):
        self.capacity=capacity
        self.lowest_frequency=None
        self.frequency_of_key={}
        self.keys_with_frequency=collections.defaultdict(collections.OrderedDict)

    def get(self, key: int) -> int:
        if key not in self.frequency_of_key:
            return -1
        freq=self.frequency_of_key[key]
        val=self.keys_with_frequency[freq][key]
        del self.keys_with_frequency[freq][key]
        if not self.keys_with_frequency[freq]:
            if freq==self.lowest_frequency:
                self.lowest_frequency+=1
            del self.keys_with_frequency[freq]
        self.frequency_of_key[key]=freq+1
        self.keys_with_frequency[freq+1][key]=val
        return val

    def put(self, key: int, value: int) -> None:
        if self.capacity<=0:
            return
        if key in self.frequency_of_key:
            freq=self.frequency_of_key[key]
            self.keys_with_frequency[freq][key]=value
            self.get(key)
            return
        if self.capacity==len(self.frequency_of_key):
            delkey,delval=self.keys_with_frequency[self.lowest_frequency].popitem(last=False)
            del self.frequency_of_key[delkey]
        self.frequency_of_key[key]=1
        self.keys_with_frequency[1][key]=value
        self.lowest_frequency=1
