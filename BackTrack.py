import sys

from State import State
from copy import deepcopy


class BackTtrack:
    def __init__(self, cage_number, animal_number, adjacent_number, cages_size_list, cage_adjacent_matrix,
                 animals_size_list, animal_matrix):
        self.cage_number = cage_number
        self.animal_number = animal_number
        self.adjacent_number = adjacent_number
        self.cages_size_list = cages_size_list
        self.cage_adjacent_matrix = cage_adjacent_matrix
        self.animals_size_list = animals_size_list
        self.animal_matrix = animal_matrix

        self.animal_cages = []
        self.assignment = None
        self.root = State(assignment=[-1 for _ in range(cage_number)])
        self.cage_neighbours = []
        # self.animal_degree = self.set_animal_degree()  # تعداد محدودیت های حیوان های انتخاب نشده
        self.set_animal_cage()
        self.find_cage_neighbour()

    def solve_backtrack(self):
        self.set_animal_cage()
        self.find_cage_neighbour()
        return self.recursive_backtrack(state=self.root, animal_id=0, animal_cage=deepcopy(self.animal_cages))

    def solve_forward_checking(self):
        self.set_animal_cage()
        self.find_cage_neighbour()
        return self.recursive_forward_checking(state=self.root, animal_id=0, animal_cage=deepcopy(self.animal_cages))

    def solve_mrv(self):
        self.set_animal_cage()
        self.find_cage_neighbour()
        return self.recursive_mrv(state=self.root, animal_cage=deepcopy(self.animal_cages))

    def solve_lcv(self):
        self.set_animal_cage()
        self.find_cage_neighbour()
        return self.recursive_lcv(state=self.root, animal_id=0, animal_cage=deepcopy(self.animal_cages))

    def solve_mrv_lcv(self):
        self.set_animal_cage()
        self.find_cage_neighbour()
        return self.recursive_mrv_lcv(state=self.root, animal_cage=deepcopy(self.animal_cages))

    def recursive_backtrack(self, state, animal_id, animal_cage):
        if animal_id >= self.animal_number:
            if state.is_complete():
                # if self.is_consistent(cage_neighbours=self.cage_neighbours, assignment=state.assignment):
                self.assignment = state.assignment
            return
        for cage_id in animal_cage[animal_id]:
            new_state = State(assignment=deepcopy(state.assignment))
            new_state.assignment[cage_id] = animal_id
            new_animal_cage = deepcopy(animal_cage)
            update_domain(new_animal_cage, cage_id)
            self.recursive_backtrack(state=new_state, animal_id=animal_id + 1, animal_cage=new_animal_cage)

    def recursive_forward_checking(self, state, animal_id, animal_cage):
        if animal_id >= self.animal_number:
            # if self.is_consistent(self.cage_neighbours, state.assignment):
            self.assignment = state.assignment
            return
        for cage_id in animal_cage[animal_id]:
            new_state = State(assignment=deepcopy(state.assignment))
            new_state.assignment[cage_id] = animal_id
            new_animal_cage = deepcopy(animal_cage)
            update_domain(new_animal_cage, cage_id)
            self.recursive_forward_checking(state=new_state, animal_id=animal_id + 1, animal_cage=new_animal_cage)
            if self.assignment:
                return

    def recursive_lcv(self, state, animal_id, animal_cage):
        if animal_id >= self.animal_number:
            # if self.is_consistent(self.cage_neighbours, state.assignment):
            self.assignment = state.assignment
            return
        self.lcv(animal_id)
        for cage_id in animal_cage[animal_id]:
            new_state = State(assignment=deepcopy(state.assignment))
            new_state.assignment[cage_id] = animal_id
            new_animal_cage = deepcopy(animal_cage)
            update_domain(new_animal_cage, cage_id)
            self.recursive_lcv(state=new_state, animal_id=animal_id + 1, animal_cage=new_animal_cage)
            if self.assignment:
                return

    def recursive_mrv(self, state, animal_cage):
        if state.is_complete():
            if self.is_consistent(self.cage_neighbours, state.assignment):
                self.assignment = state.assignment
            return
        animal_id = self.mrv(state.assignment)
        if len(animal_cage[animal_id]) == 0:
            return
        for cage_id in animal_cage[animal_id]:
            new_state = State(deepcopy(state.assignment))
            new_state.assignment[cage_id] = animal_id
            new_animal_cage = deepcopy(animal_cage)
            update_domain(new_animal_cage, cage_id)
            self.recursive_mrv(state=new_state, animal_cage=new_animal_cage)
            if self.assignment:
                return

    def recursive_mrv_lcv(self, state, animal_cage):
        if state.is_complete():
            # if self.is_consistent(self.cage_neighbours, state.assignment):
            self.assignment = state.assignment
            return
        animal_id = self.mrv(state.assignment)
        if len(animal_cage[animal_id]) == 0:
            return
        self.lcv(animal_id)
        for cage_id in animal_cage[animal_id]:
            new_state = State(deepcopy(state.assignment))
            new_state.assignment[cage_id] = animal_id
            new_animal_cage = deepcopy(animal_cage)
            update_domain(new_animal_cage, cage_id)
            self.recursive_mrv_lcv(state=new_state, animal_cage=new_animal_cage)
            if self.assignment:
                return

    def set_animal_cage(self):  # domain (cage) ha ro baraye variable (animal) ha moshakhas mikonad
        for i in range(self.animal_number):
            x = []
            for j in range(self.cage_number):
                if self.cages_size_list[j] >= self.animals_size_list[i]:
                    x.append(j)
            self.animal_cages.append(x)

    def find_cage_neighbour(self):
        for lst in self.cage_adjacent_matrix:
            x = []
            for i in range(lst.__len__()):
                if lst[i] > 0:
                    x.append(i)
            self.cage_neighbours.append(x)

    def has_problem(self, animal_id, animal_id_2):
        if animal_id_2 >= 0:
            if self.animal_matrix[animal_id][animal_id_2] == 1:
                return True
        return False

    def check_neighbours(self, cage_neighbours, cage_id, animal_id, assignment):
        for neighbour in cage_neighbours[cage_id]:
            if self.has_problem(animal_id, assignment[neighbour]):
                return False
        return True

    def is_consistent(self, cage_neighbours, assignment):
        for cage in assignment:
            if not self.check_neighbours(cage_neighbours, cage, assignment[cage], assignment):
                return False
        return True

    def lcv(self, animal_id):
        temp = [0 for _ in range(len(self.animal_cages[animal_id]))]
        new_list = []
        for i in range(len(self.animal_cages[animal_id])):
            temp[i] = self.check_domain(self.animal_cages[animal_id][i]) - 1
        for i in range(len(self.animal_cages[animal_id])):
            new_list.append(self.animal_cages[animal_id][temp.index(min(temp))])
            temp.pop(temp.index(min(temp)))
        self.animal_cages[animal_id] = new_list

    def mrv(self, assignment):
        minimum = sys.maxsize
        index = -1
        for i in range(len(self.animal_cages)):
            if assignment.count(i) < 1:
                if len(self.animal_cages[i]) < minimum:
                    minimum = len(self.animal_cages[i])
                    index = i
        return index

    def check_domain(self, cage_id):
        count = 0
        for lst in self.animal_cages:
            count += lst.count(cage_id)
        return count


def update_domain(animal_cage, cage_id):
    for item in animal_cage:
        if item.count(cage_id) > 0:
            item.remove(cage_id)

    # def set_animal_degree(self):
    #     temp = []
    #     for animal in self.animal_matrix:
    #         s = 0
    #         for item in animal:
    #             s += item
    #         temp.append(s)
    #     return temp
    #
    # def update_animal_degree(self, animal_id):
    #     for i in range(len(self.animal_cages)):
    #         if self.animal_cages[i][animal_id] == 1:
    #             self.animal_degree[i] = self.animal_degree[i] - 1
    #
    # def degree(self, assignment):  # maximum remaining value
    #     maximum = -10
    #     temp = list(self.animal_degree)
    #     for i in range(len(self.animal_degree)):
    #         if assignment.count(i) == 0:
    #             if self.animal_degree[i] > maximum:
    #                 maximum = self.animal_degree[i]
    #         else:
    #             temp[i] = -1
    #     if maximum > -10:
    #         return temp.index(maximum)
    #     else:
    #         return -1
