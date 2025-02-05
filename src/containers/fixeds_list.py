class FixedSizeList:
    def __init__(self, max_size):
        self.max_size = max_size
        self.container = []

    def add(self, item):
        if len(self.container) >= self.max_size:
            self.container.pop(0)
        self.container.append(item)

    def __getitem__(self, index):
        return self.container[index]

    def __len__(self):
        return len(self.container)

    def __repr__(self):
        return repr(self.container)