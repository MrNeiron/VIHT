from Users import User
from Rights import Rights as Rig
from random import shuffle, randrange

class Policity:

    def __init__(self):
        self.OBJECTS = ["obj1", "obj2", "obj3"]
        self.USERS = ["ivan", "larisa", "kolya", "petya"]
        self.NAMERIGHTS = Rig.NAMERIGHTS
        self.accessNameRights = {user: {object: self.__getRand() if user != self.USERS[0] else Rig.NAMERIGHTS[:3] for object in self.OBJECTS} for user in self.USERS}


    def __getRand(self):#To get some random values from list
        a = self.NAMERIGHTS[:3].copy()
        shuffle(a)
        return a[:randrange(1, len(a) + 1)]

    def Enter(self):#User identification and building user objects
        while True:
            userName = input("Login: ")
            if userName in self.USERS:
                print("Welcome {}!".format(userName))

                self.__status = {user: User(user, self.accessNameRights.get(user),"Admin" if user == self.USERS[0] else "Guest", Rig.NAMERIGHTS) for user in self.USERS}

                return self.__status.get(userName) if userName in self.__status.keys() else "none"
            else: print("Profile not found")

    def setRight(self, user = None, object = None, method = None):#To add some method(when creating new user)
        if object != None:
            if user in self.accessNameRights.keys():
                self.accessNameRights.get(user).get(object).append(method)
            else:
                if type(method) == list: self.accessNameRights[user] = {obj: method.copy() for obj in object}
                else:  self.accessNameRights[user] = {obj: [method] for obj in object}
        else:
            self.accessNameRights[user] = {object: self.__getRand() for object in self.OBJECTS}

    def getStatus(self, names = None):
        if names == None: names = self.__status.keys()
        else: names = [names]
        ret = ''
        for name in names: ret += "\n{}: {}".format(name, self.__status.get(name).getStatus())
        return ret

    def getAccessRights(self, names = None):
        if names == None: names = self.__status.keys()
        else: names = [names]
        ret = ''
        for name in names: ret += "\n{}: {}".format(name, self.__status.get(name).PrintObjects())
        return ret

    def getAccessNamesRights(self):
        return self.accessNameRights