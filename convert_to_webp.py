#!/usr/bin/env python3
"""
Image Converter to WebP
Converts all images in the directory to WebP format for better performance
"""

import os
import sys
from PIL import Image
import glob

def convert_to_webp(input_path, output_path=None, quality=85):
    """
    Convert an image to WebP format

    Args:
        input_path (str): Path to input image
        output_path (str): Path for output WebP image (optional)
        quality (int): Quality for WebP compression (0-100)
    """
    try:
        # Open the image
        with Image.open(input_path) as img:
            # Convert to RGB if necessary (for PNG with transparency)
            if img.mode in ('RGBA', 'LA', 'P'):
                # Create white background for transparent images
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'RGBA':
                    background.paste(img, mask=img.split()[-1])  # Use alpha channel as mask
                else:
                    background.paste(img)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')

            # Generate output path if not provided
            if output_path is None:
                base_name = os.path.splitext(input_path)[0]
                output_path = base_name + '.webp'

            # Save as WebP
            img.save(output_path, 'WEBP', quality=quality, method=6)
            print(f"Converted: {input_path} -> {output_path}")

            # Remove original file
            os.remove(input_path)
            print(f"Removed original: {input_path}")

    except Exception as e:
        print(f"Error converting {input_path}: {e}")

def main():
    """
    Main function to convert all images in current directory and subdirectories
    """
    # Supported formats to convert
    supported_formats = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff', '*.tif']

    # Get current directory
    current_dir = os.getcwd()

    print(f"Converting images to WebP in: {current_dir}")
    print("=" * 50)

    converted_count = 0

    # Find and convert all images
    for format_pattern in supported_formats:
        for image_path in glob.glob(os.path.join(current_dir, '**', format_pattern), recursive=True):
            # Skip if it's already a webp file
            if image_path.lower().endswith('.webp'):
                continue

            # Skip images in node_modules, .git, etc.
            if any(skip_dir in image_path for skip_dir in ['node_modules', '.git', '__pycache__', 'ThetaTau copy']):
                continue

            convert_to_webp(image_path)
            converted_count += 1

    print("=" * 50)
    print(f"Conversion complete! Converted {converted_count} images to WebP format.")

if __name__ == "__main__":
    main()
