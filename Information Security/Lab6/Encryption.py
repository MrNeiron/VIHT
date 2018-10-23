def ByteEncryption(word, key = 83):
  inputBytes = [ord(l) for l in word]
  #print(inputBytes)
  outputBytes = [l ^ key for l in inputBytes]
  newWord = "".join([chr(l) for l in outputBytes])
  return newWord