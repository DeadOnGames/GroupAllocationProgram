
def generate_neighbour(td):
    
    l = len(td)
    print("array", td)
    if l == 0:
        return [[]]

    for i in range(l):
        tdi = td[i]
        m = len(tdi)

        for j in range(m):
            o = tdi[j]
            for k in range(j,m-1):
                tnew = tdi
                print("before: ", tnew)
                swap = tnew[k+1]
                tnew[k+1] = o
                tnew[j] = swap
                print(tnew)
                
           

print(generate_neighbour([[1,2,3]]))