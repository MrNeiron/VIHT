from math import ceil
from string import ascii_lowercase as low, ascii_uppercase as up
from random import choice
from timeit import default_timer as timer

def CeilPow(alphabet, limit):
    power= 0
    while alphabet**power < limit: power+=1
    return alphabet, power

def CheckParam(val, typeVal, str, const=0):
    while type(val) is not typeVal:
        try:
            inp = input(str)
            val = typeVal(inp) if inp != 'n' else const
        except:
            print("Try again!")
    return val


def GenPass(p = None,v = None, t = None, login = None, alphabet = None, edit = False, countFunction = CeilPow):
    if edit:
        p1 = CheckParam(p, int, "Enter P: ", 10)
        p = p1**CheckParam(p, int, "Enter P(power): ", -6)
        v = CheckParam(v, int, "Enter V: ", 10)
        t = CheckParam(t, int, "Enter T(days): ", 5)
        alphabet = CheckParam(alphabet, int, "Enter A: ", 26)
    login = input("Enter login: ") if login is None else login
    tup = ('!', '"', '#', '$', '%', '&', "'", '(', ')', '*')
    start = timer()

    a = countFunction(alphabet, ceil(v * (t * 24 * 60) / p))
    s2 = a[0] ** a[1]
    password = ''.join([choice(low) for _ in range(3)] + [choice(tup) for _ in range(3)] + [choice(up)] + [low[len(login)**2 % 10 + len(login)**3 % 10 + 1]])
    print("\nPassword power: ", s2)
    print("Min password length: ", a[1])
    print("\n{:<20}|\t{:<20}|\t{:<20}\n{:<20}|\t{:<20}|\t{:.10f} sec.\t".format("Login:", "Password:", "Time:", login, password, (timer() - start)))
    return password

password = GenPass(edit= True)
input("\npress Enter")