class MyCollections:
    def __init__(self):
        self.list = []

    def add_item(self, item):
        self.list.append(item)

    def add_items(self, items):
        self.list.extend(items)

    def print_items(self):
        for item in self.list:
            print(item)
