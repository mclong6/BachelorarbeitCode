#stack class
#The reason you need to use self. is because Python does not use the @ syntax
# to refer to instance attributes. Python decided to do methods in a way that
#  makes the instance to which the method belongs be passed automatically,
# but not received automatically: the first parameter of methods is the instance
# the method is called on. That makes methods entirely the same as functions,
# and leaves the actual name to use up to you (although self is the convention,
# and people will generally frown at you when you use something else.) self is not
# special to the code, it's just another object.

class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)
