def app():  
  totalFees = 0
  i = 0
  while i < Global.group_size:
    totalFees = totalFees + Gtxn[i].fee
    i = i + 1
  return 1
