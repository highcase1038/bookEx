from PIL import Image, ImageDraw
import os
from django.conf import settings


def create_simple_placeholder():
    """Create a simple placeholder image without relying on system fonts"""
    static_dir = os.path.join(settings.BASE_DIR, 'bookEx', 'static')

    # Ensure the static directory exists
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

    # Create a 200x300 placeholder image (typical book cover proportions)
    img_width = 200
    img_height = 300
    img = Image.new('RGB', (img_width, img_height), color=(240, 240, 240))

    # Draw on the image
    draw = ImageDraw.Draw(img)

    # Draw a border
    draw.rectangle([(0, 0), (img_width - 1, img_height - 1)], outline=(200, 200, 200))

    # Draw "NO IMAGE" text as shapes instead of using fonts
    # Draw "N"
    x1, y1 = img_width // 2 - 40, img_height // 2 - 15
    x2, y2 = x1 + 10, y1 + 30
    draw.line([(x1, y1), (x1, y2)], fill=(100, 100, 100), width=3)
    draw.line([(x1, y1), (x2, y1)], fill=(100, 100, 100), width=3)
    draw.line([(x2, y1), (x2, y2)], fill=(100, 100, 100), width=3)

    # Draw "O"
    x1, y1 = img_width // 2 - 20, img_height // 2 - 15
    x2, y2 = x1 + 20, y1 + 30
    draw.rectangle([(x1, y1), (x2, y2)], outline=(100, 100, 100), width=3)

    # Draw book icon
    icon_margin = 40
    draw.rectangle(
        [(img_width // 2 - 30, img_height // 2 - 50 - icon_margin),
         (img_width // 2 + 30, img_height // 2 - 10 - icon_margin)],
        outline=(150, 150, 150),
        fill=(220, 220, 220)
    )

    # Save the image
    output_path = os.path.join(static_dir, 'placeholder-book.png')
    img.save(output_path)

    return output_path