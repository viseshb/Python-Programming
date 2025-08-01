class Cookie:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color


cookie_one = Cookie("Yellow")
cookie_two = Cookie("Green")

print("Cookie one color is", cookie_one.get_color())
print("Cookie two color is", cookie_two.get_color())

cookie_one.set_color("Black")

print("Cookie one color is now changed to", cookie_one.get_color())
print("Cookie two color is now",cookie_two.get_color())


class Books:
    def __init__(self, name):
        self.name = name

    def get_bookName(self):
        return self.name

    def set_bookName(self, name):
        self.name = name


book_one_name = Books("Harry Potter")
book_two_name = Books("Tintin")

print("Book one name is", book_one_name.get_bookName())
print("Book two name is", book_two_name.get_bookName())

book_two_name.set_bookName("Tintin 2")

print("Book one name is", book_one_name.get_bookName())
print("Book two name is", book_two_name.get_bookName())

            
