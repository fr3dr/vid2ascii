from PIL import Image, ImageDraw
import shutil
import os
import subprocess


INPUT_DIR = "input"
OUTPUT_DIR = "output"


def ger_char(input):
    return chars_list[int(input*interval)]


input_vid = "input.mp4"
fps = 30

chars = " .'`^\",:;Il!i><~+_-?][}{1)(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
chars_list = list(chars)
chars_length = len(chars_list)
interval = chars_length/256

scale = 0.2
# change this to change spacing of characters
char_width = 6
char_height = char_width*2

if os.path.exists(INPUT_DIR):
    shutil.rmtree(INPUT_DIR)
if os.path.exists(OUTPUT_DIR):
    shutil.rmtree(OUTPUT_DIR)
os.mkdir(INPUT_DIR)
os.mkdir(OUTPUT_DIR)

print("Converting to images")
subprocess.run(f"ffmpeg -i \"{input_vid}\" -q:a 0 -map a audio.mp3 -r {fps} input/img_%1d.jpg", shell=True)

# TODO: estimate the time it takes converting to ascii using this
# get number of files in input directory
file_count = 0
for entry in os.listdir(INPUT_DIR):
    file_count += 1

# convert each image in input directory to ascii
index = 1
for file in os.listdir(INPUT_DIR):
    print(f"Converting to ascii... {index}/{file_count}")

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
            draw.text((x*char_width, y*char_height), ger_char(h), (r, g, b))

    output_image.save(f"output/img_{index}.jpg")

    index += 1

print("Converting to video")
subprocess.run(f"ffmpeg -i audio.mp3 -r {fps} -i output/img_%1d.jpg output.mp4", shell=True)
print("DONE! (hopefully)")
