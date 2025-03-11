import random
import string

string_hasil = []

# Membuat string acak yang terdiri dari huruf, angka, dan karakter spesial
characters = string.ascii_letters + string.digits + string.punctuation

string_hasil.append(''.join(random.choice(string.ascii_letters) for i in range(5)))

string_hasil.append(''.join(random.choice(string.digits) for i in range(5)))

string_hasil.append(''.join(random.choice(string.punctuation) for i in range(5)))

result = ''.join(string_hasil)

print("Random String:", result)