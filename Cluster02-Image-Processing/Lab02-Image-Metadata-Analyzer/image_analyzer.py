"""
Image Analyzer
Multimedia Systems Lab

Analyzes an image and displays:
- File name
- File size
- File format
- Width and height
- Resolution
- Color mode
- EXIF metadata

Supported formats:
JPG, JPEG, PNG, TIFF, WEBP, BMP
"""

import os
import sys
from PIL import Image, ExifTags


SUPPORTED_FORMATS = {
    ".jpg", ".jpeg", ".png",
    ".tif", ".tiff",
    ".webp", ".bmp"
}


def format_file_size(size):
    """Convert bytes into a readable file size."""
    if size < 1024:
        return f"{size} Bytes"
    elif size < 1024 * 1024:
        return f"{size / 1024:.2f} KB"
    else:
        return f"{size / (1024 * 1024):.2f} MB"


def get_exif_data(image):
    """Extract EXIF metadata from the image."""
    exif_data = {}

    try:
        exif = image.getexif()

        for tag_id, value in exif.items():
            tag_name = ExifTags.TAGS.get(tag_id, tag_id)

            if isinstance(value, bytes):
                value = value.decode(errors="replace")

            exif_data[tag_name] = value

    except Exception:
        pass

    return exif_data


def get_camera(exif):
    """Get camera manufacturer and model."""
    make = exif.get("Make", "")
    model = exif.get("Model", "")

    if make and model:
        return f"{make} {model}"
    elif model:
        return str(model)
    elif make:
        return str(make)

    return "Not Available"


def get_date_taken(exif):
    """Get the image capture date."""
    return (
        exif.get("DateTimeOriginal")
        or exif.get("DateTimeDigitized")
        or exif.get("DateTime")
        or "Not Available"
    )


def get_orientation(exif):
    """Convert EXIF orientation value into readable text."""
    orientation = exif.get("Orientation")

    orientation_map = {
        1: "Normal",
        2: "Mirrored Horizontally",
        3: "Rotated 180°",
        4: "Mirrored Vertically",
        5: "Mirrored + Rotated 270°",
        6: "Rotated 90° Clockwise",
        7: "Mirrored + Rotated 90°",
        8: "Rotated 270° Clockwise"
    }

    return orientation_map.get(
        orientation,
        "Not Available"
    )


def analyze_image(image_path):
    """Analyze and display image metadata."""

    # Check whether the file exists
    if not os.path.isfile(image_path):
        print(f"\nError: File not found.")
        print(f"Path: {image_path}")
        return

    # Check file extension
    extension = os.path.splitext(image_path)[1].lower()

    if extension not in SUPPORTED_FORMATS:
        print(f"\nError: Unsupported format '{extension}'.")
        print("Supported formats: JPG, JPEG, PNG, TIFF, WEBP, BMP")
        return

    try:
        with Image.open(image_path) as image:

            file_name = os.path.basename(image_path)
            file_size = os.path.getsize(image_path)
            file_format = image.format or "Unknown"

            width, height = image.size
            color_mode = image.mode

            # Extract resolution
            dpi = image.info.get("dpi")

            if dpi:
                resolution = f"{dpi[0]:.2f} x {dpi[1]:.2f} DPI"
            else:
                resolution = "Not Available"

            # Extract EXIF metadata
            exif = get_exif_data(image)

            # Display report
            print("\n" + "=" * 40)
            print("IMAGE METADATA REPORT")
            print("=" * 40)

            print(f"\n{'File Name':<18}: {file_name}")
            print(f"{'File Size':<18}: {format_file_size(file_size)}")
            print(f"{'File Format':<18}: {file_format}")
            print(f"{'Width':<18}: {width} pixels")
            print(f"{'Height':<18}: {height} pixels")
            print(f"{'Resolution':<18}: {resolution}")
            print(f"{'Color Mode':<18}: {color_mode}")

            print("\nEXIF Metadata")
            print("-" * 40)

            print(f"{'Camera':<18}: {get_camera(exif)}")
            print(f"{'Date Taken':<18}: {get_date_taken(exif)}")
            print(f"{'Orientation':<18}: {get_orientation(exif)}")

            # Additional metadata
            extra_tags = {
                "LensModel": "Lens",
                "FNumber": "F-Number",
                "ExposureTime": "Exposure Time",
                "ISOSpeedRatings": "ISO",
                "FocalLength": "Focal Length",
                "Software": "Software"
            }

            for tag, label in extra_tags.items():
                if tag in exif:
                    print(f"{label:<18}: {exif[tag]}")

            print("\n" + "=" * 40)

    except Exception as error:
        print("\nError: Unable to analyze the image.")
        print(f"Details: {error}")


def main():
    """Main program."""

    if len(sys.argv) != 2:
        print("\nUsage:")
        print("python image_analyzer.py <image_path>")
        print("\nExample:")
        print("python image_analyzer.py ../input/sample.jpg")
        return

    analyze_image(sys.argv[1])


if __name__ == "__main__":
    main()