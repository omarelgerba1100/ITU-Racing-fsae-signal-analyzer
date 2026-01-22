#!/usr/bin/env python3
"""
ITU Racing - FSAE Signal Analyzer Icon Generator

Creates a simple racing-themed icon for the application.
Generates icon.ico in the assets folder.

Requirements:
    pip install Pillow

Usage:
    python create_icon.py
"""

import os
import sys

def check_pillow():
    """Check if Pillow is installed."""
    try:
        from PIL import Image, ImageDraw, ImageFont
        return True
    except ImportError:
        print("[!] Pillow not found. Installing...")
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'Pillow'])
        return True

def create_icon():
    """Create a racing-themed FSAE icon."""
    from PIL import Image, ImageDraw, ImageFont

    # Ensure assets directory exists
    os.makedirs('assets', exist_ok=True)

    # Icon sizes for .ico file (Windows standard sizes)
    sizes = [16, 32, 48, 64, 128, 256]

    images = []

    for size in sizes:
        # Create a new image with transparent background
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Colors - ITU Racing blue theme
        bg_color = (0, 82, 147)        # Dark blue
        accent_color = (0, 150, 255)   # Light blue
        text_color = (255, 255, 255)   # White

        # Draw rounded rectangle background
        padding = max(1, size // 16)
        draw.rounded_rectangle(
            [padding, padding, size - padding - 1, size - padding - 1],
            radius=max(2, size // 8),
            fill=bg_color
        )

        # Draw a stylized signal wave (sine wave pattern)
        wave_y_center = size // 2
        wave_amplitude = size // 6
        wave_start = size // 5
        wave_end = size - size // 5

        # Draw multiple wave lines for signal effect
        for offset in [-2, 0, 2]:
            points = []
            import math
            for x in range(wave_start, wave_end + 1):
                progress = (x - wave_start) / (wave_end - wave_start)
                y = wave_y_center + offset * (size // 20) + int(
                    wave_amplitude * math.sin(progress * 4 * math.pi)
                )
                points.append((x, y))

            if len(points) > 1:
                line_width = max(1, size // 32)
                draw.line(points, fill=accent_color, width=line_width)

        # Draw "FSAE" text at bottom (only for larger sizes)
        if size >= 48:
            try:
                # Try to use a system font
                font_size = max(8, size // 6)
                try:
                    font = ImageFont.truetype("arial.ttf", font_size)
                except:
                    try:
                        font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", font_size)
                    except:
                        font = ImageFont.load_default()

                text = "FSAE"
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                text_x = (size - text_width) // 2
                text_y = size - text_height - size // 6

                draw.text((text_x, text_y), text, fill=text_color, font=font)
            except Exception as e:
                # If text rendering fails, skip it
                pass

        images.append(img)

    # Save as .ico file with multiple sizes
    icon_path = os.path.join('assets', 'icon.ico')

    # The first image is the main one, save with all sizes
    images[-1].save(
        icon_path,
        format='ICO',
        sizes=[(s, s) for s in sizes],
        append_images=images[:-1]
    )

    print(f"[OK] Icon created: {os.path.abspath(icon_path)}")
    print(f"     Sizes included: {sizes}")

    # Also save a PNG version for other uses
    png_path = os.path.join('assets', 'icon.png')
    images[-1].save(png_path, format='PNG')
    print(f"[OK] PNG version: {os.path.abspath(png_path)}")

    return icon_path

def main():
    print("\n" + "="*50)
    print("  ITU Racing - FSAE Icon Generator")
    print("="*50 + "\n")

    check_pillow()
    icon_path = create_icon()

    print("\n" + "="*50)
    print("  Icon generation complete!")
    print("="*50 + "\n")

    return icon_path

if __name__ == '__main__':
    main()
