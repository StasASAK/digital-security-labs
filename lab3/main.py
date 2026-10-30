
from PIL import Image
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MAGIC = b"LSB3"


def hide_message(image_path, message, output_path):
    image = Image.open(image_path).convert("RGB")
    data = MAGIC + message.encode("utf-8")
    payload = len(data).to_bytes(4, "big") + data
    bits = "".join(f"{byte:08b}" for byte in payload)

    if len(bits) > image.width * image.height * 3:
        raise ValueError("Message is too large for this image")

    pixels = list(image.getdata())
    result = []
    bit_index = 0

    for pixel in pixels:
        channels = list(pixel)

        for i in range(3):
            if bit_index < len(bits):
                channels[i] = (channels[i] & 254) | int(bits[bit_index])
                bit_index += 1

        result.append(tuple(channels))

    image.putdata(result)
    image.save(output_path, format="PNG")
    print(f"Message hidden in: {output_path}")


def extract_message(image_path):
    image = Image.open(image_path).convert("RGB")
    bits = []

    for pixel in image.getdata():
        for channel in pixel:
            bits.append(str(channel & 1))

    if len(bits) < 32:
        raise ValueError("Image is too small")

    length = int("".join(bits[:32]), 2)

    if length < len(MAGIC) or (32 + length * 8) > len(bits):
        raise ValueError("No valid hidden message found")

    data = bytes(
        int("".join(bits[i:i + 8]), 2)
        for i in range(32, 32 + length * 8, 8)
    )

    if not data.startswith(MAGIC):
        raise ValueError("No valid hidden message found")

    return data[len(MAGIC):].decode("utf-8")


def compare_images(original_path, modified_path):
    original = Image.open(original_path).convert("RGB")
    modified = Image.open(modified_path).convert("RGB")

    if original.size != modified.size:
        print("Image dimensions are different")
        return

    changed_pixels = 0
    changed_channels = [0, 0, 0]
    total_difference = [0, 0, 0]

    for a, b in zip(original.getdata(), modified.getdata()):
        if a != b:
            changed_pixels += 1

        for i in range(3):
            if a[i] != b[i]:
                changed_channels[i] += 1
                total_difference[i] += abs(a[i] - b[i])

    total_pixels = original.width * original.height

    print(f"Dimensions: {original.width} x {original.height}")
    print(f"Total pixels: {total_pixels}")
    print(f"Changed pixels: {changed_pixels}")
    print(f"Changed pixels (%): {changed_pixels / total_pixels * 100:.4f}")
    print(f"Changed R channels: {changed_channels[0]}")
    print(f"Changed G channels: {changed_channels[1]}")
    print(f"Changed B channels: {changed_channels[2]}")
    print(f"Total RGB differences: {total_difference}")
    print(f"Original file size: {Path(original_path).stat().st_size} bytes")
    print(f"Modified file size: {Path(modified_path).stat().st_size} bytes")


def show_lsb_planes(image_path):
    image = Image.open(image_path).convert("RGB")

    for channel_index, name in enumerate(["Red", "Green", "Blue"]):
        plane = Image.new("L", image.size)
        plane.putdata([
            255 if pixel[channel_index] & 1 else 0
            for pixel in image.getdata()
        ])
        output = BASE_DIR / f"lsb_{name.lower()}.png"
        plane.save(output)
        print(f"Saved: {output}")


def save_histograms(image_path):
    image = Image.open(image_path).convert("RGB")
    histogram = image.histogram()

    for index, name in enumerate(["red", "green", "blue"]):
        values = histogram[index * 256:(index + 1) * 256]
        output = BASE_DIR / f"histogram_{name}.csv"

        with open(output, "w", encoding="utf-8") as file:
            file.write("Value,Count\n")
            for value, count in enumerate(values):
                file.write(f"{value},{count}\n")

        print(f"Saved histogram data: {output}")


def main():
    original = BASE_DIR / "original.jpg"
    personal = BASE_DIR / "personal_data.png"
    generated = BASE_DIR / "my_stego.png"

    while True:
        print("\n=== LSB STEGANOGRAPHY LAB 3 ===")
        print("1. Hide message")
        print("2. Extract message")
        print("3. Compare original and personal_data.png")
        print("4. Compare original and my_stego.png")
        print("5. Save LSB bit planes")
        print("6. Export RGB histograms")
        print("0. Exit")

        choice = input("Choose option: ").strip()

        try:
            if choice == "1":
                message = input("Enter message: ")
                hide_message(original, message, generated)

            elif choice == "2":
                filename = input("Enter image filename [my_stego.png]: ").strip()
                path = BASE_DIR / (filename or "my_stego.png")
                print("Extracted message:", extract_message(path))

            elif choice == "3":
                compare_images(original, personal)

            elif choice == "4":
                compare_images(original, generated)

            elif choice == "5":
                filename = input("Enter image filename [my_stego.png]: ").strip()
                path = BASE_DIR / (filename or "my_stego.png")
                show_lsb_planes(path)

            elif choice == "6":
                filename = input("Enter image filename [my_stego.png]: ").strip()
                path = BASE_DIR / (filename or "my_stego.png")
                save_histograms(path)

            elif choice == "0":
                break

            else:
                print("Invalid option")

        except Exception as error:
            print("Error:", error)


if __name__ == "__main__":
    main()

