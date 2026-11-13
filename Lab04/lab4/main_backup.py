
import hashlib
import json
import math
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DOCUMENT = BASE_DIR / "document.txt"
PRIVATE_KEY_FILE = BASE_DIR / "private_key.json"
PUBLIC_KEY_FILE = BASE_DIR / "public_key.json"
SIGNATURE_FILE = BASE_DIR / "document.sig"

P = 1000000007
Q = 1000000009
N = P * Q
PHI = (P - 1) * (Q - 1)
E = 65537


def generate_keys():
    print("\n=== KEY GENERATION ===")

    name = input("Enter your name: ")
    birth_date = input("Enter your birth date (DDMMYYYY): ")
    secret_word = input("Enter a secret word: ")

    personal_data = name + birth_date + secret_word
    seed = hashlib.sha256(personal_data.encode("utf-8")).digest()
    seed_number = int.from_bytes(seed, "big")

    if math.gcd(E, PHI) != 1:
        raise ValueError("Invalid RSA parameters")

    base_d = pow(E, -1, PHI)
    d = base_d + (seed_number % 1000) * PHI

    private_key = {"n": N, "d": d}
    public_key = {"n": N, "e": E}

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

    if not PRIVATE_KEY_FILE.exists():
        print("Error: Private key not found.")
        return

    if not DOCUMENT.exists():
        print("Error: Document not found.")
        return

    private_key = json.loads(PRIVATE_KEY_FILE.read_text(encoding="utf-8"))
    document_hash = calculate_hash(DOCUMENT)
    hash_number = int(document_hash, 16)

    signature = pow(hash_number, private_key["d"], private_key["n"])

    SIGNATURE_FILE.write_text(str(signature), encoding="utf-8")

    print("Document SHA-256:", document_hash)
    print("Digital signature created successfully!")
    print("Signature saved:", SIGNATURE_FILE.name)


def verify_signature():
    print("\n=== SIGNATURE VERIFICATION ===")

    if not PUBLIC_KEY_FILE.exists() or not SIGNATURE_FILE.exists():
        print("Error: Public key or signature not found.")
        return

    if not DOCUMENT.exists():
        print("Error: Document not found.")
        return

    public_key = json.loads(PUBLIC_KEY_FILE.read_text(encoding="utf-8"))
    signature = int(SIGNATURE_FILE.read_text(encoding="utf-8"))

    current_hash = calculate_hash(DOCUMENT)
    current_hash_number = int(current_hash, 16)

    recovered_hash = pow(signature, public_key["e"], public_key["n"])

    print("Current SHA-256:", current_hash)

    if recovered_hash == current_hash_number % public_key["n"]:
        print("RESULT: SIGNATURE IS VALID")
    else:
        print("RESULT: SIGNATURE IS INVALID")


def test_document_modification():
    print("\n=== DOCUMENT MODIFICATION TEST ===")

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
        SIGNATURE_FILE.write_text("123456789", encoding="utf-8")
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
