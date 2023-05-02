from PIL import Image, ImageDraw, ImageFont
import shutil
import os
import subprocess


def ger_char(input):
    return chars_list[int(input*interval)]


chars = " .,-~:;=!*#$@"
chars_list = list(chars)
chars_length = len(chars_list)
interval = chars_length/256

# font = ImageFont.truetype("C:\\Windows\\Fonts\\lucon.ttf")

scale = 0.2
char_width = 10
char_height = char_width*2

input_vid = "input.mp4"
fps = 30


shutil.rmtree("input")
shutil.rmtree("output")
os.mkdir("input")
os.mkdir("output")

print("Converting to images")
subprocess.run(f"ffmpeg -i \"{input_vid}\" -q:a 0 -map a audio.mp3 -r {fps} input/img_%1d.jpg", shell=True)

index = 1
for file in os.listdir("input"):
    print(f"Converting... {index}")

    # open input image
    im = Image.open(f"input/img_{index}.jpg").convert("RGB")

    # resize input image
    width, height = (1080, 720)
    im = im.resize((int(scale*width), int(scale*height*(char_width/char_height))), Image.NEAREST)
    width, height = im.size

    pix = im.load()

    # create output image
    output_image = Image.new("RGB", (char_width*width, char_height*height), color=(0, 0, 0))
    draw = ImageDraw.Draw(output_image)

    for y in range(height):
        for x in range(width):
            r, g, b = pix[x, y]
            h = int(r/3 + g/3 + b/3)
            pix[x, y] = (h, h, h)
            draw.text((x*char_width, y*char_height), ger_char(h), (r/10, g/10, b/10))

    output_image.save(f"output/img_{index}.jpg")

    index += 1

print("Converting to video")
subprocess.run(f"ffmpeg -i audio.mp3 -r {fps} -i output/img_%1d.jpg output.mp4")
print("DONE! (hopefully)")
