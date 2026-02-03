import random
import string

length = 64
random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
print(random_string)
