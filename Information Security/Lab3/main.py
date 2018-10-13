from Policity import Policity

ACTIONS = ("help", "select object","change user", "append user", "show users", "show info", "show all rights", "show ranks", "show objects rank","delete user", "exit")

polit = Policity()

user = polit.Enter()
if (user != "exit"):
  print("Status: {}\nRank: {}\nFiles: {}".format(user.getStatus(),user.getRank(), user.PrintObjects()))
  print("\nActions:")
  [print('\t'+action) for action in ACTIONS]

  while True:
      [print('_', end='') for _ in range(50)]
      print('\n')
      action = input("({})Select action: ".format(user.getName())).lower()
      if (action == ACTIONS[0]):#help
          print("\nActions:")
          [print('\t'+action) for action in ACTIONS]  

      elif (action == ACTIONS[1]):#select object
          obj = input("Filename = ")
          if obj == ACTIONS[-1] or obj not in polit.OBJECTS: continue
          if user.getRank() > polit.getFiles(obj).getRank():
            print("You don't have enough rank!")
            continue
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
                      obj2 = polit.getFiles(obj)
                      print(getattr(user, act)(obj, obj2))
                  else: print("No, you can't do it")
          else:print("No, you can't do it")

      elif (action == ACTIONS[2]):#change user
          print("...exit")
          [print('_', end='') for _ in range(50)]
          print()
          user = polit.Enter()
          if user == "exit": 
            print("ok, exit")
            break
          print("Status: {}\nRank: {}\nFiles: {}".format(user.getStatus(),user.getRank(), user.PrintObjects()))
          print("\nActions:")
          [print('\t'+action) for action in ACTIONS]  

      elif (action == ACTIONS[3]):#append user
          newName = input("New login: ")
          if newName not in polit.USERS and newName != "exit":
              polit.USERS.append(newName)
              polit.setRight(polit.USERS[-1])
              polit.setRank(polit.USERS[-1])
              print("User added!")
          else: print("User already added!")

      elif (action == ACTIONS[4]):#show users
          [print(str(i+1)+')'+user) if user != polit.USERS[0] else print(str(i+1)+')'+user + "(admin)")  for i,user in enumerate(polit.USERS)]

      elif (action == ACTIONS[5]):#show info
          print("Login: {}\nStatus: {}\nRank: {}\nFiles: {}".format(user.getName(),user.getStatus(),user.getRank(), user.PrintObjects()))

      elif (action == ACTIONS[6]):#show all rights
          print("{}".format(polit.getAccessRights()))

      elif (action == ACTIONS[7]):#show ranks
          print("{}".format(polit.getRanks()))
      
      elif (action == ACTIONS[8]):#show objects rank
          [print("{}: {}".format(myFile.getName(),myFile.getRank())) for myFile in polit.getFiles().values()]

      elif (action == ACTIONS[9]):#delete user
          [print(str(i+1)+')'+user) if user != polit.USERS[0] else print(str(i+1)+')'+user + "(admin)")  for i,user in enumerate(polit.USERS)]
          delUser = input("\nDeleted user: ")
          if delUser in polit.USERS and delUser != polit.USERS[0]:
              polit.USERS.remove(delUser)
              del polit.usersRanks[delUser]
              print("Complete!")
          else: print("Can't do that!")

      elif (action == ACTIONS[-1]):#exit
          print("ok, exit")
          break
      else:#smth else
          print("try again!")
else: print("ok, exit")

