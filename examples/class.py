def verbatim(x):
  return x

class Senior:
  @verbatim
  def __init__(self, name, age):
    self.age = age
    self.name = name

  @inline
  def isEligible(self):
    return self.age > 65

  @inline
  def evalAndPrint(self):
    a = 10
    if self.isEligible():
      print(self.name + " is eligible. " + Itob(a))
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
 
