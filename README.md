# MusicFolderShaker

This script selects several folders from your music collection and copies them to designated location, from where you can sync it with something or do other stuff. 

### What does it do?

Script will create a list of all folders located inside **input_folder** and will *randomly* copy up to **max_count** directories to the **output_folder**, with a guarantee that total size of all copied folders will not exceed **max_size**.

### Why was it created?

It was designed to provide random selection of music every week to be automatically uploaded to the phone and it is possible and advisable to set total selection size and total number of folders selected.

The script copies music by folders (considered as albums), and will also preserve file hierarchy in the output folder as well (example: "*input_folder/artist/album_a*" will be copied to "*output_folder/artist/album_a*"). There is a slight chance it will copy folder with sub-folders (e.g. full discography), but statistically it is quite low.

Will work with any files, not only music ones, just was created for music.

## Usage
```python mfshaker.py input_directory output_directory --max_size 2097152 --max_count 50 --max_tries 4000 --result_file mfshaker.result ```

`input_directory` and `output_directory` are mandatory, first one is the directory from which files will be taken, and second one is the folder where to place the selection. Output directory contents will be completely erased before new selection will be copied there.

`max_size` - maximum size of selection in BYTES. Optional, default is 100\*1024\*1024 (100 MB)

`max_count` - maximum number of folders to be selected. Optional, default is 50.

`max_tries` - maximum number of tries to make a selection. Script works by randomly selecting a folder, and if it does not fit (total size too big), it will select another random folder. This value limits maximum number of this attempts. Optional, default is 4000.

`result_file` - file to store the result of the script. I used for monitoring this script right now. Optional, default is "result.log"
Returns following values:
0 - script completed without errors.
1 - error in scanning input folder (does not exist or access violations)
2 - selection process failed
3 - failed to empty target directory
4 - failed to copy selection to destination folder (does not exist, access violation etc.)

## Notes
Please ensure your terminal supports Unicode in case you have Unicode-named files (Japanese, Korean, Chinese etc.) 

For MS Windows PowerShell - use `chcp 65001` before using this script.
