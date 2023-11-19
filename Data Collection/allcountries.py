# from bs4 import BeautifulSoup
# import requests
# base_site = 'https://www.atlasobscura.com'  # Base site

# # Define the regions and their countries
# regions = {
#     "Northern Africa": ["algeria", "egypt", "libya", "mauritania", "morocco", "sudan", "tunisia"],
#     "Western Africa": ["benin", "burkina-faso", "cape-verde", "ivory-coast", "gambia", "ghana", "guinea", "guinea-bissau", "liberia", "mali", "niger", "nigeria", "senegal", "sierra-leone", "togo"],
#     "Central Africa": ["angola", "cameroon", "central-african-republic", "chad", "democratic-republic-of-the-congo", "equatorial-guinea", "gabon", "republic-of-the-congo", "sao-tome-and-principe"],
#     "Eastern Africa": ["burundi", "comoros", "djibouti", "eritrea", "ethiopia", "kenya", "madagascar", "malawi", "mauritius", "mozambique", "rwanda", "seychelles", "somalia", "south-sudan", "tanzania", "uganda", "zambia", "zimbabwe"],
#     "Southern Africa": ["botswana", "eswatini", "lesotho", "namibia", "south-africa"]
# }

# for region, countries in regions.items():
#     with open(f"{region}.txt", "w") as file:
#         for country in countries:
#             url = f'https://www.atlasobscura.com/things-to-do/{country}/places'
#             response = requests.get(url)
#             soup = BeautifulSoup(response.content, 'html.parser')

#             card_bodies = soup.find_all('a', class_='Card')

#             for card_body in card_bodies:
#                 href = card_body['href']
#                 full_url = base_site + href

#                 # Visit each linked page and extract data
#                 linked_response = requests.get(full_url)
                
#                 if linked_response.status_code == 200:
#                     linked_soup = BeautifulSoup(linked_response.content, 'html.parser')
                    
#                     # Extract content from the linked page
#                     title = linked_soup.find('h1').text.strip()
#                     description = linked_soup.find('h3', class_='DDPage__header-dek' ).text.strip()
#                     content = linked_soup.find('div',class_='DDP__body-copy').text.strip()
                    
#                     # Write the extracted data to the file
#                     file.write(f"Title: {title}\n")
#                     file.write(f"Country: {country}\n")
#                     file.write(f"Description: {description}\n")
#                     file.write(f"Content: {content}\n")
#                     file.write("----------------------------------------\n")
#                 else:
#                     print(f"Failed to retrieve data from {full_url}")

from bs4 import BeautifulSoup
import requests
import os
import time
from datetime import datetime

base_site = 'https://www.atlasobscura.com'  # Base site

regions = {
    "Northern Africa": ["algeria", "egypt", "libya", "mauritania", "morocco", "sudan", "tunisia"],
    "Western Africa": ["benin", "burkina-faso", "cape-verde", "ivory-coast", "gambia", "ghana", "guinea", "guinea-bissau", "liberia", "mali", "niger", "nigeria", "senegal", "sierra-leone", "togo"],
    "Central Africa": ["angola", "cameroon", "central-african-republic", "chad", "democratic-republic-of-the-congo", "equatorial-guinea", "gabon", "republic-of-the-congo", "sao-tome-and-principe"],
    "Eastern Africa": ["burundi", "comoros", "djibouti", "eritrea", "ethiopia", "kenya", "madagascar", "malawi", "mauritius", "mozambique", "rwanda", "seychelles", "somalia", "south-sudan", "tanzania", "uganda", "zambia", "zimbabwe"],
    "Southern Africa": ["botswana", "eswatini", "lesotho", "namibia", "south-africa"]
}

# Create a directory to store output files
output_dir = 'output_files'
os.makedirs(output_dir, exist_ok=True)

for region, countries in regions.items():
    # Generate a dynamic file name based on the current date and region
    file_name = f"{region}_{datetime.now().strftime('%Y%m%d')}.txt"
    file_path = os.path.join(output_dir, file_name)

    with open(file_path, "w") as file:
        for country in countries:
            url = f'https://www.atlasobscura.com/things-to-do/{country}/places'
            

            response = requests.get(url)

            time.sleep(1)  # Sleep for 1 second
            
            soup = BeautifulSoup(response.content, 'html.parser')

            card_bodies = soup.find_all('a', class_='Card')

            for card_body in card_bodies:
                href = card_body['href']
                full_url = base_site + href

                # Visit each linked page and extract data
                linked_response = requests.get(full_url)

                if linked_response.status_code == 200:
                    linked_soup = BeautifulSoup(linked_response.content, 'html.parser')

                    # Extract content from the linked page
                    title = linked_soup.find('h1').text.strip()
                    description = linked_soup.find('h3', class_='DDPage__header-dek').text.strip()
                    content = linked_soup.find('div', class_='DDP__body-copy').text.strip()
                    image_div = linked_soup.find('div', class_='DDPage__item-gallery-container item-gallery-container hidden-print')
                    
                    if image_div:
                        image_src = image_div.find('img')['src']
                    else:
                        image_src = None   

                    # Write the extracted data to the file
                    file.write(f"Title: {title}\n")
                    file.write(f"Country: {country}\n")
                    file.write(f"Description: {description}\n")
                    file.write(f"Content: {content}\n")
                    file.write(f"Image link: {image_src}\n")
                    file.write("----------------------------------------\n")
                else:
                    print(f"Failed to retrieve data from {full_url}")
                    