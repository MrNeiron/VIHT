def Shift(orig, dist = 1):
  return orig[-dist:] + orig[:-dist], dist