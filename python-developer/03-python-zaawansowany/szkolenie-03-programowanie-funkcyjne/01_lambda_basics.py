"""
Szkolenie 3 Programowanie funkcyjne - Przyklad 1
Lambdy - funkcje anonimowe: jednoargumentowa, bezargumentowa, wieloargumentowa.
"""


# Lambda jednoargumentowa
caster = lambda x: x % 2

print("=== Lambda jednoargumentowa ===")
print(f"caster(5)  = {caster(5)}")    # 5 % 2 = 1
print(f"caster(10) = {caster(10)}")   # 10 % 2 = 0

# Lambda bezargumentowa
say_hello = lambda: print("Hello!")
print("\n=== Lambda bezargumentowa ===")
say_hello()

# Lambda wieloargumentowa
caster2 = lambda x, y: x % y

print("\n=== Lambda wieloargumentowa ===")
print(f"caster2(5, 2)  = {caster2(5, 2)}")    # 1
print(f"caster2(10, 3) = {caster2(10, 3)}")    # 1
print(f"caster2(1, 5)  = {caster2(1, 5)}")     # 1

# Porownanie lambdy ze zwykla funkcja
def caster_func(a, b):
    return a % b

print("\n=== Porownanie: lambda vs def ===")
print(f"lambda:   {caster2(10, 3)}")
print(f"def:      {caster_func(10, 3)}")
