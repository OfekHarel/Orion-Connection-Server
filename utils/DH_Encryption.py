import random


def generate_prime() -> int:
    min = 1
    max = 50
    cached_primes = [i for i in range(min, max) if __is_prime__(i)]
    n = random.choice(cached_primes)
    return n


def __is_prime__(num) -> bool:
    if num > 1:
        for i in range(2, num):
            if (num % i) == 0:
                return False
            else:
                return True
    else:
        return False


def generate_n() -> int:
    min = 10
    max = 100
    num = random.randint(min, max)
    return num


class Encryption:
    def __init__(self, g, n):
        self.g = g
        self.n = n
        self.private_key = generate_prime()
        self.full_key = None

    def get_partial_key(self) -> int:
        return (self.g ** self.private_key) % self.n

    def get_full_key(self, partial_key_r) -> int:
        full_key = (partial_key_r ** self.private_key) % self.n
        self.full_key = full_key
        return full_key

    def encrypt_message(self, message) -> str:
        encrypted_message = ""
        for c in message:
            encrypted_message += chr((ord(c) + self.full_key) % 256)
        return encrypted_message

    def decrypt_message(self, encrypted_message) -> str:
        decrypted_message = ""
        for c in encrypted_message:
            decrypted_message += chr((ord(c) - self.full_key) % 256)
        return decrypted_message

