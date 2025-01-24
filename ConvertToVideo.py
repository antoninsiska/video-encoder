from PIL import Image
import cv2
import numpy as np
from multiprocessing import Process, Queue, current_process  # Přidáno current_process
from tqdm import tqdm
import os

class imageToVideo:

    @staticmethod
    def convert(file):
        output = []
        # Otevření obrázku
        im = Image.open(file).convert('RGBA')
        widthP, heightP = im.size

        # Načtení pixelů obrázku
        px = im.load()

        threshold = 40  # Práh pro rozhodnutí mezi 0 a 1

        # Iterace přes všechny pixely
        for xP in range(widthP):
            for yP in range(heightP):
                # Načtení RGBA hodnoty pixelu
                r, g, b, a = px[xP, yP]
                average_intensity = (r + g + b) / 3
                binary_value = 1 if average_intensity >= threshold else 0
                output.append(binary_value)
        return output, widthP, heightP  # Vrátíme i šířku a výšku obrázku

    @staticmethod
    def generate_video_part(colors, start_index, end_index, width, height, fps, output_file, queue):
        """Generuje část videa a zapisuje stav do fronty."""
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

        # Progress bar pro snímky v části
        for i in tqdm(range(start_index, end_index), desc=f"Proces {current_process().name}", position=current_process()._identity[0]):
            color = (255, 255, 255) if colors[i] == 0 else (0, 0, 0)
            frame = np.full((height, width, 3), color, dtype=np.uint8)
            out.write(frame)

        out.release()
        queue.put(1)  # Signalizuje dokončení části

    @staticmethod
    def run(imageFileName, outputFileName, num_processes=4):
        # Získání binárních hodnot z obrázku a rozměrů
        colors, width, height = imageToVideo.convert(imageFileName)
        num_frames = len(colors)
        fps = 30  # Počet snímků za sekundu

        # Rozdělení práce do více částí
        chunk_size = num_frames // num_processes
        processes = []
        temp_files = []
        queue = Queue()

        print("Zahajuji generování videa...\n")
        
        # Spuštění procesů pro generování jednotlivých částí videa
        for i in range(num_processes):
            start_index = i * chunk_size
            end_index = num_frames if i == num_processes - 1 else (i + 1) * chunk_size
            temp_file = f"temp_part_{i}.mp4"
            temp_files.append(temp_file)
            process = Process(target=imageToVideo.generate_video_part, args=(colors, start_index, end_index, width, height, fps, temp_file, queue))
            processes.append(process)
            process.start()

        # Sledujeme stav jednotlivých částí
        with tqdm(total=num_processes, desc="Dokončené části", position=0) as pbar:
            completed = 0
            while completed < num_processes:
                queue.get()  # Čeká, dokud se neuloží signál dokončení
                completed += 1
                pbar.update(1)

        for process in processes:
            process.join()

        # Spojení částí do jednoho videa
        print("\nSpojuji všechny části do finálního videa...\n")
        with open("file_list.txt", "w") as file:
            for temp_file in temp_files:
                file.write(f"file '{temp_file}'\n")

        os.system(f"ffmpeg -f concat -safe 0 -i file_list.txt -c copy {outputFileName}")

        # Odstranění dočasných souborů
        for temp_file in temp_files:
            os.remove(temp_file)
        os.remove("file_list.txt")

        print(f"Video bylo úspěšně vytvořeno jako {outputFileName}.")

# Použití
if __name__ == '__main__':
    imageToVideo.run("image.jpg", "output.mp4")