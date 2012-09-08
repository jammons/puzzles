from copy import deepcopy
AXES = [0,1,2]
CUBE_MAP = [2,1,1,2,1,2,1,1,2,2,1,1,1,2,2,2,2]

def walk(direction, path, map):
    print map
    print_path(path)
    direction = deepcopy(direction)
    path = deepcopy(path)
    map = deepcopy(map)
    try:
        num_steps = map[0]
    except IndexError:
        print "#@#$@#$@#$@#$@#"
        return path #complete
 
    if num_steps == 0:
        if len(map) == 1 and map[0] == 0:
            return path
        # change direction then walk
        print 'change direction'
        map = map[1:]
        # try different directions
        for new_direction in set(AXES) - set([direction]):
            for orientation in (1, -1):
                new_node = deepcopy(path[-1])
                new_node[new_direction] += orientation
                if not verify(new_node, path):
                    print 'failed'
                    continue
                else:
                    new_map = deepcopy(map)
                    new_map[0] = new_map[0] - 1
                    new_path = deepcopy(path)
                    new_path.append(new_node)
                    path = walk(new_direction, new_path, new_map)
                    if path:
                        return path
    else:
        for orientation in (1, -1):
            new_node = deepcopy(path[-1])
            new_node[direction] += orientation
            if not verify(new_node, path):
                print 'failed'
                continue
            else:
                new_map = deepcopy(map)
                new_map[0] = new_map[0] - 1
                new_path = deepcopy(path)
                new_path.append(new_node)
                path = walk(direction, new_path, new_map)
                if path:
                    return path

def verify(node, path):
    # verify that node exists
    for axis in node:
        if axis > 2 or axis < 0:
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
    direction = 0
    path = [[0,0,0]]

    path = walk(direction, path, CUBE_MAP)
    print path
    print len(path)
    
    
