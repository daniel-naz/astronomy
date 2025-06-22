# Star Matcher using Astrometry.net

This project allows you to upload an image of the night sky, submit it to [astrometry.net](http://nova.astrometry.net), and receive an annotated image with identified stars. The script also generates a link to Stellarium Web so you can visualize the solved sky position.

---

## Features

- Submit night sky images to astrometry.net  
- Auto-wait for job completion  
- Fetch known stars / object annotations  
- Draw circles and labels on stars in the image  
- Save annotated image to output file  
- Generate Stellarium Web link  
- Simple CLI or interactive mode

---

## Files

| File | Purpose |
| ---- | ------- |
| `main.py` | Main CLI program |
| `astrometry_client.py` | Handles API calls to astrometry.net |
| `draw_utils.py` | Draws annotated stars on the image |
| `temp.png` | Example input image |

---

## How to run

### Option 1 — Command-line

```bash
python main.py -a "YOUR_API_KEY" -f "input_image.jpg" -o "output_image.png"
