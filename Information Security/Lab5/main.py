from Shift import Shift
from ShiftV2 import ShiftV2

text = input("Enter text: ")
newText,sh = Shift(text)

print("Type: Shift")
print("Shift: ", sh)
print("Original text: ", text)
print("Edited Text: ", newText)

newText2, sh2, direction = ShiftV2(text)

print("\nType: ShiftV2")
print("Shift: ", sh2)
print("Direction: ", direction)
print("Original text: ", text)
print("Edited Text: ", newText2)

