class Rights:

    NAMERIGHTS = ["Read", "Write", "Transfer_of_rights", "Full access"]
    def Read(cls, obj, curFile):
      return curFile.getText()
      #return("You can read {}!".format(obj))
    def Write(cls, obj):
        return("You can write {}!".format(obj))

    def Transfer_of_rights(cls, sender = None, recipient = None, object = None, method = None, lst = None):
      if sender != None:
        if Rights.NAMERIGHTS[2] in lst[sender][object]:
            if method not in lst[recipient][object]:
                print(lst.get(recipient))
                lst.get(recipient).get(object).append(method)
                return lst[recipient]
        else: return print("You can't do it")

      else: return "You can transfer rights now!"

    RIGHTS = {NAMERIGHTS[0]: classmethod(Read), NAMERIGHTS[1]: classmethod(Write),
                   NAMERIGHTS[2]: classmethod(Transfer_of_rights)}