# -*- coding: cp1251 -*-
import re
from datetime import datetime


COMMON_WORDS = (
    "password", "qwerty", "admin", "welcome", "letmein",
    "football", "dragon", "monkey", "hello", "love",
    "пароль", "привет", "кохання"
)

TRANSLIT = {
    "а": "a", "б": "b", "в": "v", "г": "h", "ґ": "g",
    "д": "d", "е": "e", "є": "ye", "ж": "zh", "з": "z",
    "и": "y", "і": "i", "ї": "yi", "й": "y", "к": "k",
    "л": "l", "м": "m", "н": "n", "о": "o", "п": "p",
    "р": "r", "с": "s", "т": "t", "у": "u", "ф": "f",
    "х": "kh", "ц": "ts", "ч": "ch", "ш": "sh",
    "щ": "shch", "ь": "", "ъ": "", "ы": "y",
    "э": "e", "ю": "yu", "я": "ya"
}


def transliterate(text):
    return "".join(TRANSLIT.get(char, char) for char in text.lower())


def get_name_variants(name, latin_name):
    variants = set()

    for value in (name, latin_name):
        for part in value.lower().split():
            if len(part) >= 3:
                variants.add(part)
                variants.add(transliterate(part))

    return variants


def analyze_password(password, name, latin_name, birth_date):
    issues = []
    recommendations = []
    lower_password = password.lower()
    length = len(password)

    has_lower = any(char.islower() for char in password)
    has_upper = any(char.isupper() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_special = any(
        not char.isalnum() and not char.isspace()
        for char in password
    )

    # Length contributes up to 6 points.
    if length >= 16:
        score = 6
    elif length >= 12:
        score = 5
    elif length >= 10:
        score = 3
    elif length >= 8:
        score = 2
    else:
        score = 0

    # Character diversity contributes up to 4 points.
    score += sum((has_lower, has_upper, has_digit, has_special))

    if length < 12:
        issues.append("The password is shorter than 12 characters.")
        recommendations.append(
            "Increase the length to at least 12, preferably 16+ characters."
        )

    missing_types = []
    if not has_lower:
        missing_types.append("lowercase letters")
    if not has_upper:
        missing_types.append("uppercase letters")
    if not has_digit:
        missing_types.append("digits")
    if not has_special:
        missing_types.append("special characters")

    if missing_types:
        recommendations.append(
            "For a generated password, include " + ", ".join(missing_types) + "."
        )

    # Match the original name and its Latin spelling.
    name_found = any(
        variant in lower_password
        for variant in get_name_variants(name, latin_name)
    )

    if name_found:
        score -= 3
        issues.append("The password contains your name.")
        recommendations.append("Remove your name from the password.")

    year = birth_date.strftime("%Y")
    day_month = birth_date.strftime("%d%m")
    month_day = birth_date.strftime("%m%d")

    # Detect dates even when separated by dots, dashes or underscores.
    compact_password = re.sub(r"[\W_]+", "", lower_password)

    year_found = year in compact_password
    date_found = any(
        pattern in compact_password
        for pattern in (day_month, month_day)
    )

    if year_found:
        score -= 2
        issues.append("The password contains your birth year.")

    if date_found:
        score -= 2
        issues.append("The password contains your birth day and month.")

    if year_found or date_found:
        recommendations.append(
            "Avoid your birth date and other personal dates."
        )

    word_found = any(word in lower_password for word in COMMON_WORDS)

    if word_found:
        score -= 2
        issues.append("A word from the common-password list was found.")
        recommendations.append(
            "Avoid common passwords and predictable dictionary words."
        )

    sequences = (
        "0123456789",
        "abcdefghijklmnopqrstuvwxyz",
        "qwertyuiop",
        "asdfghjkl",
        "zxcvbnm"
    )

    sequence_found = any(
        sequence[index:index + 4] in lower_password
        or sequence[index:index + 4][::-1] in lower_password
        for sequence in sequences
        for index in range(len(sequence) - 3)
    )

    if sequence_found:
        score -= 2
        issues.append("A predictable sequence of 4+ characters was found.")
        recommendations.append(
            "Avoid sequences such as 1234, abcd or qwerty."
        )

    repeated = re.search(r"(.)\1{2,}", password) is not None

    if repeated:
        score -= 1
        issues.append("The same character is repeated 3 or more times.")
        recommendations.append("Avoid repeated characters such as aaa or 111.")

    score = max(1, min(10, score))

    # Short or personal-data-based passwords cannot receive high scores.
    if length < 8:
        score = min(score, 3)

    if name_found or year_found or date_found:
        score = min(score, 5)

    if score <= 3:
        level = "Weak"
    elif score <= 6:
        level = "Moderate"
    elif score <= 8:
        level = "Good"
    else:
        level = "Strong"

    recommendations.append("Use a unique password for every account.")

    return {
        "score": score,
        "level": level,
        "length": length,
        "lowercase": has_lower,
        "uppercase": has_upper,
        "digits": has_digit,
        "special": has_special,
        "issues": issues,
        "recommendations": recommendations
    }


def print_result(result):
    print("\n" + "=" * 50)
    print("PASSWORD ANALYSIS")
    print("=" * 50)

    print(f"Length: {result['length']}")
    print(f"Lowercase letters: {result['lowercase']}")
    print(f"Uppercase letters: {result['uppercase']}")
    print(f"Digits: {result['digits']}")
    print(f"Special characters: {result['special']}")
    print(f"\nScore: {result['score']}/10")
    print(f"Level: {result['level']}")

    print("\nDetected weaknesses:")
    if result["issues"]:
        for issue in result["issues"]:
            print(f"- {issue}")
    else:
        print("- No weaknesses detected by the implemented checks.")

    print("\nRecommendations:")
    for recommendation in result["recommendations"]:
        print(f"- {recommendation}")

    print("\nThis score is a learning heuristic, not a security guarantee.")
    print("=" * 50)


def main():
    print("PERSONAL PASSWORD SECURITY ANALYZER")
    print("Use invented test passwords, not actual account passwords.")
    print("Input is processed locally and is not saved by this program.\n")

    while True:
        name = input("Enter your first name: ").strip()
        if len(name) >= 3:
            break
        print("Please enter a name with at least 3 characters.")

    latin_name = input(
        "Enter your name in Latin letters or a nickname (optional): "
    ).strip()

    while True:
        date_text = input("Enter your birth date (DD.MM.YYYY): ").strip()

        try:
            birth_date = datetime.strptime(date_text, "%d.%m.%Y").date()

            if birth_date > datetime.now().date():
                print("The birth date cannot be in the future.")
                continue

            break
        except ValueError:
            print("Invalid date. Example format: 15.03.2005")

    while True:
        password = input("\nEnter a TEST password (visible input): ")

        if not password:
            print("The password cannot be empty.")
            continue

        result = analyze_password(
            password, name, latin_name, birth_date
        )
        print_result(result)

        again = input("\nAnalyze another password? (y/n): ").strip().lower()
        if again != "y":
            print("Program finished.")
            break`


if __name__ == "__main__":
    main()
