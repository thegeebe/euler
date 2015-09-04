import numpy

def parsegrid():
    f = open('grid.txt')
    lines = f.readlines()
    grid = []
    for l in lines:
        grid.append(map(lambda x: int(x), l.strip().split(' ')))
    f.close()
    return grid

def genConsecIdx(m,n,num):
    idx = []
    l = lambda x, y: (x[0]-y, x[1])
    r = lambda x, y: (x[0]+y, x[1])
    u = lambda x, y: (x[0], x[1]-y)
    d = lambda x, y: (x[0]-y, x[1]+y)
    dl = lambda x, y: d(l(x,y),y)
    dr = lambda x, y: d(r(x,y),y)
    ts = [l, r, u, d, dl, dr]

    ra = range(0,num)
    for i in range(0,m):
        for j in range(0,n):
            for t in ts:
                tmp = set([])
                for q in ra:
                    k = t((i,j), q)
                    if (k[0] < 0) or (k[1] < 0) or (k[0] >= m) or (k[1] >= n):
                        break
                    tmp.add(k)
                if (len(tmp) == num):
                    idx.append(tmp)

    return idx

def p11():
    res = genConsecIdx(20, 20, 4)

    grid = parsegrid()
    result = []
    for i in range(0, len(res)):
        path = res[i]
        tmp = 1
        for vert in path:
            tmp *= grid[vert[0]][vert[1]]
        result.append(tmp)
    return max(result)

def triangle(n):
    prev = 0
    i = 1
    while i <= n:
        yield prev+i
        prev += i
        i+=1

def factors(n):
    return set(reduce(list.__add__,
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))
def p12():
    MAX = 2e32
    for k in triangle(MAX):
        if len(factors(k)) > 500:
            break
    return k

def p13(n, lines=None):
    sum = 0
    if lines is None:
        f = open('largesum.txt')
        lines = f.readlines(); f.close()
        lines = map(lambda x: x.strip(), lines)
    for k in lines:
        sum += int(k[0:n])
    return sum

p14e = lambda x: x/2
p14o = lambda x: 3*x+1

def p14r(x, results={}):
    if (x==1):
        return 1
    elif (results.has_key(x)):
        return results[x]
    elif (x%2==0):
        return 1+p14r(p14e(x), results)
    else:
        return 1+p14r(p14o(x), results)

def p14(num):
    start = time.time()
    results = {}
    for i in range(1, num):
        chainlen = p14r(i, results)
        results[i] = chainlen
    tmp = [v for _,v in results.iteritems()]
    print "%d ms" % ((time.time() - start) * 1000)
    return numpy.argmax(tmp)+1
