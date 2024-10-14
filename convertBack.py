from PIL import Image

# Otevření souboru pro načtení a ověření rozměrů obrázku
with open("output.txt", "r") as file:
    lines = file.readlines()

# První krok: Určení maximálních hodnot souřadnic
max_x = 0
max_y = 0

# Procházení souřadnic a hledání maximálních hodnot
for line in lines:
    parts = line.strip().split()
    xP = int(parts[1][1:-1])  # Extrahování X souřadnice
    yP = int(parts[2][:-1])   # Extrahování Y souřadnice
    max_x = max(max_x, xP)
    max_y = max(max_y, yP)

# Vytvoření nového obrázku na základě zjištěných rozměrů
widthP = max_x + 1  # Rozměr v ose x
heightP = max_y + 1  # Rozměr v ose y
new_image = Image.new('RGB', (widthP, heightP), color='white')
px = new_image.load()

# Druhý krok: Načtení binárních hodnot a nastavení pixelů
for line in lines:
    parts = line.strip().split()
    xP = int(parts[1][1:-1])  # Extrahování X souřadnice
    yP = int(parts[2][:-1])   # Extrahování Y souřadnice
    binary_value = int(parts[-1])  # Poslední hodnota je binární hodnota (0 nebo 1)

    # Nastavení barvy pixelu podle binární hodnoty
    if binary_value == 1:
        px[xP, yP] = (255, 255, 255)  # Bílá pro hodnotu 1
    else:
        px[xP, yP] = (0, 0, 0)  # Černá pro hodnotu 0

# Uložení nového obrázku
new_image.save("output_image.png")
new_image.show()
