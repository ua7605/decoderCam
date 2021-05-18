import getopt
import sys

import watchFileService


def main(argv):
    # You need to give as arguments first an input file and then an output file

    input_file = ''
    output_file = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('test.py -i <input_file> -o <output_file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <input_file> -o <output_file>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg
    print('Input file is "', input_file)
    print('Output file is "', output_file)
    watchFileService.main(file_path=input_file, file_path_json=output_file)


if __name__ == "__main__":
    main(sys.argv[1:])
