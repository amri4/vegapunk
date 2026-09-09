from PIL import Image, ImageDraw, ImageFont
from io import BytesIO


def create_poster(
    name,
    bounty,
    avatar_bytes
):
    width = 700
    height = 900

    image = Image.new(
        "RGB",
        (width, height),
        "#e8d3a8"
    )

    draw = ImageDraw.Draw(image)

    title_font = ImageFont.truetype(
        "arial.ttf",
        90
    )

    name_font = ImageFont.truetype(
        "arial.ttf",
        45
    )

    bounty_font = ImageFont.truetype(
        "arial.ttf",
        50
    )

    small_font = ImageFont.truetype(
        "arial.ttf",
        32
    )

    draw.text(
        (width // 2, 30),
        "WANTED",
        font=title_font,
        anchor="ma",
        fill="black"
    )

    avatar = Image.open(
        BytesIO(avatar_bytes)
    ).convert("RGB")

    avatar.thumbnail(
        (400, 400)
    )

    x = (width - avatar.width) // 2

    image.paste(
        avatar,
        (x, 170)
    )

    draw.text(
        (width // 2, 610),
        name.upper(),
        font=name_font,
        anchor="ma",
        fill="black"
    )

    draw.text(
        (width // 2, 675),
        "DEAD OR ALIVE",
        font=small_font,
        anchor="ma",
        fill="black"
    )

    draw.text(
        (width // 2, 745),
        f"฿ {bounty:,}",
        font=bounty_font,
        anchor="ma",
        fill="black"
    )

    output = BytesIO()

    image.save(
        output,
        format="PNG"
    )

    output.seek(0)

    return output