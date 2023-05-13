# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# You are given a 5 x 5 grid, and this grid should hold the letters A through Y.
# Some of the cells in the grid are already filled out.  The others can go anywhere,
# but the constraint is that adjacent letters (for example F and G) must be adjacent to each other, either horizontally or vertically.
#
# -    -    -    -    Y
# R    A    -    -    -
# -    -    -    -    -
# -    E    -    -    -
# -    -    -    -    K
#
# Design a solution for this constraint satisfaction problem.
# (Solution should explain the variables, the domain values, the constraints, and how the constraint propagation would work.)


field = [
    [" ", " ", " ", " ", "Y"],
    ["R", "A", " ", " ", " "],
    [" ", " ", " ", " ", " "],
    [" ", "E", " ", " ", " "],
    [" ", " ", " ", " ", "K"]
]


# field2 = [
#     ['A', 'B', 'C', 'D', 'E'],
#     ['J', 'I', 'H', 'G', 'F'],
#     ['K', 'L', 'M', 'N', 'O'],
#     ['T', 'S', 'R', 'Q', 'P'],
#     ['U', 'V', 'W', 'X', 'Y']
# ]

# for row in field:
#     for value in row:
#         print(value, end=" ")
#     print()


def append_to_sequence(sequence, key, i, j):
    if key not in sequence:
        sequence[key] = []

    if i - 1 >= 0 and field[i - 1][j] == ' ':
        sequence[key].append([i - 1, j])

    if j - 1 >= 0 and field[i][j - 1] == ' ':
        sequence[key].append([i, j - 1])

    if i + 1 < len(field) and field[i + 1][j] == ' ':
        sequence[key].append([i + 1, j])

    if j + 1 < len(field) and field[i][j + 1] == ' ':
        sequence[key].append([i, j + 1])


# Calculate if there is a position around the current letter that can be assigned,
# if exist calculate the previous and next letter of it and record that position to an assign map
def mrv(field, record):
    sequence = {}

    for element in field:
        for item in element:
            if item != ' ':
                record.add(item)

    for i in range(len(field)):
        for j in range(len(field[i])):
            cur = field[i][j]
            if cur != " ":
                if ord(cur) - 1 >= ord('A') and chr(ord(cur) - 1) not in record:
                    prev_key = chr(ord(cur) - 1)
                    if prev_key not in sequence:
                        sequence[prev_key] = []
                    append_to_sequence(sequence, prev_key, i, j)

                elif ord(cur) + 1 <= ord('Y') and chr(ord(cur) + 1) not in record:
                    next_key = chr(ord(cur) + 1)
                    if next_key not in sequence:
                        sequence[next_key] = []
                    append_to_sequence(sequence, next_key, i, j)

    sequence = dict(sorted(sequence.items(), key=lambda x: len(x[1])))
    return sequence


# calculate the number of position which is not assign, it is the influence of current position
def lcv(field, sequence):
    influence = [[0] * len(row) for row in field]
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == ' ':
                if i - 1 >= 0 and field[i - 1][j] == ' ':
                    influence[i][j] += 1
                if i + 1 < len(field) and field[i + 1][j] == ' ':
                    influence[i][j] += 1
                if j - 1 >= 0 and field[i][j - 1] == ' ':
                    influence[i][j] += 1
                if j + 1 < len(field[i]) and field[i][j + 1] == ' ':
                    influence[i][j] += 1

    return influence


def is_alphabet_sequence(field):
    if not field or len(field) == 0 or len(field[0]) == 0:
        return False

    rows = len(field)
    cols = len(field[0])

    directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]
    letters_found = set()

    for i in range(rows):
        for j in range(cols):
            current = field[i][j]
            if 'A' <= current <= 'Y':
                letters_found.add(current)
                found_next = False
                for dir in directions:
                    new_row = i + dir[0]
                    new_col = j + dir[1]

                    if 0 <= new_row < rows and 0 <= new_col < cols:
                        if field[new_row][new_col] == chr(ord(current) + 1):
                            found_next = True
                            break
                if not found_next and current != 'Y':
                    return False

    return len(letters_found) == 25


def csp(field, record):
    # If find the answer return true
    if is_alphabet_sequence(field):
        return True
    # print(field)
    # Calculate the order of filling in the blanks
    sequence = mrv(field, record)
    # AC3,if there is no possible, return it
    for value in sequence.values():
        if len(value) == 0:
            return False
    # Calculate how many position selections each space can influence
    influence = lcv(field, sequence)
    # sort the influence increased
    sorted_sequence = {
        key: sorted(values, key=lambda x: influence[x[0]][x[1]], reverse=True)
        for key, values in sequence.items()
    }

    for key in sequence:
        if key not in record:
            # choose each from the record
            for indices in sequence[key]:
                i, j = indices
                record.add(key)
                field[i][j] = key
                if csp(field, record):
                    return True
                field[i][j] = ' '
                record.remove(key)
            if key not in record:
                return False
    return False


for row in field:
    for value in row:
        print(value, end=" ")
    print()

record = set()
if csp(field, record):
    # print(field)
    for row in field:
        for value in row:
            print(value, end=" ")
        print()
else:
    print("can not find")
