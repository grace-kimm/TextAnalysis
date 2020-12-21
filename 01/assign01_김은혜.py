# Assign01_김은혜

# HW4
import sys
print("# HW4")

dict1 = {'Tom': 20}
print(dict1['Tom'])  # Tom's age
dict1['John'] = 30  # Add another person's age information : John, 30
print(len(dict1))  # the number of keys

dict1['Sarah'] = 28
dict1['Jack'] = 41
print(dict1.keys())  # the keys of the updated dictionary variable

# HW5
print("\n# HW5")
d = {
    "int": 0,
    "float": 0.0,
    "boolean": True,
    "str": "a",
    "list": list(),
    "dict": dict(),
    "set": set()
}
for key, value in d.items():
    print(key, sys.getsizeof(value))
