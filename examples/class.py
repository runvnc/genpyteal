class Senior:

  @verbatim
  def xini(name, age):
    self.age_ = age
    self.name_ = name

  @inline
  def init(self):
    self.age = Int(self.age_)
    self.name = Bytes(self.name_)
   
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
  mary.init()
  tom = Senior('Tom', 75)
  tom.init()

  mary.evalAndPrint()
  tom.evalAndPrint()

  return 1
