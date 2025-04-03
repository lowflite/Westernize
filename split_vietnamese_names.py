import os
import json
import argparse

def load_name_dict(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return (
        set(data.get("family_names", [])),
        set(data.get("middle_names", [])),
        set(data.get("compound_given_names", []))
    )

def split_name(name, family_set, compound_given_set):
    parts = name.strip().split()

    if len(parts) < 2:
        return (parts[0] if parts else '', '', ''), 'Too few parts'

    if len(parts) == 2:
        return (parts[0], '', parts[1]), None

    # Name has 3+ parts
    family = parts[0]
    given = parts[-1]
    middle = ' '.join(parts[1:-1])

    # Check for known compound given names
    if len(parts) >= 4:
        last_two = ' '.join(parts[-2:])
        if last_two in compound_given_set:
            given = last_two
            middle = ' '.join(parts[1:-2])

    warning = None
    if family not in family_set:
        warning = f"Unrecognized family name: {family}"
    if len(parts) > 4:
        warning = f"{warning or ''}; Unusually long name ({len(parts)} parts)".strip('; ')

    return (family, middle, given), warning

def main():
    parser = argparse.ArgumentParser(description="Parse Vietnamese names into family, middle, and given parts.")
    parser.add_argument('--input', default='vietnamese_names.txt', help="Input file name (default: vietnamese_names.txt)")
    parser.add_argument('--output', default='names_parsed.tsv', help="TSV output file name (default: names_parsed.tsv)")
    parser.add_argument('--json', default='names_parsed.json', help="JSON output file name (default: names_parsed.json)")
    parser.add_argument('--log', default='issues.log', help="Log file name (default: issues.log)")
    parser.add_argument('--names', default='common_names.json', help="JSON dictionary of common names (default: common_names.json)")

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"❌ Input file not found: {args.input}")
        return

    family_names, middle_names, compound_given_names = load_name_dict(args.names)

    parsed_data = []

    with open(args.input, 'r', encoding='utf-8') as infile, \
         open(args.output, 'w', encoding='utf-8') as tsv_out, \
         open(args.json, 'w', encoding='utf-8') as json_out, \
         open(args.log, 'w', encoding='utf-8') as logfile:

        tsv_out.write("Family\tMiddle\tGiven\n")
        line_number = 1

        for line in infile:
            clean_line = line.strip()
            if not clean_line:
                logfile.write(f"Line {line_number}: Empty line\n")
                line_number += 1
                continue

            (family, middle, given), warning = split_name(clean_line, family_names, compound_given_names)
            parsed_data.append({"line": line_number, "family": family, "middle": middle, "given": given})
            tsv_out.write(f"{family}\t{middle}\t{given}\n")

            if warning:
                logfile.write(f"Line {line_number}: '{clean_line}' — {warning}\n")

            line_number += 1

        json.dump(parsed_data, json_out, ensure_ascii=False, indent=2)

    print(f"✅ TSV saved to: {args.output}")
    print(f"✅ JSON saved to: {args.json}")
    print(f"📝 Log saved to: {args.log}")

if __name__ == "__main__":
    main()
