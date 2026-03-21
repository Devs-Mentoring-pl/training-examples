"""
Szkolenie 4 Listy skladane i Generatory - Przyklad 4
Zaawansowane metody generatorow: send(), throw(), close().
"""


# ========== send() - wysylanie wartosci do generatora ==========

def accumulator():
    """Akumulator przesylanych wartosci."""
    total = 0
    value = None
    while True:
        value = yield total   # odbieramy wyslana wartosc
        if value is None:
            break
        total += value        # kumulujemy wartosci

    yield total


print("=== send() - akumulator ===")
generator = accumulator()
next(generator)             # inicjalizacja generatora
generator.send(0)
generator.send(5)
generator.send(10)
generator.send(5)
generator.send(1)
result = next(generator)    # rownowazne generator.send(None) - konczy petle
print(f"Suma skumulowana: {result}")   # 21


# ========== throw() - rzucanie wyjatku w generatorze ==========

def gen_infinite_nums():
    num = 0
    while True:
        yield num
        num += 1


print("\n=== throw() - przerwanie generatora wyjatkiem ===")
generator2 = gen_infinite_nums()
print(f"next(): {next(generator2)}")   # 0
print(f"next(): {next(generator2)}")   # 1

for val in generator2:
    if val >= 10:
        try:
            generator2.throw(ValueError("Too big value!"))
        except ValueError as e:
            print(f"Przechwycono: {e}")
            break
    else:
        print(f"  val = {val}")


# ========== close() - zamkniecie generatora ==========

print("\n=== close() - lagodne zamkniecie generatora ===")
generator3 = gen_infinite_nums()
print(f"next(): {next(generator3)}")   # 0
print(f"next(): {next(generator3)}")   # 1

for val in generator3:
    if val >= 10:
        generator3.close()
    else:
        print(f"  val = {val}")

print("Generator zamkniety bez bledu.")
