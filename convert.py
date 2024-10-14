from PIL import Image

def ConvertImageToBin(file):
    output = []
    # Otevření obrázku
    im = Image.open("./image.jpg").convert('RGBA')
    widthP, heightP = im.size

    # Načtení pixelů obrázku
    px = im.load()

    threshold = 40  # Práh pro rozhodnutí mezi 0 a 1

    # Otevření souboru pro zápis binárních hodnot
    with open("output.txt", "w") as file:
        # Iterace přes všechny pixely
        for xP in range(widthP):
            for yP in range(heightP):
                # Načtení RGBA hodnoty pixelu
                r, g, b, a = px[xP, yP]
                
                # Spočítání průměrné hodnoty z RGB (luminance)
                average_intensity = (r + g + b) / 3
                
                # Převod na binární hodnotu (0 nebo 1) podle prahu
                if average_intensity >= threshold:
                    binary_value = 1  # světlý pixel
                else:
                    binary_value = 0  # tmavý pixel
                
                output.append(binary_value)
                # Zapsání binární hodnoty do souboru
                file.write(f"Pixel ({xP}, {yP}) má binární hodnotu: {binary_value}\n")
        return output
