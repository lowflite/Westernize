import unicodedata

def remove_accents(text):
    """
    Converts Vietnamese characters to closest English equivalents.

    NFKD stands for Normalization Form KD (Compatibility Decomposition)

    """
    normalized = unicodedata.normalize('NFKD', text)
    return ''.join([c for c in normalized if not unicodedata.combining(c)])

def convert_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            clean_line = remove_accents(line)
            outfile.write(clean_line)

if __name__ == "__main__":
    input_path = "names_parsed.tsv"   # Change this as needed
    output_path = "names_western.tsv" # Change this as needed
    convert_file(input_path, output_path)
    print(f"✅ Converted names written to: {output_path}")
