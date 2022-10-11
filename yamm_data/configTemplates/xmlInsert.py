
with open(fileOld, 'r') as file :
    filedata = file.read()

filedata = filedata.replace(toReplace, repWord)

with open(fileNew, 'w') as file:
    file.write(filedata)