import json
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, XSD
from datetime import datetime

DECRYPTONTO = Namespace("https://de-crypt.org/r/")

def create_ontology():
    g = Graph()
    g.bind("decryptonto", DECRYPTONTO)
    
    # Load your ontology file
    g.parse("DecryptONTO.ttl", format="turtle")
    
    return g

def load_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except UnicodeDecodeError:
        print(f"UTF-8 decoding failed. Trying with 'utf-8-sig' encoding...")
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            return json.load(f)

def populate_ontology(g, data):
    for record in data:
        record_uri = URIRef(DECRYPTONTO[record['records']['id']])
        g.add((record_uri, RDF.type, DECRYPTONTO.Record))
        
        # Add all properties
        property_mappings = {
            'id': (DECRYPTONTO.hasID, XSD.string),
            'name': (DECRYPTONTO.hasName, XSD.string),
            'current_country': (DECRYPTONTO.hasCurrentCountry, XSD.string),
            'current_city': (DECRYPTONTO.hasCurrentCity, XSD.string),
            'current_holder': (DECRYPTONTO.hasCurrentHolder, XSD.string),
            'additional_information': (DECRYPTONTO.hasAdditionalInformation, XSD.string),
            'number_of_pages': (DECRYPTONTO.hasNumberOfPages, XSD.integer),
            'cleartext_lang': (DECRYPTONTO.hasCleartextLanguage, XSD.string),
            'author': (DECRYPTONTO.hasAuthor, XSD.string),
            'creation_date': (DECRYPTONTO.hasCreationDate, XSD.dateTime),
            'private_ciphertext': (DECRYPTONTO.hasPrivateCiphertext, XSD.boolean),
            'cipher_types': (DECRYPTONTO.hasCipherTypes, XSD.string),
            'symbol_sets': (DECRYPTONTO.hasSymbolSets, XSD.string),
            'status': (DECRYPTONTO.hasStatus, XSD.string),
            'record_type': (DECRYPTONTO.hasRecordType, XSD.string),
            #'access_mode': (DECRYPTONTO.hasAccessMode, XSD.string),
            'start_year': (DECRYPTONTO.hasStartYear, XSD.integer)
        }

        for key, (predicate, datatype) in property_mappings.items():
            if key in record['records'] and record['records'][key] is not None:
                value = record['records'][key]
                if datatype == XSD.boolean:
                    value = value.lower() == 'true'
                elif datatype == XSD.integer:
                    value = int(value)
                elif datatype == XSD.dateTime:
                    # Parse the datetime and format it to ISO 8601
                    try:
                        dt = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                        value = dt.isoformat()
                    except ValueError:
                        print(f"Warning: Unable to parse datetime '{value}' for record {record['id']}. Skipping this field.")
                        continue
                g.add((record_uri, predicate, Literal(value, datatype=datatype)))

    return g

def main():
    g = create_ontology()
    data = load_data('decode_records_detailed.json')
    g = populate_ontology(g, data)
    
    # Save the populated ontology
    g.serialize(destination="populated_decryptontology.ttl", format="turtle")

if __name__ == "__main__":
    main()
