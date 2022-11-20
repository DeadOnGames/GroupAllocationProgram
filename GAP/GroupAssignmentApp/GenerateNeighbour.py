

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

    
    for i in range(len(twoD)-1):
        twoDC = twoD.copy()
        iList = twoDC[i]
        # iList is the i-th list in twoD
        elem = iList[i+1]
        # elem is the i-th element of the i-th list
        for j in range(i,len(twoD)-1):
            # jList is the j\+!-th list of twoD
            jList = twoDC[j+1]
            for k in range(len(twoDC[j])):
                twoDC = twoD.copy()
                elemJ = jList[k]
                twoDC[i][i+1] = elemJ
                twoDC[j+1][k] = elem
                perm.append(twoDC)


            

    return perm


    


# testing:
# inputting two arrays with 2 elements each
print(generate_neighbour([[1,2],[3,4]]))

# inputting three arrays with 2 elements each
#print(generate_neighbour([[1,2],[3,4],[5,6]]))
# inputting 1 array
#print(generate_neighbour([1,2,3]))
#inputting an empty array
#print(generate_neighbour([]))