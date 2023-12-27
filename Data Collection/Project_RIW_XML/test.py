import os
import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom

base_site = 'https://www.atlasobscura.com'  # Base site

regions = {
    "Africa": {
        "North Africa": ["algeria", "egypt", "libya", "mauritania", "morocco", "sudan", "tunisia"],
        "West Africa": ["benin", "burkina-faso", "cape-verde", "ivory-coast", "gambia", "ghana", "guinea", "guinea-bissau", "liberia", "mali", "niger", "nigeria", "senegal", "sierra-leone", "togo"],
        "Central Africa": ["angola", "cameroon", "central-african-republic", "chad", "democratic-republic-of-the-congo", "equatorial-guinea", "gabon", "republic-of-the-congo", "sao-tome-and-principe"],
        "East Africa": ["burundi", "comoros", "djibouti", "eritrea", "ethiopia", "kenya", "madagascar", "malawi", "mauritius", "mozambique", "rwanda", "seychelles", "somalia", "south-sudan", "tanzania", "uganda", "zambia", "zimbabwe"],
        "Southern Africa": ["botswana", "eswatini", "lesotho", "namibia", "south-africa"]
    },
    "Asia": {
        "Central Asia": ["kazakhstan", "kyrgyzstan", "tajikistan", "turkmenistan", "uzbekistan"],
        "Eastern Asia": ["china", "japan", "mongolia", "north-korea", "south-korea", "taiwan"],
        "Southern Asia": ["afghanistan", "bangladesh", "bhutan", "india", "iran", "maldives", "nepal", "pakistan", "sri-lanka"],
        "South-Eastern Asia": ["brunei", "cambodia", "east-timor", "indonesia", "laos", "malaysia", "myanmar", "philippines", "singapore", "thailand", "vietnam"],
        "Western Asia": ["armenia", "azerbaijan", "bahrain", "cyprus", "georgia", "iraq", "israel", "jordan", "kuwait", "lebanon", "oman", "palestine", "qatar", "saudi-arabia", "syria", "turkey", "united-arab-emirates", "yemen"]
    },
    "Europe": {
        "Eastern Europe": ["belarus", "bulgaria", "czech-republic", "hungary", "moldova", "poland", "romania", "russia", "slovakia", "ukraine"],
        "Northern Europe": ["denmark", "estonia", "finland", "iceland", "ireland", "latvia", "lithuania", "norway", "sweden", "united-kingdom"],
        "Southern Europe": ["albania", "andorra", "bosnia-and-herzegovina", "croatia", "greece", "italy", "kosovo", "malta", "montenegro", "north-macedonia", "portugal", "san-marino", "serbia", "slovenia", "spain", "vatican-city"],
        "Western Europe": ["austria", "belgium", "france", "germany", "liechtenstein", "luxembourg", "monaco", "netherlands", "switzerland"]
    },
    "North America": {
        "Northern America": ["canada", "united-states", "mexico"],
        "Central America": ["belize", "costa-rica", "el-salvador", "guatemala", "honduras", "nicaragua", "panama"],
        "Caribbean": ["antigua-and-barbuda", "bahamas", "barbados", "cuba", "dominica", "dominican-republic", "grenada", "haiti", "jamaica", "saint-kitts-and-nevis", "saint-lucia", "saint-vincent-and-the-grenadines", "trinidad-and-tobago"]
    },
    "Oceania": {
        "Australia and New Zealand": ["australia", "new-zealand"],
        "Melanesia": ["fiji", "papua-new-guinea", "solomon-islands", "vanuatu"],
        "Micronesia": ["kiribati", "marshall-islands", "micronesia", "nauru", "palau"],
        "Polynesia": ["samoa", "tonga", "tuvalu"]
    },
    "South America": {
        "South America": ["argentina", "bolivia", "brazil", "chile", "colombia", "ecuador", "guyana", "paraguay", "peru", "suriname", "uruguay", "venezuela"]
    }
}

# Create a directory to store output files
output_dir = 'output_files'
os.makedirs(output_dir, exist_ok=True)

for continent, continent_regions in regions.items():
    for region, countries in continent_regions.items():
        # Generate a dynamic file name based on the current date, continent, and region
        file_name = f"{continent}_{region}_{datetime.now().strftime('%Y%m%d')}.xml"
        file_path = os.path.join(output_dir, file_name)

        # Create the root element
        root = ET.Element("data")

        with open(file_path, "wb") as file:
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

                        # Create location element and add data
                        location_elem = ET.SubElement(root, "location")
                        ET.SubElement(location_elem, "Title").text = title
                        ET.SubElement(location_elem, "Country").text = country
                        ET.SubElement(location_elem, "Description").text = description
                        ET.SubElement(location_elem, "Content").text = content
                        ET.SubElement(location_elem, "Image_link").text = image_src

            # Create an ElementTree object
            tree = ET.ElementTree(root)

            # Use minidom to prettify the XML output
            xml_str = minidom.parseString(ET.tostring(root, 'utf-8')).toprettyxml(indent="    ")

            # Write the formatted XML to the file
            file.write(xml_str.encode('utf-8'))

