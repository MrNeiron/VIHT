from string import ascii_lowercase as alphabet

def ShiftV2(orig, sh = 3, direction = -1):
  assert (direction == 1 or direction == -1)
  edit = ''
  for symbol in orig:
    edit += alphabet[alphabet.find(symbol) + sh * direction]
  return edit, sh, direction