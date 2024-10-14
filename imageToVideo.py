from PIL import Image
import cv2
import numpy as np
from tqdm import tqdm

class imageToVideo:

    def convert(file):
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
    def GenerateVideo(coloursBin:str):

        colors = []

        for i in coloursBin:
            if i == 0:
                colors.append((255,255,255))
            else:
                colors.append((0,0,0))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec pro MP4
        fps = 30
        width, height = 640, 480
        out = cv2.VideoWriter('output.mp4', fourcc, fps, (width, height))

        # Generování snímků
        num_frames = len(colors)
        # Použití tqdm pro progress bar
        for i in tqdm(range(num_frames), desc="Generování snímků", unit="frame"):
            # Vytvoření snímku s barvou ze seznamu (cyklicky)
            color = colors[i % len(colors)]
            frame = np.full((height, width, 3), color, dtype=np.uint8)
            
            # Uložení snímku do videa
            out.write(frame)

        # Uvolnění video writeru
        out.release()
        print("Video bylo úspěšně vytvořeno jako output.mp4.")

    
    def Run(imageFileName):
        colour = imageToVideo.convert(imageFileName)
        imageToVideo.GenerateVideo(colour)

