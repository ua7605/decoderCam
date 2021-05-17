# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import watchFileService
import sys, getopt
# if __name__ == '__main__':
#
#     decoder = CamDecoder(file_path='/Users/vincentcharpentier/School/Master/MAP/Decoder/cam_1_20210312T104241_uper.csv', output_file_path='/Users/vincentcharpentier/School/Master/MAP/Decoder/CAMv1.json')
#     #decoder.encode()

def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print ('test.py -i <inputfile> -o <outputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('test.py -i <inputfile> -o <outputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   print('Input file is "', inputfile)
   print('Output file is "', outputfile)
   watchFileService.main(file_path=inputfile, file_path_json=outputfile)



if __name__ == "__main__":
    main(sys.argv[1:])
    #watchFileService.main(file_path='/Users/vincentcharpentier/School/Master/MAP/Decoder/cam_1_20210312T104241_uper.csv', file_path_json='/Users/vincentcharpentier/School/Master/MAP/Decoder/CAMv1.json')


# See PyCharm help at https://www.jetbrains.com/help/pycharm/   /Users/vincentcharpentier/Downloads/username.csv
