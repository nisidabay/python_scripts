import itertools


def permutation(string):
    if len(string) == 0:
        return ['']
    prev_list = permutation(string[1:])
    next_list = []
    for i, j in itertools.product(range(len(prev_list)), range(len(string))):
        new_str = prev_list[i][:j] + string[0] + prev_list[i][j:len(string) -
                                                              1]
        if new_str not in next_list:
            next_list.append(new_str)
    return next_list


print(permutation("ABC"))
