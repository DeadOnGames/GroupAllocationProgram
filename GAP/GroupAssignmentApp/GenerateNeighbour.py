def generate_neighbour(twoD):
    perm = []
    # perm = array to be returned: 3d array
    # twoD = 2d list
    if len(twoD) == 1:
        # if only one group is submitted, group is returned with no change
        return twoD
    elif len(twoD) == 0:
        # if no groups entered, warning message given
        return "Error: No groups submitted"

    twoDnew = twoD.copy()
    length = len(twoDnew)
    for i in range(length):
        newList = twoDnew[i]
        # newList is the i-th list in twoDnew

        


generate_neighbour([[1,2,3],[4,5,6]])