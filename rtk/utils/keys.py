import random


def generate_secret(chars='abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)', seed=None):
    return ''.join(random.Random(seed).choice(chars) for i in range(50))
