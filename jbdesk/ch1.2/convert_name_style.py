import re

def to_snake_case(text):
    text = re.sub(r'([a-z])([A-Z])', r'\1_\2', text)  # camelCase -> snake_case
    text = re.sub(r'[-\s]', '_', text)  # kebab-case, space -> snake_case
    return text.lower()

def to_camel_case(text):
    words = to_snake_case(text).split('_')
    return words[0] + ''.join(word.capitalize() for word in words[1:])

def to_pascal_case(text):
    words = to_snake_case(text).split('_')
    return ''.join(word.capitalize() for word in words)

def to_kebab_case(text):
    return to_snake_case(text).replace('_', '-')

def to_screaming_snake_case(text):
    return to_snake_case(text).upper()

def to_train_case(text):
    return '-'.join(word.capitalize() for word in to_snake_case(text).split('_'))

# 테스트
text_samples = [
    "camelCase",
    "PascalCase",
    "snake_case",
    "SCREAMING_SNAKE_CASE",
    "kebab-case",
    "Train-Case"
]

for text in text_samples:
    print(f"Original: {text}")
    print(f"Snake Case: {to_snake_case(text)}")
    print(f"Camel Case: {to_camel_case(text)}")
    print(f"Pascal Case: {to_pascal_case(text)}")
    print(f"Kebab Case: {to_kebab_case(text)}")
    print(f"Screaming Snake Case: {to_screaming_snake_case(text)}")
    print(f"Train Case: {to_train_case(text)}")
    print("-")
