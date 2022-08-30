class CalculationError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class string_calculate:
    def __init__(self, text: str):
        self.text = text
        self.text = self.text.replace("\n", " ")
        self.text = self.text.replace(" ", "")
        operators = ["+", "-", "*", "/", "(", ")"]
        for operator in operators:
            self.text = self.text.replace(operator, " " + operator + " ")

        self.text_list = self.text.split(" ")
        for item in self.text_list:
            if item == "+" or item == "-" or item == "*" or item == "/" or item == "" or item == "(" or item == ")":
                pass
            else:
                try:
                    float(item)
                    pass
                except ValueError:
                    raise CalculationError(
                        f"Error convering to equation '{item}' is not a number or one of the following opperators +, -, *, /, (, ) or a number.\n\n The equation was:\t '{self.text}'"
                    )
                except Exception as e:
                    raise CalculationError(e)
        self.text = self.text.replace(" ", "")
        self.value = eval(self.text)
