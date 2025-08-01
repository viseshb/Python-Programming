def functionThree():
    print("Three")

def functionTwo():
    functionThree()
    print("Two")

def functionOne():
    functionTwo()
    print("One")

functionOne()        