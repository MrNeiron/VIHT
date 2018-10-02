from Rights import Rights as Rig
class User:
    def __init__(self, name, objects, status, namerights):
        self.__name = name
        self.__status = status
        self.__objects = objects
        self.NAMERIGHTS = namerights
        self.methods = set()
        for objName in self.__objects.keys():
            for i in range(len(self.__objects.get(objName))):
                self.methods.add(self.__objects.get(objName)[i])
        self.AppendRights(self.methods)

    def getName(self):
        return self.__name

    def getObjects(self):
        return self.__objects

    def setObjects(self, object = None, meth = None):
        self.__objects[object].append(meth)

    def getStatus(self):
        return self.__status

    def PrintObjects(self):#To take objects
        ret = ''
        for key, value in self.__objects.items():
            ret += "\n\t{}: ".format(key)
            full = True
            if len(value) != len(self.NAMERIGHTS[:3]):
                full = False
            else:
                for i in range(len(self.NAMERIGHTS[:3])):
                    if value[i] not in self.NAMERIGHTS[:3]:
                        full = False
                        break
            if full:
                ret += str(self.NAMERIGHTS[-1])
            else:
                for i in range(len(value)): ret += value[i] if i+1 == len(value) else value[i] + ', '
        return ret

    def AppendRights(self, lstMethods):#Correlating method's name and list name
        for meth in lstMethods:
            setattr(User, meth, Rig.RIGHTS.get(meth))
