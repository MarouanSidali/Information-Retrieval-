import xml.etree.ElementTree as ET

# Load the XML file
xml_file_path = '/Users/yuskiem/Downloads/Information-Retrieval--master/Data Collection/UnescoWebsite/xml_doc_id/updated_combined_xml_file.xml'
tree = ET.parse(xml_file_path)
root = tree.getroot()

# Initialize Doc_ID counter
doc_id_counter = 1

# Iterate over each 'location' element
for location in root.findall('.//location'):
    # Create a new 'Doc_ID' element and set its text
    doc_id_element = ET.Element('Doc_ID')
    doc_id_element.text = str(doc_id_counter)

    # Increment the Doc_ID counter for the next iteration
    doc_id_counter += 1

    # Insert the 'Doc_ID' element as the first subelement of 'location'
    location.insert(0, doc_id_element)

# Write the modified XML back to the file
tree.write('/Users/yuskiem/Downloads/Information-Retrieval--master/Data Collection/UnescoWebsite/xml_doc_id/updated_docID_combined_xml_file.xml', encoding='utf-8', xml_declaration=True)
