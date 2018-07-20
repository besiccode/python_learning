
class Doy(object):

    def __init__(self, name):
        self.name = name

    def eat(self, food):
        print("%s is eating %s" % (self.name, food))


def boo(self):
    print("%s is booing" % self.name)


a = Doy("Alex")

choice = input(">>:").strip()

if hasattr(a, choice):
    fun = getattr(a, choice)
    fun("gali")
else:
    # print("a has no %s attribute" % choice)
    setattr(a, choice, boo)
    fun = getattr(a, choice)
    fun(a)



