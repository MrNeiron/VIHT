from math import ceil
from string import ascii_lowercase as low, ascii_uppercase as up
from random import choice
from timeit import default_timer as timer

def CeilPow(alphabet, limit):
    power= 0
    while alphabet**power < limit: power+=1
    return alphabet, power

def GenPass(p = 10 **-6,v = 10, t = 5, login = None, alphabet = 26, countFunction = CeilPow):
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

password = GenPass()
input("\npress Enter")