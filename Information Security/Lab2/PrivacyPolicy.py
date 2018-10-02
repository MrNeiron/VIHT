from Policity import Policity

ACTIONS = ("help", "select object","change user", "append user", "show users", "show info", "show all rights", "delete user", "exit")

polit = Policity()

user = polit.Enter()
print("Status: {}\nFiles: {}".format(user.getStatus(), user.PrintObjects()))

while True:
    [print('_', end='') for _ in range(50)]
    print('\n')
    action = input("({})Select action: ".format(user.getName())).lower()
    if (action == ACTIONS[0]):#help
        [print(action) for action in ACTIONS]

    elif (action == ACTIONS[1]):#select object
        obj = input("Filename = ")
        if obj == ACTIONS[-1] or obj not in polit.OBJECTS: continue
        act = input("Action = ")
        if act == "transfer": act = polit.NAMERIGHTS[-2]
        if act in user.methods:
            if act == polit.NAMERIGHTS[-2]:
                recipient  = input("Recipient: ")
                if recipient in polit.USERS:
                    act2 = input("Right = ")
                    if act2 == "transfer": act2 = polit.NAMERIGHTS[-2]
                    getattr(user, act)(user.getName(), recipient, obj, act2, polit.accessNameRights)
                    print("{}".format(polit.getAccessRights(recipient)))
            else:
                if act in user.getObjects().get(obj):
                    print(getattr(user, act)(obj))
                else: print("No, you can't do it")
        else:print("No, you can't do it")

    elif (action == ACTIONS[2]):#change user
        user = polit.Enter()
        print("Status: {}\nFiles: {}".format(user.getStatus(), user.PrintObjects()))

    elif (action == ACTIONS[3]):#append user
        newName = input("New login: ")
        if newName not in polit.USERS:
            polit.USERS.append(newName)
            polit.setRight(polit.USERS[-1])
            print("User added!")
        else: print("User already added!")

    elif (action == ACTIONS[4]):#show users
        [print(str(i+1)+')'+user) for i,user in enumerate(polit.USERS)]

    elif (action == ACTIONS[5]):#show info
        print("Login: {}\nStatus: {}\nFiles: {}".format(user.getName(),user.getStatus(), user.PrintObjects()))

    elif (action == ACTIONS[6]):#show all rights
        print("{}".format(polit.getAccessRights()))

    elif (action == ACTIONS[7]):#delete user
        delUser = input("Deleted user: ")
        if delUser in polit.USERS and delUser != polit.USERS[0]:
            polit.USERS.remove(delUser)
    elif (action == ACTIONS[-1]):#exit
        print("ok, exit")
        break
    else:#smth else
        print("try again!")

