from PIL import Image, ImageDraw, ImageFont

def draw_annotations(input_path, output_path, annotations, prints=True):
    try:
        if not annotations:
            if prints: print("[X] No annotations")
            return False

        if prints: print(f"[✓] Drawing annotations...")

        # --- Determine image size ---
        if input_path:
            # Open original image
            img = Image.open(input_path).convert("RGB")
            if prints: print(f"[✓] Loaded image: {input_path}")
        else:
            # Create blank image large enough to fit all annotations
            max_x = max(ann['pixelx'] for ann in annotations)
            max_y = max(ann['pixely'] for ann in annotations)
            padding = 50  # extra space around

            width = int(max_x + padding)
            height = int(max_y + padding)

            img = Image.new("RGB", (width, height), color="black")
            if prints: print(f"[✓] Created blank image: {width}x{height}")

        # --- Draw ---
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype("arial.ttf", size=16)
        except:
            font = ImageFont.load_default()

        for ann in annotations:
            x = ann['pixelx']
            y = ann['pixely']
            names = ', '.join(ann['names'])

            r = 10  # circle radius

            # Draw circle
            draw.ellipse((x - r, y - r, x + r, y + r), outline='red', width=2)

            # Draw text
            draw.text((x + r + 2, y - r), names, fill='yellow', font=font)

        # --- Save ---
        img.save(output_path)
        if prints: print(f"[✓] Saved annotated image as: {output_path}")
        if prints: print("[✓] Done.")

        return True

    except Exception as e:
        if prints: print("[X] Fatal error!\n", e)
        return False
