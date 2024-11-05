import os
from pathlib import Path, PurePath
import re
from typing import Iterable, List, Union

latex_aux_extensions = [
    "aux",
    "blg",
    "brf",
    "dvi",
    "idx",
    "ilg",
    "ind",
    "lof",
    "log",
    "lol",
    "lot",
    "out",
    "toc",
    "synctex.gz",
    "nav",
    "snm",
    "vrb",
    "pyg",
]

def build_file_ext_regex(extensions: Iterable[str]):
    """ Regular expression that matches file names of any extension.
    Args:
        extensions: List of extensions without leading '.'
    Returns:
        Compiled regular expression
    """
    return re.compile(".*\\.(" + "|".join(extensions) + ")")

def get_files_with_extension(
        working_dir: Union[str, PurePath], extensions: Iterable[str], recursive=False
) -> List[Path]:
    """ Get all files with extension in directory.
    '.git' directories are ignored.
    Args:
        working_dir: directory
        extensions:
    Returns:
        list of Path objects with the matches
    """
    regex = build_file_ext_regex(extensions)
    if not recursive:
        return [
            path for path in Path(working_dir).iterdir()
            if regex.match(path.name)
        ]
    else:
        matches = []
        for root, dirs, files in os.walk(str(working_dir)):
            # Remove .git directories, because they contain .idx files
            dirs[:] = [d for d in dirs if d not in [".git"]]
            matches += [Path(root) / file for file in files if regex.match(file)]
        return matches

def sort_files():
    filenames = ["./workshops.bib", "./journals.bib", "./conferences.bib", "./unrefereed.bib"]

    for filename in filenames:
        entries = []

        # Parse file. Assume reasonably well-formatted.
        with open(filename) as f:
            for line in f:
                if line.startswith("@"):
                    entries.append([])
                entries[-1].append(line)

        # Sort by "key" in "@misc{key,".
        entries.sort(key=lambda lines: re.findall(r'\d+', lines[0].split("{")[1])[0], reverse=True)
        # Save sorted file.
        with open(filename, "w") as f:
            f.write("".join(x for xs in entries for x in xs))
            f.close()

def label_bbls(counts):
    filenames = ["./workshops.bbl", "./journals.bbl", "./conferences.bbl",  "./unrefereed.bbl"]
    labeled_filenames = ["./labeled_workshops.bbl", "./labeled_journals.bbl", "./labeled_conferences.bbl",  "./labeled_unrefereed.bbl"]

    for file in labeled_filenames:
        if os.path.isfile(file):  
            os.remove(str(file))
    indexnames = ["W-", "J-", "C-", "U-"]
    fileindex = 0
    for filename in filenames:
        i = counts[fileindex]+1
        with open(filename) as f:
            for line in f:
                if line.find("bibitem") != -1:
                    i -= 1
                newline = line.replace('\\bibitem{', '\\bibitem['+indexnames[fileindex]+str(i)+']{')
                with open(labeled_filenames[fileindex], "a") as f:
                    f.write(newline)
                    f.close()
        fileindex += 1
    i = 0
    for file in filenames:
        if os.path.isfile(file):  
            os.remove(str(file))
    for myfile in labeled_filenames:
        if os.path.isfile(myfile):
            os.rename(myfile, filenames[i])
            i += 1

# Function to merge all files in a folder
def merge_files(folder_path, counts):    
    myfiles = ["./workshops.bib", "./journals.bib", "./conferences.bib", "./unrefereed.bib"]
    for myfile in myfiles:
        if os.path.isfile(myfile):
            os.remove(myfile)

    my_folder_path = "."
    for folder in os.listdir(folder_path):
        if folder.startswith('.'):
            continue
        folder = os.path.join(folder_path, folder)
        if not os.path.isdir(folder):
            continue
         # open new file in write mode
        files = os.listdir(folder)
        for file in files:
            lines_in_file = []
            if file.endswith('.bib'):
                with open(os.path.join(folder, file)) as f:
                    lines_in_file = f.readlines()
                    if 'acm sigsoft software engineering notes' in (''.join(lines_in_file)).lower():
                        with open(my_folder_path+"/unrefereed.bib", 'a') as nf:
                        # open files to merge in read mode
                            nf.writelines(lines_in_file)
                            # insert a newline after reading each file
                            nf.write("\n")
                            counts[3]+=1
                            nf.close()
                    else:
                        if 'workshop' in (''.join(lines_in_file)).lower():
                            with open(my_folder_path+"/workshops.bib", 'a') as nf:
                                # open files to merge in read mode
                                nf.writelines(lines_in_file)
                                # insert a newline after reading each file
                                nf.write("\n")
                                counts[0]+=1
                                nf.close()
                        else:
                            if 'article' in (''.join(lines_in_file)).lower():
                                with open(my_folder_path+"/journals.bib", 'a') as nf:
                                # open files to merge in read mode
                                    nf.writelines(lines_in_file)
                                    # insert a newline after reading each file
                                    nf.write("\n")
                                    counts[1]+=1
                                    nf.close()        
                            else:
                                if 'inproceedings' in (''.join(lines_in_file)).lower():
                                    with open(my_folder_path+"/conferences.bib", 'a') as nf:
                                        # open files to merge in read mode
                                        nf.writelines(lines_in_file)
                                        # insert a newline after reading each file
                                        nf.write("\n")
                                        counts[2]+=1
                                        nf.close()
    return counts

# Call function from the main folder with the subfolders
counts = merge_files("./content/publication", [0,0,0,0])
sort_files()

os.system("latex cv/journals.tex")
os.system("bibtex journals.aux")
os.system("pdflatex cv/journals.tex")

os.system("latex cv/conferences.tex")
os.system("bibtex conferences.aux")
os.system("pdflatex cv/conferences.tex")
os.system("latex cv/workshops.tex")
os.system("bibtex workshops.aux")
os.system("pdflatex cv/workshops.tex")

os.system("latex cv/unrefereed.tex")
os.system("bibtex unrefereed.aux")
os.system("pdflatex cv/unrefereed.tex")

label_bbls(counts)

myfiles = get_files_with_extension(Path("."), ["bib","tex"])
for myfile in myfiles:
    if os.path.isfile(myfile):
        os.rename(myfile.name, "cv/"+myfile.name)

myfiles = get_files_with_extension(Path("."), ["bib","tex", "bbl"])
for myfile in myfiles:
    if os.path.isfile(myfile):
        os.rename(myfile.name, "../CV/bbl/"+myfile.name)

files = get_files_with_extension(Path("."), latex_aux_extensions)
for file in files:
    os.remove(str(file))

with open("../CV/bbl/statistics.txt", 'w') as nf:
    # open files to merge in read mode
    nf.write(str(counts[1]))
    nf.write(str(" journal papers, "))

    nf.write(str(counts[2]))
    nf.write(" peer-reviewed conference papers, ")
    nf.write(str(counts[3]))
    nf.write(" unrefereed publications, and ")
    nf.write(str(counts[0]))
    nf.write(" peer-reviewed workshop papers")


    #nf.writelines(str("Total count: "))
    #nf.write(str(sum(counts)))
    #nf.write("\n")
    # insert a newline after reading each file
    nf.close()

