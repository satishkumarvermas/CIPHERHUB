def process(text, action):
    if action == 'encrypt':
        return encrypt(text)
    elif action == 'decrypt':
        return decrypt(text)

def encrypt(text):
    return 'encrypted_' + text

def decrypt(text):
    return text.replace('encrypted_', '')