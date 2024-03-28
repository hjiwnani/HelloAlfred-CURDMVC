def recover_original_string(shifted_string):
    original_chars = []
    for char in shifted_string:
        ascii_value = ord(char) - 1
        original_char = chr(ascii_value)
        original_chars.append(original_char)
    return ''.join(original_chars)

def reverse_string(input_string):
    return input_string[::-1]
    
def reverse_modified_string_to_original(modified_string):
    original_string = ""
    for i, char in enumerate(modified_string):
        if i % 2 == 0:
            original_char = chr(ord(char) + 3)
        else:
            original_char = chr(ord(char) + 2)
        original_string += original_char
    
    return original_string

def decode_password(input_str: str) -> str:
    input_str = recover_original_string(input_str)
    input_str = reverse_string(input_str)
    input_str = reverse_modified_string_to_original(input_str)
    input_str = input_str.swapcase()
    return input_str