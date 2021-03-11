# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from Decoder import CamDecoder


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #print_hi('PyCharm')

    decoder = CamDecoder(file_path='/Users/vincentcharpentier/Downloads/username.csv', output_file_path='/Users/vincentcharpentier/School/Master/MAP/Decoder/CAMv1.json')
    decoder.encode()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
