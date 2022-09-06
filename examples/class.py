

def verbatim(x):
  pass


class Senior:

  @verbatim
  def __init__(self, name, age):
    self.age_ = Int(age)
    self.name_ = Bytes(name)

  @inline
  def isEligible(self):
    return self.age > 65

  @inline
  def evalAndPrint(self):
    if self.isEligible():
      print(self.name + " is eligible.")
    else:
      print(self.name + " is too young.")


def app():
  mary = Senior('Mary', 62)
  tom = Senior('Tom', 75)

  mary.evalAndPrint()
  tom.evalAndPrint()

  return 1


  #@inline
  #def init(self):
  #  self.age = Int(self.age_)
  #  self.name = Bytes(self.name_)
 
