class State:
    def __init__(self, assignment):
        self.assignment = assignment

    def is_complete(self):
        for i in range(self.assignment.__len__()):
            if self.assignment[i] < 0:
                return False
        return True


