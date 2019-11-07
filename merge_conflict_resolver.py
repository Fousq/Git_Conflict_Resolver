import os
import re

def load_ignore_file(path: str) -> list:
    files_ignore = [".fileignore", ".gitignore"]
    tree = os.walk(path)
    for dir_path, dir_name, file_names in tree:
        for file_name in file_names:
            if (file_name == ".gitignore") or (file_name == ".fileignore"):
                f = open(file_name, "r")
                for line in f.readlines():
                    file = line
                    if line[-1] == '\n':
                        file = line[:-1]
                    files_ignore.append(file)
                f.close()
            break
    return files_ignore

def skip_file(file: str, files_ignore: list) -> bool:
    for file_ignore in files_ignore:
        if re.match(file_ignore, file) != None:
            return True
    return False

"""
    @param: path - the path where merge conflict was caused
"""
def resolve(path: str):
    files_ignore = load_ignore_file(path)
    tree = os.walk(path)
    for dir_path, dir_name, file_names in tree:
        for file_name in file_names:
            if not skip_file(file_name, files_ignore):
                delete_conflict_content(file_name)
    pass

def delete_conflict_content(file: str):
    print("file to update: " + file)
    pattern_start = r">>>>>>> HEAD"
    pattern_end = r"======="
    is_deleted = False
    start = False
    end = False
    start_index = 0
    end_index = 0
    f = open(file, "r+")
    lines = f.readlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        print(line)
        if start and end:
            is_deleted = True
            start = False
            end = False

        if is_deleted:
            n = 0
            while ((start_index + n) != end_index + 1):
                pop_line = lines.pop(start_index)
                n += 1
            is_deleted = False
            i -= n

        if re.match(pattern_start, line) != None:
            start = True
            start_index = i
        elif re.match(pattern_end, line) != None:
            end = True
            end_index = i
        i += 1
    content = "".join(line for line in lines)
    f.seek(0)
    f.truncate(0)
    f.write(content)
    f.close()
    pass