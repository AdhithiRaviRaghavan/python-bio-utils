# manny's code
def func1(a, b):
    for i in range(1,100):

        b = b - 1

        print("iteration {} : {}\n".format(i, i/a))
        a = a - b

def func2(a):
    c = 5
    func1(a, c)

a = 10

func2(a)

