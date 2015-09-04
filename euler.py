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

def p15(exp):
    tmp = str(pow(2,exp))
    val = 0
    for k in tmp:
        val += int(k)
    return k

ones = ['', 'one','two','three','four','five','six','seven','eight','nine']
tens1 = ['ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen']
tens = ['','','twenty','thirty','forty','fifty','sixty','seventy','eighty','ninety']
hundreds = map(lambda x: x+' hundred', ones)
thousands = map(lambda x: x+ ' thousand', ones)

def p16h(i):
    t = i / 1000
    h = (i-1000*t) / 100
    te= (i-1000*t-100*h) / 10
    tw= (i-1000*t-100*h) / 20
    o = i - 1000*t - 100*h - 10*te

    tmp = []

    if (t > 0):
        tmp.append(thousands[t])
    if (h > 0):
        tmp.append(hundreds[h])
    if (te==1):
        tmp.append(tens1[o])
    if (te==0) or (te>=2):
        val = tens[te]
        if (o>0):
            val += ones[o]
        tmp.append(val)
    out = " and ".join(tmp)
    if out[-5:]==" and ":
        out = out[0:-5]
    return out

def p16(a,b):
    val = 0
    for i in range(a, b+1):
        val += len(p16h(i).replace(' ', ''))
    return val


class TriDigit():
    def __init__(self, val):
        self.val = val
        self.children = set([])
        self.best = None
    def addchild(self, child):
        self.children.add(child)
    def addchildren(self, children):
        for k in children:
            self.addchild(k)
    def bestsum(self):
        if (self.best):
            return self.best
        if len(self.children) == 0:
            out = self.val
        else:
            out = self.val + max(map(lambda x: x.bestsum(), self.children))

        self.best = out
        return out
    def __repr__(self):
        return "TriDigit Val: %d" % self.val

def p17(filename):
    f = open(filename)
    lines = f.readlines()
    f.close()
    digs = map(lambda x: map(lambda y: TriDigit(int(y)), x.strip().split(' ')), lines)
    numrows = len(digs)
    for i in range(0, numrows-1):
        for j in range(0,i+1):
            #ipdb.set_trace()
            digs[i][j].addchildren([digs[i+1][j], digs[i+1][j+1]])
    return digs[0][0].bestsum()
