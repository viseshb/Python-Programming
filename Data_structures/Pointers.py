num1 = 11

num2 = num1

print("Before num2 is updated:")
print("num1 =",num1)
print("num2 =",num2)

print("\nnum1 points to:",id(num1))
print("num2 points to:", id(num2))

num2 = 22

print("After num2 is updated:")
print("num1 =",num1)
print("num2 =",num2)

print("\nnum1 points to:",id(num1))
print("num2 points to:", id(num2))

dict1 = {
    'Value': 11
}

dict2 = dict1

print("Before value is updated:")
print("dict1 =",dict1)
print("dict2 =",dict2)

print("\ndict1 points to",id(dict1))
print("dict2 points to",id(dict2))

dict2['Value'] = 22

print("\nAfter value is updated:")
print("dict1 =",dict1)
print("dict2 =",dict2)

print("\ndict1 points to",id(dict1))
print("dict2 points to",id(dict2))