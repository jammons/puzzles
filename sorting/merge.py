# Should perform merge sort on the given list
ul = [4,2,9,20,292,4,37,8,273,49]

def merge(l1, l2):
    i, j = 0, 0 
    new_list = []
    while i<len(l1) and j<len(l2):
        #print l1[i], l2[j]
        if l1[i] <= l2[j]:
            new_list.append(l1[i])
            i += 1
        else:
            new_list.append(l2[j])
            j += 1
        
    new_list += l1[i:]
    new_list += l2[j:]
    return new_list

def mergesort(ul):
    if len(ul) <= 1:
        return ul
    else:
        midway = len(ul) / 2
        s1 = mergesort(ul[:midway])
        s2 = mergesort(ul[midway:])
        return merge(s1, s2)

sl = mergesort(ul)
print sl

