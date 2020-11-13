from BackTrack import BackTtrack


def main():
    cage_number = None  # N
    animal_number = None  # P
    adjacent_number = None  # M
    cages_size_list = []
    cage_adjacent_matrix = None
    animals_size_list = []
    animal_matrix = []
    assignment_list = []

    inp = input().split()
    cage_number = int(inp[0])
    animal_number = int(inp[1])
    adjacent_number = int(inp[2])

    cage_adjacent_matrix = [[0 for i in range(cage_number)] for j in range(cage_number)]

    inp = input().split()
    for i in range(cage_number):
        cages_size_list.append(int(inp[i]))

    inp = input().split()
    for i in range(animal_number):
        animals_size_list.append(int(inp[i]))

    for i in range(adjacent_number):
        inp = input().split()
        cage_adjacent_matrix[int(inp[0]) - 1][int(inp[1]) - 1], cage_adjacent_matrix[int(inp[1]) - 1][
            int(inp[0]) - 1] = 1, 1

    for i in range(animal_number):
        x = []
        inp = input().split()
        for j in range(animal_number):
            x.append(int(inp[j]))
        animal_matrix.append(x)
    # inp = input("enter cage numbers , animal numbers , adjacent numbers").split()
    #     cage_number = int(inp[0])
    #     animal_number = int(inp[1])
    #     adjacent_number = int(inp[2])
    #
    #     cage_adjacent_matrix = [[0 for i in range(cage_number)] for j in range(cage_number)]
    #
    #     inp = input("enter cage sizes ({} needed) : ".format(cage_number)).split()
    #     for i in range(cage_number):
    #         cages_size_list.append(int(inp[i]))
    #
    #     inp = input("enter animal sizes ({} needed): ".format(animal_number)).split()
    #     for i in range(animal_number):
    #         animals_size_list.append(int(inp[i]))
    #
    #     for i in range(adjacent_number):
    #         inp = input("adjacent ({} of {}) : ".format(i + 1, adjacent_number)).split()
    #         cage_adjacent_matrix[int(inp[0]) - 1][int(inp[1]) - 1], cage_adjacent_matrix[int(inp[1]) - 1][
    #             int(inp[0]) - 1] = 1, 1
    #
    #     print("enter animal matrix : \n")
    #     for i in range(animal_number):
    #         x = []
    #         inp = input().split()
    #         for j in range(animal_number):
    #             x.append(int(inp[j]))
    #         animal_matrix.append(x)

    back_track = BackTtrack(cage_number, animal_number, adjacent_number, cages_size_list, cage_adjacent_matrix,
                            animals_size_list, animal_matrix)
    # back_track.solve_backtrack()
    back_track.solve_forward_checking()
    # back_track.solve_mrv() #TODO
    # back_track.solve_lcv()
    # back_track.solve_mrv_lcv() #TODO
    print(back_track.assignment)


if __name__ == '__main__':
    main()
