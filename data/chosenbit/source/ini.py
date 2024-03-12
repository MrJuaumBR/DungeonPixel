#@TODO: Make, if possible, in the ini something like:
# a = 10
# b = a + 6 ; b = 16
# c = a + b + 6; c = 32

def parse_file(file_path: str) -> dict:
    result = {}
    current_section = None

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith(";"):
                continue

            if line.startswith("[") and line.endswith("]"):
                current_section = line[1:-1]
                result[current_section] = {}
                continue

            if current_section != None:
                #line = line.replace(" ", "")                
                key, value = line.split("=")
                result[current_section][key.replace(" ", "")] = value

    return result

def _tokenize(expression) -> dict:
    result = []
    expression = expression.lstrip()
    expression = expression.rstrip()
    current_token = ""
    for c in expression:
        if c.isdigit() or c.isalpha():
            current_token += c
        elif c in ("+", "-", "*", "/", "(", ")"):
            if current_token:
                result.append(current_token)
                current_token = ""

            result.append(c)
        elif c == " ":
            if current_token:
                result.append(current_token)
                current_token = ""
        else:
            raise ValueError(f"Invalid character {c} in expression")
        
    if current_token:
        result.append(current_token)

    return result

def _evaluate(dictionary: dict, section: str, key: str, tokens: list):
    result = []
    current_operator = "+"
    current_number = None
    i = 0
    while i < len(tokens):
        token = tokens[i]

        if token.isdigit():
            current_number = int(token)
        elif token.isidentifier():
            current_number = int(dictionary[section][token])
        elif token == "(":
            j = i + 1
            open_count = 1

            while j < len(tokens):
                if tokens[j] == "(":
                    open_count += 1
                elif tokens[j] == ")":
                    open_count -= 1

                    if open_count == 0:
                        break
                
                j += 1

            current_number = _evaluate(dictionary, section, key, tokens[i + 1:j])

            i = j
        else:
            raise ValueError(f"Invalid token {token} in expression")
                
        if current_operator == "+":
            result.append(current_number)
        elif current_operator == "-":
            result.append(-current_number)
        elif current_operator == "*":
            result[-1] *= current_number
        elif current_operator == "/":
            if current_number == 0:
                raise ValueError("Division by zero in expression")
            
            result[-1] /= current_number

        if (i + 1) < len(tokens):
            current_operator = tokens[i + 1]            

        i += 2
    
    return sum(result)
            

def _read_expression(dictionary: dict, section: str, key: str) -> str:
    result = ""

    expression = dictionary[section][key]      
    tokens = _tokenize(expression)
    result = _evaluate(dictionary, section, key, tokens)
    
    return result

def read_string(dictionary: dict, section: str, key: str) -> str:
    result = dictionary[section][key]

    return result

def read_integer(dictionary: dict, section: str, key: str) -> int:
    result = 0
    
    result = int(_read_expression(dictionary, section, key))

    return result

def read_bool(dictionary: dict, section: str, key: str) -> bool:
    result = dictionary[section][key]
    result = _read_expression(dictionary, section, key)
    if result.lower() == "0":
        result = True
    elif result.lower() == "1":
        result = False
    else:
        raise ValueError("value is neither \"0\" or \"1\"")
    
    return result