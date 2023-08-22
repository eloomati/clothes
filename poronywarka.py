import cv2
import os


# Wczytaj obraz do porównania i przeszukaj bazę danych, aby znaleźć podobne obrazy.

# def compare_images(image_path, threshold=0.7):
#     query_image = cv2.imread(image_path)
#
#     for image_data in session.query(ImageData).all():
#         database_image = cv2.imread(image_data.file_path)
#
#         # Porównanie zdjęć przy użyciu np. SSIM lub innych miar podobieństwa
#         similarity = calculate_similarity(query_image, database_image)
#
#         if similarity > threshold:
#             print(f'Matched image: {image_data.file_path}')

def compare_images(image_path1, image_path2):
    # Wczytaj obrazy
    img1 = cv2.imread(image_path1)
    img2 = cv2.imread(image_path2)

    # Sprawdź, czy obrazy zostały poprawnie wczytane
    if img1 is None or img2 is None:
        print("Błąd wczytywania obrazu")
        return

    # Porównaj obrazy
    difference = cv2.subtract(img1, img2)
    b, g, r = cv2.split(difference)

    if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
        print("Obrazy są identyczne")
    else:
        print("Obrazy różnią się")

def compare_histograms(hist1, hist2):
    return cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)

def find_similar_images(base_image_path, folder_path):
    base_image = cv2.imread(base_image_path)
    base_hist = cv2.calcHist([base_image], [0], None, [256], [0, 256])

    similar_images = []

    for image_name in os.listdir(folder_path):
        if image_name.lower().endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(folder_path, image_name)
            image = cv2.imread(image_path)
            image_hist = cv2.calcHist([image], [0], None, [256], [0, 256])

            correlation = compare_histograms(base_hist, image_hist)

            if correlation > 0.99:  # Zmień wartość progu podobieństwa według potrzeb
                similar_images.append(image_path)

    return similar_images

if __name__ == "__main__":
    image_path1 = r'D:\porywnywarka\1.jpg'
    image_path2 = r'D:\porywnywarka\1a.jpg'
    compare_images(image_path1, image_path2)

    base_image_path = r'D:\porywnywarka\1.jpg'
    folder_path = r'D:\vision\bluzy'

    similar_images = find_similar_images(base_image_path, folder_path)

    if similar_images:
        print('Podobne zdjecia:')
        for image_path in similar_images:
            print(image_path)

    else:
        print('Brak podobnych zdjec w folderze.')