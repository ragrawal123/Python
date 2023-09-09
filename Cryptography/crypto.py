import math
import random

# Caesar Cipher
# Arguments: string, integer
# Returns: string
def encrypt_caesar(plaintext, offset):
    encryptedString = ""
    alpha = "ABCDEFGHIJKLMNOPOQSTUVWXYZ"
    begNum = 65
    endNum = 90
    numInAlpha = 26
    for character in plaintext:
        if character in alpha:
            numValue = ord(character) - begNum
            if numValue + offset > numInAlpha - 1:
                encryptedString += encrypt_help(numValue, offset)
            else:
                encryptedString += (chr(ord(character) + offset))
        else:
            encryptedString = "No message received"
    return encryptedString

#Arguments: integer, integer
#Returns: string
def encrypt_help(numValue, offset):
    eString = ""
    numInAlpha = 26
    begNum = 65
    numValue = (numValue + offset)%numInAlpha
    eString = chr(numValue + begNum)
    return eString

# Arguments: string, integer
# Returns: string
def decrypt_caesar(ciphertext, offset):
    decryptedString = ""
    alpha = "ABCDEFGHIJKLMNOPOQSTUVWXYZ"
    begNum = 65

    for character in ciphertext:
        if character in alpha:
            numValue = ord(character) - begNum
            if numValue - offset < 0:
                decryptedString += decrypt_help(numValue, offset)
            else:
                decryptedString += (chr(ord(character) - offset))
        else:
            decryptedString = "No message received"
    return decryptedString

#Arguments: integer, integer
#Returns: string
def decrypt_help(numValue, offset):
    dString = ""
    numInAlpha = 26
    begNum = 65
    numValue = (numValue - offset)% numInAlpha
    eString = chr(numValue + begNum)
    return eString

# Vigenere Cipher
# Arguments: string, string
# Returns: string
def encrypt_vigenere(plaintext, keyword):
    keyword = vigenere_key(plaintext, keyword)
    encryptList = []
    begNum = 65;
    for character in range(len(plaintext)):
        numValue = (ord(plaintext[character]) + ord(keyword[character])) % 26
        numValue += begNum;
        encryptList.append(chr(numValue))
    encryptedWord = "".join(encryptList)
    return encryptedWord

# Arguments: string, string
# Returns: string
def decrypt_vigenere(ciphertext, keyword):
    keyword = vigenere_key(ciphertext, keyword)
    decryptList = []
    begNum = 65
    for character in range(len(ciphertext)):
        numValue = (ord(ciphertext[character]) - ord(keyword[character])) % 26
        numValue += begNum
        decryptList.append(chr(numValue))
    decryptedWord = "".join(decryptList)
    return decryptedWord

#Arguments: string, string
#Returns: string
def vigenere_key(plaintext, keyword):
    keylist = list(keyword)
    if len(plaintext) == len(keylist):
        return keyword
    if len(plaintext) < len(keyword):
        keylist = keyword[0:len(keyword)-(len(keyword)-len(plaintext))]
        return ("".join(keylist))
    else:
        for character in range(len(plaintext)-len(keylist)):
            keylist.append(keylist[character%len(keylist)])
    newKeyWord = "".join(keylist)
    return newKeyWord

# Merkle-Hellman Knapsack Cryptosystem
# Arguments: integer
# Returns: tuple (W, Q, R) - W a length-n tuple of integers, Q and R both integers
def generate_private_key(n=8):
    W = []
    total = 1
    for bit in range(n):
        num = random.randint(total + 1, 2 *total)
        total += num
        W.append(num)
    Q = random.randint(total, total*2)
    R = random.randint(2, Q-1)
    while(math.gcd(R, Q) != 1):
        R = random.randint(2, Q-1)
    return (tuple(W), Q, R)
    
# Arguments: tuple (W, Q, R) - W a length-n tuple of integers, Q and R both integers
# Returns: B - a length-n tuple of integers
def create_public_key(private_key):
    W, Q, R = private_key
    B = []
    for element in W:
        B.append((R * element) % Q)
    return tuple(B)

# Arguments: string, tuple B
# Returns: list of integers
def encrypt_mhkc(plaintext, public_key):
    encrypted = []
    M = []
    for character in plaintext:
        C = 0
        M = byte_to_bit(ord(character))
        for position in range (0, 8):
            mPosition = int(M[position])
            keyPosition = int(public_key[position])
            C += (mPosition*keyPosition)
        encrypted.append(C)
    return encrypted

#Arguments: integer
#Returns: List of integers(1s and 0s)
def byte_to_bit(byte):
    bits = []
    binary = bin(byte)[2:]
    for element in binary:
        bits.append(element)
    if len(bits) < 8:
        remainder = 8 % len(bits)
        for num in range(0, remainder):
            bits.insert(0, 0)
    return bits

# Arguments: list of integers, private key (W, Q, R) with W a tuple.
# Returns: bytearray or str of plaintext
def decrypt_mhkc(ciphertext, private_key):
    W = private_key[0]
    Q = private_key[1]
    R = private_key[2]
    S = findS(R, Q)
    Decrypted = []
    for character in ciphertext:
        C = character * S % Q
        bitString = []
        for element in reversed(W):
            if element <= C:
                bitString.append(1)
                C = C - element
            else:
                bitString.append(0)
        Decrypted.append(chr(bits_to_byte(reversed(bitString))))
    return "".join(Decrypted)

#Arguments: integer, integer
#Returns: integer
def findS(R, Q):
    for S in range(2,Q):
        if (R * S % Q == 1):
            return S
    return 0

#Arguments: List of integers(1s and 0s)
#Returns: integer
def bits_to_byte(bits):
    bitsAsStrings = []
    for element in bits:
        bitsAsStrings.append(str(element))
    bitString = "".join(bitsAsStrings)
    decimal = int(bitString, 2)
    return decimal

def main():
    # Testing code here
    caesar()
    vigenere()
    MHKC()
    
#Does Caesar Cipher 
def caesar():
    encryptCaesar = encrypt_caesar("ABCDE", 5)
    print("Caesar Encryption: " + encryptCaesar)
   
    decryptCaesar = decrypt_caesar(encryptCaesar, 5)
    print("Caesar Decryption: " + decryptCaesar)

#Does Vigenere Cipher
def vigenere():
    plaintext = "ATTACKATDAWN"
    keyword = "LEMON"
    
    encryptVigenere = encrypt_vigenere(plaintext, keyword)
    print("Vigenere Encryption: " + encryptVigenere)
    
    decryptVigenere = decrypt_vigenere(encryptVigenere, keyword)
    print("Vigenere Decryption: " + decryptVigenere)

#Does MHKC Cipher
def MHKC():
    privateKey = generate_private_key()
    publicKey = (create_public_key(privateKey))
    
    encryptedMHKC = (encrypt_mhkc("ATTACKATDAWN", publicKey))
    print(encryptedMHKC)
    
    print("Decrypted MHKC: " + decrypt_mhkc(encryptedMHKC, privateKey))

if __name__ == '__main__':
    main()
