from copy import deepcopy
import math

AXES = [0,1,2]
CUBE_MAP = [2,1,1,2,1,2,1,1,2,2,1,1,1,2,2,2,2]

def walk(steps, axis, sign, path, map_index):
    # Copy args
    steps = deepcopy(steps)
    axis = deepcopy(axis)
    sign = deepcopy(sign)
    path = deepcopy(path)
    map_index = deepcopy(map_index)
    
   

    new_nodes = []
    current_node = path[-1]
    # Take the number of steps in the right direction
    for i in range(0, steps):
        new_node = deepcopy(current_node) 
        new_node[axis] += sign * (i + 1)
        if verify(new_node, path):
            # Node verified, remember it
            new_nodes.append(new_node)
        else:
            # Stop searching this branch
            return False

    new_path = deepcopy(path) # NOTE: copy might not be needed here
    new_path.extend(new_nodes)
    new_index = map_index + 1

    # debug
    print_path(new_path)
    print new_index

    # Success condition
    if len(new_path) == math.pow(len(AXES),3):
        print ' %%% SOLUTION FOUND %%% '
        return new_path
    
    # Otherwise keep walking
    for d in set(AXES) - set([axis]):
        for sign in (1,-1):
            walk_result = walk(steps=CUBE_MAP[new_index], axis=d, sign=sign, path=new_path, map_index=new_index)
            if walk_result:
                # Ignore falsy return values
                return walk_result

def verify(node, path):
    # verify that node exists
    for value in node:
        if value > 2 or value < 0:
            return False

    # verify that node is not in path
    if node in path:
        return False

    return True

def print_path(path):
    tmp_str = ''
    print 
    for i in range(0,3):
        print
        for j in range(0,3):
            tmp_str = ''
            for k in range(0,3):
                if [k, j, i] in path:
                    tmp_str += '* '
                else:
                    tmp_str += '- '
            print tmp_str

    print '=============='
    
if __name__ == '__main__':
    axis = 0
    path = [[0,0,0]]
    index = 0
    path = walk(steps=CUBE_MAP[index], axis=axis, sign=1, path=path, map_index=index)
    print path
