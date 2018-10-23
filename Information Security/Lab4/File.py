class File():
  def __init__(self, name, rank, text = ""):
    self.name = name
    self.rank = rank
    self.text = text

  def getName(self):
    return self.name

  def setName(self, newName):
    self.name = newName

  def setText(self, text):
    self.text = text

  def getText(self):
    return self.text
