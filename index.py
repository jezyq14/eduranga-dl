import os
import json
import requests
from PIL import Image
from fpdf import FPDF
from PyPDF2 import PdfMerger

with open('config.json') as config_file:
    config = json.load(config_file)

download_folder = config['download_folder']
output_pdf = config['output_pdf']
book_id = config['bookId']
number_of_pages = config['number_of_pages']
cookies = {
    'wsipnet_session': config['wsipnet_session'],
    'wsipnet_session_lifetime': config['wsipnet_session_lifetime']
}

os.makedirs(download_folder, exist_ok=True)

image_paths = []
for number in range(1, number_of_pages + 1):
    url = f"https://appwsipnet.eduranga.pl/e-podreczniki/podglad/{book_id}/files/mobile/{number}.jpg"
    response = requests.get(url, cookies=cookies)
    
    if response.status_code == 200:
        image_path = os.path.join(download_folder, f"{number}.jpg")
        with open(image_path, 'wb') as img_file:
            img_file.write(response.content)
        image_paths.append(image_path)
    else:
        print(f"Failed to download image {number}: {response.status_code}")

temp_pdf_folder = os.path.join(download_folder, "temp_pdfs")
os.makedirs(temp_pdf_folder, exist_ok=True)

for image_path in image_paths:
    with Image.open(image_path) as img:
        width, height = img.size
    
    width_mm = width * 0.264583
    height_mm = height * 0.264583
    
    pdf = FPDF(orientation='P', unit='mm', format=(width_mm, height_mm))
    pdf.add_page()
    
    pdf.image(image_path, x=0, y=0, w=width_mm, h=height_mm)
    
    individual_pdf_path = os.path.join(temp_pdf_folder, f"{os.path.basename(image_path).replace('.jpg', '.pdf')}")
    pdf.output(individual_pdf_path)

merger = PdfMerger()
for pdf_file in os.listdir(temp_pdf_folder):
    if pdf_file.endswith('.pdf'):
        merger.append(os.path.join(temp_pdf_folder, pdf_file))

merger.write(output_pdf)
merger.close()

for pdf_file in os.listdir(temp_pdf_folder):
    os.remove(os.path.join(temp_pdf_folder, pdf_file))
os.rmdir(temp_pdf_folder)

print(f"PDF created successfully: {output_pdf}")