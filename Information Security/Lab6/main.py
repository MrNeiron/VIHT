from Encryption import ByteEncryption

originalText = input()
encryptedText = ByteEncryption(originalText)

print("Original sentence: " + str(originalText)
      +"\nEncrypted sentence: " + str(encryptedText))
