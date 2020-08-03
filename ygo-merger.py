#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      zaktu
#
# Created:     03-08-2020
# Copyright:   (c) zaktu 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import glob
import os

def main():
    print("Enter the path of a directory containing any number of .ydk files:")
    print("Does not read any files which have 'merged' in the file name.")
    print("(Current directory is " + os.getcwd() + ")")
    dir = input()
    os.chdir(dir)

    print("Enter a filename for the new merged file (will have '-merged.ydk'"
           + " appended to it)")
    new_file = input()

    main_card_ids = []
    extra_card_ids = []

    for file in glob.glob("*.ydk"):
        if 'merged' not in file:
            parse_file(file, main_card_ids, extra_card_ids)

    print("Removing copies in excess of 3...")
    main_card_dict = remove_excess_triplicates(main_card_ids)
    extra_card_dict = remove_excess_triplicates(extra_card_ids)

    create_new_ydk_file(main_card_dict, extra_card_dict, new_file)

    print("Merging complete!")

def parse_file(file, main_card_ids, extra_card_ids):
    print("Reading " + file)
    ydk = open(file, "r")
    is_main = True

    for line in ydk:
        if '#main' in line:
            continue
        elif '#extra' in line:
            is_main = False
            continue
        elif '!side' in line:
            continue
        elif line.strip() == '':
            continue
        else:
            if is_main:
                main_card_ids.append(line.strip())
            else:
                extra_card_ids.append(line.strip())

def remove_excess_triplicates(card_ids):

    unique_ids = dict.fromkeys(card_ids)
    for card in card_ids:
        if unique_ids[card] == None:
            unique_ids[card] = 1
        elif unique_ids[card] <= 2:
            print("incrementing from " + str(unique_ids[card]) + "to" +  str(unique_ids[card] + 1))
            unique_ids[card] = unique_ids[card] + 1
    return unique_ids

def create_new_ydk_file(main_card_dict, extra_card_dict, file_name):
    new_file_name = file_name + '-merged.ydk'
    print("Writing to " + new_file_name)
    file = open(new_file_name, 'w')

    file.write('#main\n')
    for card, count in main_card_dict.items():
        for i in range(count):
            file.write(card + '\n')
    file.write('#extra\n')
    for card, count in extra_card_dict.items():
        for i in range(count):
            file.write(card + '\n')
    file.write('!side\n')

if __name__ == '__main__':
    main()
