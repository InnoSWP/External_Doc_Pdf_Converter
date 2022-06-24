import argparse
import utils
import pdf2image
from pathlib import Path
import numpy as np
import cv2
from PIL import ImageChops
from PIL import Image


def pil_to_np(pil_img):
    return np.array(pil_img)


def np_to_pil(np_img):
    return Image.fromarray(np.uint8(np_img))


def crop_np_image(np_img):
    gray = cv2.cvtColor(np_img, cv2.COLOR_BGR2GRAY)
    gray = 255 * (gray < 128).astype(np.uint8)  # To invert the text to white
    coords = cv2.findNonZero(gray)  # Find all non-zero points (text)
    x, y, w, h = cv2.boundingRect(coords)  # Find minimum spanning bounding box
    rect = np_img[y:y + h, x:x + w]  # Crop the image - note we do this on the original image
    return rect


def compare_two_pdfs(good_pdf: Path, bad_pdf: Path):
    print("path1", good_pdf, "path2", bad_pdf)
    image_good = pdf2image.convert_from_path(good_pdf)
    image_bad = pdf2image.convert_from_path(bad_pdf)
    for (pil_good_image, pil_bad_image) in zip(image_good, image_bad):
        # np_good_image = np.array(pil_good_image)
        # np_bad_image = np.array(pil_bad_image)
        np_good_image = crop_np_image(np.array(pil_good_image))
        np_bad_image = crop_np_image(np.array(pil_bad_image))
        ratio = np_good_image.shape[0] / np_bad_image.shape[0]
        new_size = (int(np_bad_image.shape[1] * ratio), int(np_bad_image.shape[0] * ratio))
        np_bad_image = cv2.resize(np_bad_image, new_size)
        pil_good_image = np_to_pil(np_good_image)
        pil_bad_image = np_to_pil(np_bad_image)
        im_diff = ImageChops.difference(pil_good_image, pil_bad_image)
        np_diff_image = np.array(im_diff)
        size = 0.45
        resized_good = cv2.resize(np_good_image,
                                  (int(np_good_image.shape[:2][1] * size), int(np_good_image.shape[:2][0] * size)))
        resized_bad = cv2.resize(np_bad_image,
                                 (int(np_bad_image.shape[:2][1] * size), int(np_bad_image.shape[:2][0] * size)))
        resized_diff = cv2.resize(np_diff_image,
                                  (int(np_diff_image.shape[:2][1] * size), int(np_diff_image.shape[:2][0] * size)))
        cv2.imshow("good", resized_good)
        cv2.imshow("bad", resized_bad)
        cv2.imshow("diff", resized_diff)
        cv2.waitKey(0)


def main():
    parser = argparse.ArgumentParser("Convert documents to pdf files")
    parser.add_argument("foldergood", type=utils.validate_dir, help="folder with the good pdfs")
    parser.add_argument("folderbad", type=utils.validate_dir, help="folder with the bad pdfs")
    p = parser.parse_args()
    good_pdf_dir: Path = p.foldergood.absolute()
    bad_pdf_dir: Path = p.folderbad.absolute()
    files_good = []
    files_bad = []
    for entry in good_pdf_dir.iterdir():
        if entry.is_file():
            files_good.append(entry)
    for entry in bad_pdf_dir.iterdir():
        if entry.is_file():
            files_bad.append(entry)
    for (pdf_good, pdf_bad) in zip(files_good, files_bad):
        compare_two_pdfs(pdf_good.absolute(), pdf_bad.absolute())


if __name__ == "__main__":
    main()
