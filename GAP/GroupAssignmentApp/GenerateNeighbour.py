def generate_neighbours(iter_2d):
    perm = []
    # perm = 3d array to be returned
    # iter_2d = 2d iterable
    if len(iter_2d) == 1:
        # if only one group is submitted, group is returned with no change
        return [iter_2d]
    elif len(iter_2d) == 0:
        # if no groups entered, warning message given
        return "Error: No groups submitted"

    for i in range(len(iter_2d) - 1):

        twoDC = iter_2d.copy()
        iList = twoDC[i]
        iList2 = twoDC[i + 1]
        for j in range(len(iList)):
            for k in range(len(iList2)):
                return perm
