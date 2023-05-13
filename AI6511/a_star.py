import copy
import itertools
import heapq
#
start_status = [
    [1, 30, 3, 4, 14, 28, 7, 8, 23, 10],
    [11, 25, 13, 5, 15, 16, 26, 18, 19, 21],
    [20, 22, 9, 24, 12, 17, 27, 6, 29, 2]
]

# start_status = [
#     [1, 3, 2, 13, 5, 6, 7, 8, 28, 10],
#     [11, 12, 4, 14, 15, 16, 17, 18, 19, 20],
#     [21, 22, 23, 24, 25, 26, 27, 9, 29, 30]
# ]

target_status = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    [11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
    [21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
]


def generate_targets():
    ranges = [
        list(range(1, 11)),
        list(range(11, 21)),
        list(range(21, 31)),
    ]
    samples = []

    for perm in itertools.permutations(ranges):
        samples.append(list(perm))

    return samples


def cal_dic(status):
    dict_status = dict()
    for i in range(len(status)):
        for j in range(len(status[0])):
            dict_status[status[i][j]] = (i, j)
    return dict_status


def heuristic(current_status, target_status):
    # print("tar: ", target_status)
    current = cal_dic(current_status)
    res = 0
    for j in range(len(target_status)):
        for k in range(len(target_status[0])):
            ele = current[target_status[j][k]]
            x, y = ele[0], ele[1]
            res += abs(x - j) + abs(y - k)
    return res/2


def best_order(current_status, target_status):
    min_res = float('inf')
    for i in range(len(target_status)):
        res = 0
        res = heuristic(current_status, target_status[i])
        if res < min_res:
            min_res = res
            min_i = i
    return target_status[min_i], min_res


def astar(start_status):
    target_status = generate_targets()
    target, h = best_order(start_status, target_status)
    print(target, h)
    visited = set()
    visited.add(str(start_status))
    # fn,hn,gn,current_status,path
    queue = [(h, h, 0, start_status, [])]
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while queue:
        _, hn, gn, current_status, paths = heapq.heappop(queue)

        if current_status == target:
            return gn, paths
        for i in range(len(target)):
            for j in range(len(target[0])):
                for move in moves:
                    x, y = i + move[0], j + move[1]
                    if 0 <= x < len(start_status) and 0 <= y < len(start_status[0]):
                        new_state = copy.deepcopy(current_status)
                        # print("new: ",new_state)
                        new_state[i][j], new_state[x][y] = new_state[x][y], new_state[i][j]
                        new_gn = gn + 1
                        new_hn = heuristic(new_state, target)
                        # print(hn, new_hn)
                        assert hn <= new_hn + 1
                        new_paths = paths[:]
                        new_paths.append([i, j, x, y])
                        if str(new_state) not in visited:
                            heapq.heappush(queue, (new_gn + new_hn, new_hn, new_gn, new_state, new_paths))
                            visited.add(str(new_state))
    return

print(astar(start_status))
