import cv2
import numpy as np
from tqdm import tqdm# Seznam barev (ve formátu BGR)
colors = []
def GenerateVideo(colorsBin):

    colors = []

    for i in colorsBin:
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
