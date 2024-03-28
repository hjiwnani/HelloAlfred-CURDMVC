import hashlib
import secrets

def shift_string(input_string):
    shifted_chars = []
    for char in input_string:
        ascii_value = ord(char) + 1
        shifted_char = chr(ascii_value)
        shifted_chars.append(shifted_char)
    return ''.join(shifted_chars)

def convert_string_to_modified_string(input_string):
    modified_string = ""
    for i, char in enumerate(input_string):
        if i % 2 == 0:
            modified_char = chr(ord(char) - 3)
        else:
            modified_char = chr(ord(char) - 2)
        modified_string += modified_char

    return modified_string

def reverse_string(input_string):
    return input_string[::-1]


def recover_original_string(shifted_string):
    original_chars = []
    for char in shifted_string:
        ascii_value = ord(char) - 1
        original_char = chr(ascii_value)
        original_chars.append(original_char)
    return ''.join(original_chars)

def custom_salt_and_hash(password):
    salt = secrets.token_bytes(16)  # 16 bytes = 128 bits
    salted_password = salt + password.encode('utf-8')
    hashed_password = hashlib.sha256(salted_password).hexdigest()
    return salt, hashed_password

def Encode_password(pass_):
    pass_ = pass_.swapcase()
    pass_ = convert_string_to_modified_string(pass_)
    pass_ = reverse_string(pass_)
    shifted_string = pass_
    converted_to = shift_string(shifted_string)
    enc = custom_salt_and_hash(converted_to)
    return converted_to,enc

def verify_password(entered_password, stored_salt, stored_hashed_password):
    entered_password,funused = Encode_password(entered_password)
    salted_password = stored_salt + entered_password.encode('utf-8')
    computed_hashed_password = hashlib.sha256(salted_password).hexdigest()
    return computed_hashed_password == stored_hashed_password