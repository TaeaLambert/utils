class CalculationError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class string_calculate:
    def __init__(self, text: str):
        text_list = text.split(" ")
        for item in text_list:
            if item == "+" or item == "-" or item == "*" or item == "/" or item == "" or item == "(" or item == ")":
                pass
            else:
                try:
                    float(item)
                    pass
                except ValueError:
                    raise CalculationError(
                        f"Error convering to equation {item} is not a number or one of the following opperators +, -, *, /, (, )"
                    )
                except Exception as e:
                    raise CalculationError(e)
        text = text.replace(" ", "")
        self.value = eval(text)
