import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import random

# List of country codes
# country_codes = ['AF', 'AL', 'DZ', 'AD', 'AO', 'AG', 'AR', 'AM', 'AU', 'AT', 'AZ', 'BS', 'BH', 'BD', 'BB', 'BY', 'BE', 'BZ',
#     'BJ', 'BT', 'BO', 'BA', 'BW', 'BR', 'BN', 'BG', 'BF', 'BI', 'CV', 'KH', 'CM', 'CA', 'CF', 'TD', 'CL', 'CN',
#     'CO', 'KM', 'CD', 'CG', 'CR', 'HR', 'CU', 'CY', 'CZ', 'DK', 'DJ', 'DM', 'DO', 'EC', 'EG', 'SV', 'GQ', 'ER',
#     'EE', 'SZ', 'ET', 'FJ', 'FI', 'FR', 'GA', 'GM', 'GE', 'DE', 'GH', 'GR', 'GD', 'GT', 'GN', 'GW', 'GY', 'HT',
#     'HN', 'HU', 'IS', 'IN', 'ID', 'IR', 'IQ', 'IE', 'IL', 'IT', 'JM', 'JP', 'JO', 'KZ', 'KE', 'KI', 'KP', 'KR',
#     'KW', 'KG', 'LA', 'LV', 'LB', 'LS', 'LR', 'LY', 'LI', 'LT', 'LU', 'MK', 'MG', 'MW', 'MY', 'MV', 'ML', 'MT',
#     'MH', 'MR', 'MU', 'MX', 'FM', 'MD', 'MC', 'MN', 'ME', 'MA', 'MZ', 'MM', 'NA', 'NR', 'NP', 'NL', 'NZ', 'NI',
#     'NE', 'NG', 'NO', 'OM', 'PK', 'PW', 'PA', 'PG', 'PY', 'PE', 'PH', 'PL', 'PT', 'QA', 'RO', 'RU', 'RW', 'KN',
#     'LC', 'VC', 'WS', 'SM', 'ST', 'SA', 'SN', 'RS', 'SC', 'SL', 'SG', 'SK', 'SI', 'SB', 'SO', 'ZA', 'ES', 'LK',
#     'SD', 'SR', 'SE', 'CH', 'SY', 'TJ', 'TZ', 'TH', 'TL', 'TG', 'TO', 'TT', 'TN', 'TR', 'TM', 'TV', 'UG', 'UA',
#     'AE', 'GB', 'US', 'UY', 'UZ', 'VU', 'VA', 'VE', 'VN', 'YE', 'ZM', 'ZW'
# ]

# Custom headers with a user-agent
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

def get_soup(url):
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception if the GET request was not successful
    return BeautifulSoup(response.text, 'html.parser')

def scrape_country(country_code, file):
    url = f'https://whc.unesco.org/en/statesparties/{country_code}'
    soup = get_soup(url)

    # Find and scrape the country title
    country_title_tag = soup.find('h1', class_='text-break')
    country_title = country_title_tag.get_text(strip=True) if country_title_tag else 'Title not found'

    div_with_list = soup.find('div', class_='overflow-auto scrollbar-custom')
    ul = div_with_list and div_with_list.find('ul', class_='mb-3 pl-3')
    items = ul and ul.find_all('li', class_='cultural')

    if items:
        # Shuffle the list of items randomly
        random.shuffle(items)
        
        # Limit to a maximum of 10 items
        items = items[:10]

        for item in items:
            anchor = item.find('a', href=True)
            if anchor:
                absolute_url = urljoin(url, anchor['href'])
                file.write(f"Title: {anchor.get_text(strip=True)}\n")
                file.write(f"Country: {country_title}\n")
                file.write(f"Description: {item.get_text(strip=True)}\n")

                item_soup = get_soup(absolute_url)

                # Find and concatenate content from p tags inside div with class 'border-top pt-4 mt-4'
                additional_content_div = item_soup.find('div', class_='border-top pt-4 mt-4')
                if additional_content_div:
                    p_tags = additional_content_div.find_all('p')
                    content = ' '.join([p_tag.get_text(strip=True) for p_tag in p_tags])
                    file.write(f"Content: {content}\n")

                # Find the img tag inside the anchor tag within div with class 'w-100'
                w100_div = item_soup.find('div', class_='border-top mt-4 pt-4')
                anchor_tag = w100_div and w100_div.find('a')
                img_tag = anchor_tag and anchor_tag.find('img')
                img_src = img_tag['src'] if img_tag and 'src' in img_tag.attrs else 'Image source not found'
                file.write(f"Image link: {img_src}\n")
                file.write("----------------------------------------\n")
                
                time.sleep(10)  
    else:
        print(f'No items found for {country_code}.')

    # file.write(f"Country Title: {country_title}\n\n")

def main():
    with open('output.txt', 'a', encoding='utf-8') as file:
        for country_code in country_codes:
            print(f"Scraping data for {country_code}...")
            scrape_country(country_code, file)

if __name__ == "__main__":
    main()