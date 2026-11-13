
import hashlib
import json
import math
import secrets
from getpass import getpass
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DOCUMENT = BASE_DIR / "document.txt"
PRIVATE_KEY_FILE = BASE_DIR / "private_key.json"
PUBLIC_KEY_FILE = BASE_DIR / "public_key.json"
SIGNATURE_FILE = BASE_DIR / "document.sig"

E = 65537


def is_prime(number):
    if number < 2:
        return False

    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]

    for prime in small_primes:
        if number == prime:
            return True
        if number % prime == 0:
            return False

    d = number - 1
    r = 0

    while d % 2 == 0:
        d //= 2
        r += 1

    for _ in range(20):
        a = secrets.randbelow(number - 3) + 2
        x = pow(a, d, number)

        if x == 1 or x == number - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, number)
            if x == number - 1:
                break
        else:
            return False

    return True


def generate_prime(seed, label):
    counter = 0

    while True:
        data = seed + label + counter.to_bytes(4, "big")
        candidate = int.from_bytes(
            hashlib.sha512(data).digest(), "big"
        )
        candidate |= (1 << 511) | 1

        if is_prime(candidate):
            return candidate

        counter += 1


def generate_keys():
    print("\n=== KEY GENERATION ===")

    name = input("Enter your name: ")
    birth_date = input("Enter your birth date (DDMMYYYY): ")
    secret_word = getpass("Enter a secret word: ")

    personal_data = name + birth_date + secret_word
    seed = hashlib.sha256(personal_data.encode("utf-8")).digest()

    p = generate_prime(seed, b"prime_p")
    q = generate_prime(seed, b"prime_q")

    if p == q:
        print("Error: Identical prime numbers.")
        return

    n = p * q
    phi = (p - 1) * (q - 1)

    if math.gcd(E, phi) != 1:
        print("Error: Invalid RSA parameters.")
        return

    d = pow(E, -1, phi)

    private_key = {"n": n, "d": d}
    public_key = {"n": n, "e": E}

    PRIVATE_KEY_FILE.write_text(
        json.dumps(private_key, indent=4), encoding="utf-8"
    )
    PUBLIC_KEY_FILE.write_text(
        json.dumps(public_key, indent=4), encoding="utf-8"
    )

    print("Private key saved:", PRIVATE_KEY_FILE.name)
    print("Public key saved:", PUBLIC_KEY_FILE.name)
    print("Key pair generated successfully!")


def calculate_hash(file_path):
    return hashlib.sha256(file_path.read_bytes()).hexdigest()


def sign_document():
    print("\n=== DOCUMENT SIGNING ===")

    if not PRIVATE_KEY_FILE.exists() or not DOCUMENT.exists():
        print("Error: Private key or document not found.")
        return

    private_key = json.loads(
        PRIVATE_KEY_FILE.read_text(encoding="utf-8")
    )

    document_hash = calculate_hash(DOCUMENT)
    hash_number = int(document_hash, 16)

    signature = pow(
        hash_number, private_key["d"], private_key["n"]
    )

    SIGNATURE_FILE.write_text(
        str(signature), encoding="utf-8"
    )

    print("Document SHA-256:", document_hash)
    print("Digital signature created successfully!")
    print("Signature saved:", SIGNATURE_FILE.name)


def verify_signature():
    print("\n=== SIGNATURE VERIFICATION ===")

    if not all([
        PUBLIC_KEY_FILE.exists(),
        SIGNATURE_FILE.exists(),
        DOCUMENT.exists()
    ]):
        print("Error: Required files not found.")
        return

    try:
        public_key = json.loads(
            PUBLIC_KEY_FILE.read_text(encoding="utf-8")
        )
        signature = int(
            SIGNATURE_FILE.read_text(encoding="utf-8")
        )

        n = public_key["n"]
        e = public_key["e"]

        if not 0 <= signature < n:
            print("RESULT: SIGNATURE IS INVALID")
            return

        current_hash = calculate_hash(DOCUMENT)
        expected_hash = int(current_hash, 16)
        recovered_hash = pow(signature, e, n)

        print("Current SHA-256:", current_hash)

        if recovered_hash == expected_hash:
            print("RESULT: SIGNATURE IS VALID")
        else:
            print("RESULT: SIGNATURE IS INVALID")

    except (ValueError, KeyError, TypeError, json.JSONDecodeError):
        print("RESULT: SIGNATURE IS INVALID")


def test_document_modification():
    print("\n=== DOCUMENT MODIFICATION TEST ===")

    if not DOCUMENT.exists():
        print("Error: Document not found.")
        return

    original_content = DOCUMENT.read_bytes()

    try:
        with DOCUMENT.open("ab") as file:
            file.write(b"\nUnauthorized modification.")

        print("Document was modified.")
        verify_signature()

    finally:
        DOCUMENT.write_bytes(original_content)
        print("Original document restored.")


def test_signature_forgery():
    print("\n=== SIGNATURE FORGERY TEST ===")

    if not SIGNATURE_FILE.exists():
        print("Error: Signature not found.")
        return

    original_signature = SIGNATURE_FILE.read_bytes()

    try:
        SIGNATURE_FILE.write_text(
            "123456789", encoding="utf-8"
        )

        print("Fake signature created.")
        verify_signature()

    finally:
        SIGNATURE_FILE.write_bytes(original_signature)
        print("Original signature restored.")


def main():
    while True:
        print("\n=== PERSONAL DIGITAL SIGNATURE SYSTEM ===")
        print("1. Generate key pair")
        print("2. Sign document")
        print("3. Verify signature")
        print("4. Test document modification")
        print("5. Test signature forgery")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            generate_keys()
        elif choice == "2":
            sign_document()
        elif choice == "3":
            verify_signature()
        elif choice == "4":
            test_document_modification()
        elif choice == "5":
            test_signature_forgery()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
