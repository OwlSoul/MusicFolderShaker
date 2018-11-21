#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Please, ensure your terminal supports UTF-8 encoding.
# For MS powershell use: chcp 65001

# USAGE EXAMPLE:
# C:\Python\python.exe mfshaker.py "O:\[ Musica Machina ]" "Y:\[ Musica Sync ]\[MX10 - Huawei Honor 9 Lite]"

import os
import random
import shutil
import distutils.dir_util
import argparse

# ----------------                                 CONFIGURATION                                      ---------------- #

# Starting path, folder scan will go from here
# start_path = "O:\\[ Musica Machina ]"

# Output path, folder where new files will be placed
# output_path = "Y:\\[ Musica Sync ]\\[MX10 - Huawei Honor 9 Lite]"

# Maximal selected directory size, in bytes
selection_max_size = 100*1024*1024

# Maximal selection tries
selection_max_tries = 4000

# Maximal selection directories
selection_max_count = 50

# Result file
result_file = "result.log"

# ----------------                                     VARIABLES                                      ---------------- #

# List to store directory full names and directory size
directory_list = []

# List to store directories to be selected for copy
selected_list = []

# ---------------------------------------------------------------------------------------------------------------------#


def write_result(result_filename, result):
    res_file = open(result_filename, "w")
    res_file.write(str(result))
    res_file.close()

# STEP 01: Parsing arguments
parser = argparse.ArgumentParser(description="Music Folder Shaker, this script will select several folders from your "
                                             "music collection and copy them to destination folder, from where you "
                                             "can sync them with some device or do... stuff.\n"
                                             "It is possible AND advisable to set folder count and total size limits."
                                             "\n\n"
                                             "Please, ensure your terminal supports UTF-8 encoding."
                                             "For MS powershell use: chcp 65001")
parser.add_argument("path_in")
parser.add_argument("path_out")
parser.add_argument("--max_size", type=int, help="Maximum size of resulting folders set, in bytes, default is "
                    "4000*1024*1024 (4 GB)")
parser.add_argument("--max_count", type=int, help="Maximum count of folders to be selected, default is 50")
parser.add_argument("--max_tries", type=int, help="Maximum number of tries to select folders, default is 4000")
parser.add_argument("--result_file", help="Result file, will be rewritten every time script runs, default is" 
                    "\"result.log\"")

args = parser.parse_args()
start_path = args.path_in
output_path = args.path_out
if args.max_size:
    selection_max_size = args.max_size
if args.max_count:
    selection_max_count = args.max_count
if args.max_tries:
    selection_max_tries = args.max_tries
if args.result_file:
    result_file = args.result_file

print()
print("PATH IN   : \""+start_path+"\"")
print("PATH OUT  : \""+output_path+"\"")
print("----")
print("MAX SIZE  :", selection_max_size, "/", selection_max_size / (1024*1024), "MB")
print("MAX COUNT :", selection_max_count)
print("MAX TRIES :", selection_max_tries)
print("RESULT FILE:", result_file)
print()

write_result(result_file, 1)

# STEP 02: Forming directory list
print("Scanning folders... ")
for dirpath, dirnames, filenames in os.walk(start_path):
    dir_size = 0
    for f in filenames:
        filename = os.path.join(dirpath, f)
        dir_size += os.path.getsize(filename)
    directory_list.append([dirpath, dir_size])

print("Selecting folders...")
dir_count = len(directory_list)
# Getting the size of folders with subfolders
for i in range(0, dir_count):
    sum_size = 0
    for j in range(i+1, dir_count):
        if directory_list[j][0].startswith(directory_list[i][0]):
            sum_size += directory_list[j][1]  # This is because directory can contain subdirectory AND some files
    directory_list[i][1] += sum_size
print("DONE!")

write_result(result_file, 2)

# STEP 03: Selection process
random.seed()
total_size = 0
selected_count = 0
for i in range(0, selection_max_tries):
    dir_index = random.randint(0, dir_count-1)

    # Check for duplicates
    is_duplicate = False
    for j in range(0, len(selected_list)-1):
        if selected_list[j] == directory_list[dir_index]:
            is_duplicate = True
            break
    if is_duplicate:
        continue

    # Check is size is acceptable
    if total_size + directory_list[dir_index][1] < selection_max_size:
        selected_list.append(directory_list[dir_index])
        selected_count += 1
        total_size += directory_list[dir_index][1]

    # Break the cycle if required number of folders was selected
        if selected_count >= selection_max_count:
            break

print("Total size: ", total_size, "bytes / ", total_size/(1024*1024), "MB")

write_result(result_file, 3)

# STEP 04: Purging target directory
print("Purging target directory...")
for f in os.listdir(output_path):
    filename = os.path.join(output_path, f)
    try:
        if os.path.isfile(filename):
            os.unlink(filename)
        elif os.path.isdir(filename):
            shutil.rmtree(filename)
    except Exception as e:
        print(e)
print(" OK!")

write_result(result_file, 4)

# STEP 05: Copying selected files
print("Copying selected files...")
for i in range(0, len(selected_list)):
    print(str(i+1)+"/"+str(selected_count), selected_list[i][0], ":", selected_list[i][1]/(1024*1024), "MB")
    target_dir = selected_list[i][0][len(start_path)+1:]
    dst_path = os.path.join(output_path, target_dir)
    print("    Copy to:", dst_path, "\n")
    try:
        distutils.dir_util.copy_tree(selected_list[i][0], dst_path)
    except Exception as e:
        print(e)
print("DONE!")

write_result(result_file, 0)

# ----------------                                   END OF SCRIPT                                    ---------------- #

