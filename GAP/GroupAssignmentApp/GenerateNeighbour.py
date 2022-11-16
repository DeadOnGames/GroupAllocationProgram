def generate_neighbour(td):
    perm = []
    l = len(td)
    print("array", td)
    if l == 0:
        return [[]]

    for i in range(l):
        tdi = td[i]
        m = len(tdi)
        for j in range(m-1):
            o = tdi[j]
            tnew = 0
            for k in range(j+1,m):
                tnew = td[i].copy()
                swap = tnew[k]
                tnew[j] = swap
                tnew[k] = o
                perm.append(tnew)
    
    return perm