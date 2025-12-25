import cv2
import numpy as np


COULEURS_REF = {
    'Blanc': (255, 255, 255),
    'Jaune': (0, 255, 255),
    'Vert': (0, 255, 0),
    'Bleu': (255, 0, 0),
    'Orange': (0, 165, 255),
    'Rouge': (0, 0, 255)
}

cap = cv2.VideoCapture(0)
taille_zone = 200

print("Appuyez sur 'd' pour détecter, 'q' pour quitter.")

while True:
    ret, frame = cap.read()
    if not ret:
        break
        

    frame_analyse = frame.copy()

    height, width, _ = frame.shape
    x1 = int(width / 2 - taille_zone / 2)
    y1 = int(height / 2 - taille_zone / 2)
    x2 = int(width / 2 + taille_zone / 2)
    y2 = int(height / 2 + taille_zone / 2)


    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)

    points_a_analyser = []
    pas = int(taille_zone / 3)
    offset = int(pas / 2)

    for i in range(3):
        for j in range(3):
            cx = x1 + j * pas + offset
            cy = y1 + i * pas + offset
            points_a_analyser.append((cx, cy))
            cv2.circle(frame, (cx, cy), 3, (255, 255, 255), -1)

    cv2.imshow('TP5 - Rubiks Cube', frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('d'):
        print("\n--- DETECTION ---")
        
        for idx, (px, py) in enumerate(points_a_analyser):
            b, g, r = frame_analyse[py, px]


            nom_couleur = "Inconnu"
            dist_min = float('inf')

            for nom_ref, (rb, rg, rr) in COULEURS_REF.items():
                dist = np.sqrt((b - rb)**2 + (g - rg)**2 + (r - rr)**2)
                if dist < dist_min:
                    dist_min = dist
                    nom_couleur = nom_ref

            print(f"Case {idx+1} : {nom_couleur} (BGR: {b},{g},{r})")

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()