
def generate_neighbour(td):
    perm = []
    l = len(td)
    print("array", td)
    if l == 0:
        return [[]]

    for i in range(l):
        tdi = td[i]
        
        m = len(tdi)
        if m == 1:
            perm.append(tdi)
        for j in range(m):
            o = tdi[j]
            for k in range(j,m-1):
                n = tdi[k+1]
                print("n", n)
                tdinew = tdi
                tdinew[k+1] = o
                tdinew[j] = n
                print(tdinew)
                perm.append(tdinew)

    return perm

print(generate_neighbour([[1,2,3]]))