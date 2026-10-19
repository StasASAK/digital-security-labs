
import string

ALPHABET = string.ascii_lowercase
NAME = "Stanislav"
SURNAME = "Kudelenko"
BIRTH_DATE = "19.10"
MESSAGE = "Information security is very important"


def generate_caesar_key(date):
    return sum(int(char) for char in date if char.isdigit()) % 26


def generate_vigenere_key(surname):
    return "".join(char.upper() for char in surname if char.isalpha())


def caesar_encrypt(text, shift):
    result = ""

    for char in text:
        if char.lower() in ALPHABET:
            index = ALPHABET.index(char.lower())
            new_index = (index + shift) % 26
            new_char = ALPHABET[new_index]

            if char.isupper():
                new_char = new_char.upper()

            result += new_char
        else:
            result += char

    return result


def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)


def vigenere_encrypt(text, key):
    result = ""
    key = key.lower()
    key_index = 0

    for char in text:
        if char.lower() in ALPHABET:
            shift = ALPHABET.index(key[key_index % len(key)])
            index = ALPHABET.index(char.lower())
            new_char = ALPHABET[(index + shift) % 26]

            if char.isupper():
                new_char = new_char.upper()

            result += new_char
            key_index += 1
        else:
            result += char

    return result


def vigenere_decrypt(text, key):
    result = ""
    key = key.lower()
    key_index = 0

    for char in text:
        if char.lower() in ALPHABET:
            shift = ALPHABET.index(key[key_index % len(key)])
            index = ALPHABET.index(char.lower())
            new_char = ALPHABET[(index - shift) % 26]

            if char.isupper():
                new_char = new_char.upper()

            result += new_char
            key_index += 1
        else:
            result += char

    return result


def atbash_cipher(text):
    result = ""

    for char in text:
        if char.lower() in ALPHABET:
            index = ALPHABET.index(char.lower())
            new_char = ALPHABET[25 - index]

            if char.isupper():
                new_char = new_char.upper()

            result += new_char
        else:
            result += char

    return result


def caesar_brute_force(text):
    print("\n=== CAESAR BRUTE FORCE ===")

    for shift in range(1, 26):
        decrypted = caesar_decrypt(text, shift)
        print(f"Shift {shift:2}: {decrypted}")


def compare_ciphers(text, caesar_key, vigenere_key):
    caesar_result = caesar_encrypt(text, caesar_key)
    vigenere_result = vigenere_encrypt(text, vigenere_key)
    atbash_result = atbash_cipher(text)

    print("\n=== CIPHER COMPARISON ===")
    print(f"{'Algorithm':<12} {'Length':<10} {'Key':<15} {'Key complexity'}")
    print("-" * 60)
    print(f"{'Caesar':<12} {len(caesar_result):<10} {caesar_key!s:<15} Low")
    print(f"{'Vigenere':<12} {len(vigenere_result):<10} {vigenere_key:<15} Medium")
    print(f"{'Atbash':<12} {len(atbash_result):<10} {'None':<15} None")

    print("\n=== ENCRYPTED RESULTS ===")
    print("Caesar:  ", caesar_result)
    print("Vigenere:", vigenere_result)
    print("Atbash:  ", atbash_result)

    print("\n=== ANALYSIS ===")
    print("Caesar uses a fixed shift and is easy to break.")
    print("Vigenere uses a repeating key and is harder to analyze.")
    print("Atbash uses a reversed alphabet and has no secret key.")
    print("None of these classical ciphers is secure for modern communication.")


def main():
    caesar_key = generate_caesar_key(BIRTH_DATE)
    vigenere_key = generate_vigenere_key(SURNAME)

    print("=== PERSONAL MESSAGE PROTECTION ===")
    print("Student:", NAME, SURNAME)
    print("Group: 6.04.122.010.23.1")
    print("Date:", BIRTH_DATE)
    print("Caesar key:", caesar_key)
    print("Vigenere key:", vigenere_key)

    while True:
        print("\n========== MAIN MENU ==========")
        print("1. Caesar cipher")
        print("2. Vigenere cipher")
        print("3. Atbash cipher")
        print("4. Caesar brute force")
        print("5. Compare algorithms")
        print("6. Full demonstration")
        print("0. Exit")

        choice = input("\nSelect an option: ")

        if choice == "0":
            print("Program finished.")
            break

        elif choice == "1":
            text = input("Enter text: ")
            encrypted = caesar_encrypt(text, caesar_key)
            decrypted = caesar_decrypt(encrypted, caesar_key)

            print("\n=== CAESAR CIPHER ===")
            print("Shift:", caesar_key)
            print("Original:", text)
            print("Encrypted:", encrypted)
            print("Decrypted:", decrypted)

        elif choice == "2":
            text = input("Enter text: ")
            encrypted = vigenere_encrypt(text, vigenere_key)
            decrypted = vigenere_decrypt(encrypted, vigenere_key)

            print("\n=== VIGENERE CIPHER ===")
            print("Key:", vigenere_key)
            print("Original:", text)
            print("Encrypted:", encrypted)
            print("Decrypted:", decrypted)

        elif choice == "3":
            text = input("Enter text: ")
            encrypted = atbash_cipher(text)
            decrypted = atbash_cipher(encrypted)

            print("\n=== ATBASH CIPHER ===")
            print("Original:", text)
            print("Encrypted:", encrypted)
            print("Decrypted:", decrypted)

        elif choice == "4":
            text = input("Enter encrypted text: ")
            caesar_brute_force(text)

        elif choice == "5":
            compare_ciphers(MESSAGE, caesar_key, vigenere_key)

        elif choice == "6":
            print("\n=== FULL DEMONSTRATION ===")
            print("Original message:", MESSAGE)

            caesar_result = caesar_encrypt(MESSAGE, caesar_key)
            vigenere_result = vigenere_encrypt(MESSAGE, vigenere_key)
            atbash_result = atbash_cipher(MESSAGE)

            print("\nCaesar encrypted:", caesar_result)
            print("Caesar decrypted:", caesar_decrypt(caesar_result, caesar_key))

            print("\nVigenere encrypted:", vigenere_result)
            print("Vigenere decrypted:", vigenere_decrypt(vigenere_result, vigenere_key))

            print("\nAtbash encrypted:", atbash_result)
            print("Atbash decrypted:", atbash_cipher(atbash_result))

            compare_ciphers(MESSAGE, caesar_key, vigenere_key)

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()

