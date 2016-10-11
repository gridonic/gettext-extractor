import re
import sys
import hashlib
import os
import codecs

print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))

basePath = os.getcwd() + '/'
# Should basePath above not work, you can also use an absolute path:
# basePath = '/absolute-path-to-project/wp-content/themes/your-theme/'

fileNames = []
outputFileName = None
index = 0
for argument in sys.argv:
    if argument == '-o' and index + 1 < len(sys.argv):
        outputFileName = sys.argv[index + 1]
    index += 1

filesArgumentFound = False
for argument in sys.argv:
    if filesArgumentFound and not argument in fileNames:
        fileNames.append(argument)
    if argument == '--files':
        filesArgumentFound = True
    index += 1

print('Base path: ' + basePath)
print('Output file: ' + outputFileName)
print('Input Files:')
for fileName in fileNames:
    print(fileName)

translationMap = {}

for fileName in fileNames:
    with codecs.open(basePath + fileName, 'r', encoding='utf8') as inputFile:
        lineNumber = 1
        for line in inputFile:
            matches = re.findall( r"(?:__|_e|trans)\(('|\")(.*?)(\1)(?:\w*?)(?:,|\))", line, re.MULTILINE)
            if len(matches) > 0:
                for match in matches:
                    text = match[1]
                    textHash = re.sub('[^a-zA-Z0-9\n\.]', '', text)
                    if not textHash in translationMap:
                        translationMap[textHash] = [text.replace("\\'", "'"), fileName + "{:10}".format(lineNumber)]
                        translationMap[textHash].append('');

                    translationMap[textHash].append(fileName + ':' + str(lineNumber))

            contextualMatches = re.findall( r"(?:_x|transX)\(('|\")(.*?)(\1)(?:\w*?)(?:,)(?:\s*?)(?:')(\w*?)(?:')(?:,|\))", line, re.MULTILINE)
            if len(contextualMatches) > 0:
                for match in contextualMatches:
                    text = match[1]
                    comment = match[3]
                    textHash = re.sub('[^a-zA-Z0-9\n\.]', '', '' + text + comment)
                    if not textHash in translationMap:
                        translationMap[textHash] = [text.replace("\\'", "'"), fileName + "{:10}".format(lineNumber)]
                        translationMap[textHash].append(comment);

                    translationMap[textHash].append(fileName + ':' + str(lineNumber))

            lineNumber += 1

    with codecs.open(outputFileName, 'w', encoding='utf8') as outputFile:

        for item in sorted(translationMap.items(), key=lambda e: e[1][1]):
            values = item[1]
            for occurence in values[3:]:
                outputFile.write('#: ' + occurence + '\n')

            if values[2]:
                outputFile.write('msgctxt "' + re.sub('"', '\\"', values[2]) + '"\n')

            outputFile.write('msgid "' + re.sub('"', '\\"', values[0]) + '"\n')
            outputFile.write('msgstr ""\n\n')
