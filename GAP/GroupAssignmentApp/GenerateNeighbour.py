

def generate_neighbour(twoD):
    perm = []
    # perm = 3d array to be returned
    # twoD = 2d list
    if len(twoD) == 1:
        # if only one group is submitted, group is returned with no change
        return twoD
    elif len(twoD) == 0:
        # if no groups entered, warning message given
        return "Error: No groups submitted"

    twoDC = twoD.copy()
    for i in range(len(twoDC)):
        lst = twoDC[i]
        elem = lst[i]

        # lst is the i-th list in twoD
        newList = []
        newlist.append(elem)
        for j in range(i+1,len(twoDC)):
                       
            nextList = list[j]
            newElem = nextList[j-1]
            newList.append(newElem)

        perm.append(newList)

    


# testing:
# inputting two arrays with 2 elements each
print(generate_neighbour([[1,2],[3,4]]))
# inputting three arrays with 2 elements each
#print(generate_neighbour([[1,2],[3,4],[5,6]]))
# inputting 1 array
#print(generate_neighbour([1,2,3]))
#inputting an empty array
#print(generate_neighbour([]))