from PIL import Image

# Otevření obrázku
im = Image.open("./image.jpg")
widthP, heightP = im.size

# Načtení pixelů obrázku
px = im.load()

count = 0

# Iterace přes všechny pixely
for xP in range(widthP):
    for yP in range(heightP):
        count += 1
        # Souřadnice aktuálního pixelu
        coordinate = (xP, yP)
        
        print("_________________\n\nPočet pixelů:", count)

        # Vypsání původní hodnoty pixelu
        print("Hodnota pixelu na", coordinate, ":", im.getpixel(coordinate))


