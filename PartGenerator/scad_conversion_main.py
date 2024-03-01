import PartGenerator.SCadConverter as SCadConverter
import argparse
import onshapeInterface.ProcessUrl as ProcessUrl
import PartGenerator.Send as Send
import sys

# Parse input arguments.
valid_examples = ["011", "096", "107", "114", "162", "148"]
parser = argparse.ArgumentParser()
parser.add_argument('--mode', help='choose "example" or "custom." Look at code to find which onshape urls to find output',
                    default='example')

parser.add_argument('--scad_file', help='location of scad file',
                    default='PartGenerator/scad/test.scad')

parser.add_argument('--example', help=str(valid_examples),
                    default='011')
args = parser.parse_args()

if __name__ == '__main__':
    if args.mode == "custom":
        filename = args.scad_file
    else:
        filename = "PartGenerator/scad/" + args.example + ".scad"
        if args.example not in valid_examples:
            print("Invalid example name. Choose from: ", valid_examples)
            sys.exit(-1)

    json_url = ProcessUrl.OnshapeUrl(
        "https://cad.onshape.com/documents/c3b4576ef97b70b3e09ba2f0/w/2a155a6e88e3a953e49858f7/e/43845e67493d95a88592d49d")
    part_url = ProcessUrl.OnshapeUrl(
        "https://cad.onshape.com/documents/c3b4576ef97b70b3e09ba2f0/w/2a155a6e88e3a953e49858f7/e/2a5362fe0e6cb33b327a98de")

    combined_request = SCadConverter.build_tree_from_scad(filename)
    json_request = combined_request.get_formatted_request()
    your_mesh = Send.build_part(json_request, part_url=part_url, json_url=json_url, name="aaa")
    print("Onshape part url at %s" % part_url.original_url)