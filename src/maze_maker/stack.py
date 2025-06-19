class Stack:
    def __init__(self):
        self.items = []
        self.visited_cells = []

    def push(self, item):
        self.items.append(item)
        if item not in self.visited_cells:
            self.visited_cells.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Pop from an empty stack")
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("Peek from an empty stack")
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def visited(self, check):
        return check in self.visited_cells