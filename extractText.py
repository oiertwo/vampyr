__author__ = 'oier'

import os
import subprocess
def extractText(path, dest='', params=''):
    '''
    :param path:
    :param params:
    :return:
    '''

    '''
    Usage: java -jar pdfbox-app-x.y.z.jar ExtractText [OPTIONS] <PDF file> [Text File]
                -password  <password>        Password to decrypt document
                -encoding  <output encoding> (ISO-8859-1,UTF-16BE,UTF-16LE,...)
                -console                     Send text to console instead of file
                -html                        Output in HTML format instead of raw text
                -sort                        Sort the text before writing
                -ignoreBeads                 Disables the separation by beads
                -force                       Enables pdfbox to ignore corrupt objects
                -debug                       Enables debug output about the time consumption of every stage
                -startPage <number>          The first page to start extraction(1 based)
                -endPage <number>            The last page to extract(inclusive)
                -nonSeq                      Enables the new non-sequential parser
                <PDF file>                   The PDF document to use
                [Text File]                  The file to write the text to
    '''

    s = "java -jar ./java/extractText.jar"
    if (params != ''):
        s += " " + params
    s += " " + path
    if (dest != ''):
        s += " " + dest
    #os.system(s)
    try:
        subprocess.check_call(s)
    except:
        print("ERROR CALLING JAVA PDF TO TEXT TRANSFORMER")


def multiExtractText(path, dest='', params=''):
    for i in path:
        if (dest != ''):
            extractText(path=path,dest=dest, params=params)
        else :
            extractText(path=path, params=params)

def compile(file, libs = ''):
    pass