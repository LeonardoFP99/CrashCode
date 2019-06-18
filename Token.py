import random
import string

def gerarToken():
  chars_digits = string.ascii_letters + string.digits
  return ''.join(random.choice(chars_digits) for i in range(20))
