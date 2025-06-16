import random
import string

def generar_pin():
    return "".join(random.choices(string.digits, k=6))