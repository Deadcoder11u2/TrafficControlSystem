def flip_signal(wait_array):
    isRed = [False]*19
    for i in range(1, 19, 2):
        sig1 = wait_array[i]
        sig2 = wait_array[i+1]
        if sig1 < sig2:
            isRed[i] = True
        else:
            isRed[i+1] = True
    return isRed


# def branching_and_bounding(lb, root):
#     time = lb[root]

#     for j in range(2, len(lb), 1):


# def branching(node, lb):
    