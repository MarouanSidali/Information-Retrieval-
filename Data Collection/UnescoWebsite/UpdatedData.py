import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Function to parse location information from the text file
def parse_location_info(text_file):
    locations = []
    with open(text_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        current_location = {}

        for line in lines:
            line = line.strip()
            if line.startswith('Title:'):
                current_location['Title'] = line.split(': ', 1)[1]
            elif line.startswith('Country:'):
                current_location['Country'] = line.split(': ', 1)[1]
            elif line.startswith('Description:'):
                current_location['Description'] = line.split(': ', 1)[1]
            elif line.startswith('Content:'):
                current_location['Content'] = line.split(': ', 1)[1]
            elif line.startswith('Image link:'):
                current_location['Image_link'] = line.split(': ', 1)[1]
                locations.append(current_location)
                current_location = {}

    return locations

# Function to add locations to the existing XML file
def add_locations_to_xml(locations, xml_file):
    new_tree = ET.ElementTree(ET.Element("locations"))

    for location in locations:
        location_elem = ET.SubElement(new_tree.getroot(), "location")
        ET.SubElement(location_elem, "Title").text = location.get('Title', '')
        ET.SubElement(location_elem, "Country").text = location.get('Country', '')
        ET.SubElement(location_elem, "Description").text = location.get('Description', '')
        ET.SubElement(location_elem, "Content").text = location.get('Content', '')
        ET.SubElement(location_elem, "Image_link").text = location.get('Image_link', '')

    # Prettify only the portion of the XML that was just added
    rough_string = ET.tostring(new_tree.getroot(), 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")

    # Append the prettified portion to the existing tree
    root = ET.parse(xml_file).getroot()
    new_elements = ET.fromstring(pretty_xml)
    root.extend(new_elements)

    return ET.ElementTree(root)

# Main function
def main():
    text_file_path = '/workspace/Information-Retrieval-/Data Collection/UnescoWebsite/output.txt'
    xml_file_path = '/workspace/Information-Retrieval-/Data Collection/UnescoWebsite/combined_20231227.xml'

    # Parse location information from the text file
    locations = parse_location_info(text_file_path)

    # Add locations to the existing XML file
    new_tree = add_locations_to_xml(locations, xml_file_path)

    # Save the updated XML file
    updated_xml_file_path = '/workspace/Information-Retrieval-/Data Collection/UnescoWebsite/updated_combined_xml_file.xml'
    new_tree.write(updated_xml_file_path, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    main()