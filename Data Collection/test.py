# from bs4 import BeautifulSoup
# import requests

# url = 'https://www.atlasobscura.com/things-to-do/algeria/places'
# response = requests.get(url)
# soup = BeautifulSoup(response.content, 'html.parser')

# card_bodies = soup.find_all('a', class_='Card')

# # for card_body in card_bodies:
# #             anchor_tag = card_body.find('a')  # Adjust this based on the actual structure
            
# #             if anchor_tag and 'href' in anchor_tag.attrs:
# #                 link = anchor_tag['href']
# #                 full_url = base_url + link  # Construct the full URL for the linked page
                
# #                 # Scrape content from the linked page (similar to previous examples)
# #                 linked_response = requests.get(full_url)
# # # Process and store 'title' and 'description' in your dataset

# print(card_bodies)

# from bs4 import BeautifulSoup
# import requests

# url = 'https://www.atlasobscura.com/things-to-do/algeria/places'
# response = requests.get(url)
# soup = BeautifulSoup(response.content, 'html.parser')

# card_bodies = soup.find_all('a', class_='Card')

# base_site = 'https://www.atlasobscura.com'  # Base site

# for card_body in card_bodies:
#     # Extract the href attribute from each anchor tag
#     href = card_body['href']  # Assuming 'href' is the attribute you want to extract
    
#     # Construct the full URL by appending the href to the base site
#     full_url = base_site + href
    
#     print(full_url)  # Print or process the constructed URLs as needed

# from bs4 import BeautifulSoup
# import requests

# base_site = 'https://www.atlasobscura.com'  # Base site

# url = 'https://www.atlasobscura.com/things-to-do/algeria/places'
# response = requests.get(url)
# soup = BeautifulSoup(response.content, 'html.parser')

# card_bodies = soup.find_all('a', class_='Card')

# for card_body in card_bodies:
#     href = card_body['href']
#     full_url = base_site + href

#     # Visit each linked page and extract data
#     linked_response = requests.get(full_url)
    
#     if linked_response.status_code == 200:
#         linked_soup = BeautifulSoup(linked_response.content, 'html.parser')
        
#         # Extract content from the linked page
#         # Adjust the tags and attributes according to the structure of the linked page
#         title = linked_soup.find('h1').text.strip()
#         description = linked_soup.find('h3', class_='DDPage__header-dek' ).text.strip()
#         content = linked_soup.find('div',class_='DDP__body-copy').text.strip()
#         # description = linked_soup.find('div', class_='description').text.strip()
        
#         # Process and use the extracted data
#         print("Title:", title)
#         print("Description:", description)
#         print("Content:", content)  
#         # print("---------")
#     else:
#         print(f"Failed to retrieve data from {full_url}")

# from bs4 import BeautifulSoup
# import requests

# base_site = 'https://www.atlasobscura.com'  # Base site

# url = 'https://www.atlasobscura.com/things-to-do/morocco/places'
# response = requests.get(url)
# soup = BeautifulSoup(response.content, 'html.parser')

# card_bodies = soup.find_all('a', class_='Card')

# for card_body in card_bodies:
#     href = card_body['href']
#     full_url = base_site + href

#     # Visit each linked page and extract data
#     linked_response = requests.get(full_url)
    
#     if linked_response.status_code == 200:
#         linked_soup = BeautifulSoup(linked_response.content, 'html.parser')
        
#         # Extract content from the linked page
#         # Adjust the tags and attributes according to the structure of the linked page
#         title = linked_soup.find('h1').text.strip()
#         description = linked_soup.find('h3', class_='DDPage__header-dek' ).text.strip()
#         content = linked_soup.find('div',class_='DDP__body-copy').text.strip()
#         # description = linked_soup.find('div', class_='description').text.strip()
        
#         # Process and use the extracted data
#         print("Title:", title)
#         print("Description:", description)
#         print("Content:", content)  
#         print("----------------------------------------")
#     else:
#         print(f"Failed to retrieve data from {full_url}")


from bs4 import BeautifulSoup
import requests

base_site = 'https://www.atlasobscura.com'  # Base site
url = 'https://www.atlasobscura.com/things-to-do/algeria/places'

# Create a session object for requests
session = requests.Session()

# Send a GETquest to the reundefinedtarget URL and create a BeautifulSoup object
response = session.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find all the anchor tags with the class "Card" on the page
card_bodies = soup.find_all('a', class_='Card')

for card_body in card_bodies:
    href = card_body['href']
    full_url = base_site + href

    # Send a GET request to each constructed URL and create a BeautifulSoup object
    linked_response = session.get(full_url)
    
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
        
        
        print("Title:", title)
        print("Description:", description)
        print("Content:", content)
        print("Image src:", image_src)  
        print("----------------------------------------")
    else:
        print(f"Failed to retrieve data from {full_url}")

