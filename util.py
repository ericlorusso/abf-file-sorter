import os
import sys



# take a filename (not path) and return it without the extension, if it has one.
def removeFileExtension(fileName):
    end = len(fileName) - 1
    while(fileName[end] != '.' and end != 0):
        end -= 1
    if(end != 0):
        return fileName[:end]
    if(fileName[end] == '.'):
        # we're at the begining character and it's a ., meaning it's a file like .gitignore
        return ''
    # this fileName doesn't even have an extension
    return fileName

# take any path, relative or absolute, and return the fileName
def getFileNameFromPath(path):
    start = len(path) - 1
    while((path[start] != '/' and path[start] != '\\') and start != 0):
        start -= 1
    if(path[start] == '/' or path[start] == '\\'):
        start += 1
    return path[start:]

# take a path and return the filename without the extension
def getRootFileNameFromPath(path):
    return removeFileExtension(getFileNameFromPath(path))


def ensureEndSlash(path):
    if(path[-1] == '/' or path[-1] == '\\'):
        return path
    return path + '/'

def getParentDir(path):
    slashes = set(['/','\\'])
    if(path[-1] in slashes):
        path = path[:-1]
    i = len(path) - 1
    while (path[i] not in slashes) and i != -1:
        i -= 1
    #either pointing to end slash, or -1
    if path[i] in slashes:
        path = path[:i]
    return path


def resetDir(path):
    #case 1: path does not exist. make it if you can, or return an error.
    if(os.path.exists(path) == False):
        stack = []
        parentDir = path
        while(os.path.exists(parentDir) == False):
            stack.append(parentDir)
            parentDir = getParentDir(parentDir)
        while(len(stack) != 0):
            #you can make this folder now
            os.mkdir(stack.pop())

    #case 2: the directory exists, and you need to purge it.
    purgeDir(path)



#recursively delete an entire folder hierarcy, except for the root folder
def purgeDir(path):
    files = os.listdir(path)
    for File in files:
        filepath = os.path.join(path,File)
        if(os.path.isfile(filepath)):
            if(os.path.splitext(path)[1] != '.gitignore'):
                os.remove(filepath)
        else:
           purgeDir(filepath)
           os.rmdir(filepath)



# this is the same as processHierarhcy, but no outputs files are generated.
def directory_walk(payload_dir, file_function, *args):
    files = os.listdir(payload_dir)
    for File in files:
        file_path = os.path.join(payload_dir, File)
        if os.path.isfile(file_path):
            file_function(payload_dir, File, *args)
        else:
            directory_walk(file_path, file_function, *args)


# this is the same as processHierarhcy, but no outputs files are generated.
def directory_walk_and_clone(payload_dir, target_dir, file_function, *args):
    files = os.listdir(payload_dir)
    for File in files:
        file_path = os.path.join(payload_dir, File)
        if os.path.isfile(file_path):
            file_function(payload_dir, File, *args)
        else:
	    output_sub_dir_path = os.mkdir(os.path.join(target_dir, File))
            directory_walk(file_path, output_sub_dir_path, file_function, *args)





