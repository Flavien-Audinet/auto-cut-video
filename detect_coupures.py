import cv2

def detecter_coupures(video_path, seuil=8000000):
    # Ouvrir la vidéo
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Erreur lors de l'ouverture de la vidéo.")
        return [], 0

    # Lire la première trame
    ret, prev_frame = cap.read()
    prev_frame = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    coupure_indices = []
    coupure_count = 0
    frame_count = 1

    while True:
        # Lire la trame suivante
        ret, current_frame = cap.read()
        if not ret:
            break

        # Convertir la trame en niveaux de gris pour faciliter la comparaison
        current_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)

        # Calculer la différence absolue entre les deux trames
        diff = cv2.absdiff(current_frame, prev_frame)

        # Somme des différences de pixels pour la trame actuelle
        somme_diff_pixels = diff.sum()

        # Si la somme des différences est supérieure au seuil, une coupure est détectée
        if somme_diff_pixels > seuil:
            # Récupérer le time code correspondant à la trame détectée
            timecode_ms = (frame_count / cap.get(cv2.CAP_PROP_FPS)) * 1000
            secondes, timecode_ms = divmod(int(timecode_ms), 1000)
            minutes, secondes = divmod(secondes, 60)
            heures, minutes = divmod(minutes, 60)
            timecode = f"{heures:02d}:{minutes:02d}:{secondes:02d}.{timecode_ms:03d}"
            coupure_indices.append(timecode)
            coupure_count += 1

        # Mettre à jour la trame précédente pour la prochaine itération
        prev_frame = current_frame

        # Incrémenter le compteur de trame
        frame_count += 1

    # Fermer la vidéo
    cap.release()

    return coupure_indices, coupure_count

# Exemple d'utilisation du script pour détecter les coupures dans une vidéo
if __name__ == "__main__":
    # Chemin vers la vidéo d'entrée
    video_path = input("Entrez le chemin vers la vidéo : ")

    # Seuil de détection des coupures (8000000)
    seuil = 8000000

    coupure_indices, coupure_count = detecter_coupures(video_path, seuil)

    print("Time codes des coupures détectées :")
    for timecode in coupure_indices:
        print(timecode)

    print("Nombre total de coupures détectées :", coupure_count)