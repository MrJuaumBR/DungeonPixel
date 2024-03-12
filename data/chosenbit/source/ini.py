#@TODO: Make, if possible, in the ini something like:
# a = 10
# b = a + 6 ; b = 16
# c = a + b + 6; c = 32

def parse_ini(file_path: str) -> dict:
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
                line = line.replace(" ", "")                
                key, value = line.split("=")
                result[current_section][key] = value

    return result

def read_string(dictionary: dict, section: str, key: str) -> str:
    result = dictionary[section][key]

    return result

def read_integer(dictionary: dict, section: str, key: str) -> int:
    result = int(dictionary[section][key])

    return result

def read_bool(dictionary: dict, section: str, key: str) -> bool:
    result = dictionary[section][key]

    if result.lower() == "true":
        result = True
    elif result.lower() == "false":
        result = False
    else:
        raise ValueError("value is neither \"true\" or \"false\"")
    
    return result