from PIL import Image


def embed_message(image_path, message, output_path):
    image = Image.open(image_path)
    encoded_image = image.copy()
    binary_message = ''.join(format(ord(char), '08b') for char in message) + '11111111'
    width, height = image.size
    data_index = 0

    for y in range(height):
        for x in range(width):
            if data_index < len(binary_message):
                pixel = list(encoded_image.getpixel((x, y)))
                pixel[0] = pixel[0] & ~1 | int(binary_message[data_index])
                data_index += 1
                encoded_image.putpixel((x, y), tuple(pixel))
            else:
                break

    encoded_image.save(output_path)
    return output_path


def extract_message(image_path):
    image = Image.open(image_path)
    binary_message = ''
    width, height = image.size

    for y in range(height):
        for x in range(width):
            pixel = image.getpixel((x, y))
            binary_message += str(pixel[0] & 1)

    chars = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    message = ''.join(chr(int(char, 2)) for char in chars)
    return message.split(chr(255))[0]  # Stop at the end marker
