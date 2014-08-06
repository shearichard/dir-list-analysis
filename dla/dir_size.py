'''
dir_size.py 

Given a windows file directory listing provides some analysis of which
directories use how much space. Essentially windirstat when all you can
get from the users is a directory listing
'''
import re
import csv
#
INPUTFILELOCATION = "C:/usr/rshea/data/src/Python/DirAnalysis/F_Drive_Dir_Dump.txt"
#
def findSizeRegexSupportObj():
    rawstr = r"""^\s+(?P<FileCount>\d+)\sFile\(s\)\s+(?P<Bytes>[-,0-9]+)"""
    embedded_rawstr = r"""^\s+(?P<FileCount>\d+)\sFile\(s\)\s+(?P<Bytes>[-,0-9]+)"""

    compile_obj = re.compile(rawstr)
    return compile_obj
    match_obj = compile_obj.search(matchstr)


def findDirPathBuildRegexSupportObj():
    rawstr = r"""^\s+(?P<Preamble>Directory of\s)(?P<Path>\S+)"""
    embedded_rawstr = r"""^\s+(?P<Preamble>Directory of\s)(?P<Path>\S+)"""
    compile_obj = re.compile(rawstr)
    return compile_obj
    
#
def findDirPath(path_Rgx_Obj, candidateLine):
    
    match_obj = path_Rgx_Obj.search(candidateLine)
    if match_obj != None:
        Preamble = match_obj.group('Preamble')
        Path = match_obj.group('Path')
        return True
    else:
        return False


def getDirDumpAsListOfLines():
    lstOut = []
    with open(INPUTFILELOCATION, 'r') as f:
        for line in f:
            lstOut.append(line)
    return lstOut
        
def buildDicDir(lstLines, path_Rgx_Obj, size_Rgx_Obj, blnSkipZeroSizeDirectories):
   
    dicDir = {}
    blnProcessingDirectory = False
    strCurrentDirectory = None
    idx = -1
    for candidateLine in lstLines:
        idx += 1
        path_MatchObj = path_Rgx_Obj.search(candidateLine)
        #Is current line a 'Path' line ?
        if path_MatchObj == None:
            #No ... is it a 'Size' line ?
            size_MatchObj = size_Rgx_Obj.search(candidateLine)
            if size_MatchObj == None:
                #No ... move onto next line in input 
                pass
            else:
                #Yes ... store the size etc against the path in the output dictionary 
                if blnProcessingDirectory == True:
                    iSize = int(size_MatchObj.group('Bytes').replace(',',''))
                    iFileCount = int(size_MatchObj.group('FileCount').replace(',',''))
                    if ((blnSkipZeroSizeDirectories == True) and (iSize == 0)):
                        pass
                    else:
                        dicDir[CurrentDirectory] = {'FileCount': iFileCount, 'Bytes': iSize}
                    blnProcessingDirectory = False
                else:
                    if candidateLine.find('Total Files Listed:'):
                        print "Processed all of Input successfully"
                        exit
                    else:
                        print "Encountered Size Before Path - Fatal Error %d" % (idx) 
                        exit
        else:
            #We've found a 'Path' line which looks like this
            #      Directory of F:\_report
            #
            #Store the path into a local variable until we find
            #the size
            if blnProcessingDirectory == False:
                CurrentDirectory = path_MatchObj.group('Path')
                blnProcessingDirectory = True
            else:
                print "Encountered Path Before Size - Fatal Error %d" % (idx)
                exit

    return dicDir
    '''
        
    sampleDirectoryString = """ Directory of F:\9c00d1fe3766bfc2333a2867ea\amd64"""
    findDirPath(path_Rgx_Obj, sampleDirectoryString)
    sampleDirectoryString = """Mary has a 999 little lamb 12/1/09"""
    findDirPath(compile_obj, sampleDirectoryString)
    matchstr = """              18 File(s)        6 bytes"""
    
    print len(lstLines)
                '''
 
def analyseDirectories(dicDir, numberOfResults):
    dicWork = {}
    MaxInDicCurrently = -1
    MinInDicCurrently =  999999999999  
    for k,v in dicDir.iteritems():
        if len(dicWork.items()) <= numberOfResults:
            dicWork[k] = v 
            if v['Bytes'] > MaxInDicCurrently:
                MaxInDicCurrently = v['Bytes']
            if v['Bytes'] < MinInDicCurrently:
                MinInDicCurrently = v['Bytes']
        else:
            if v['Bytes'] > MinInDicCurrently:
                keyToDelete = None
                for kWork,vWork in dicWork.iteritems():
                    if dicWork[kWork]['Bytes'] == MinInDicCurrently:
                        keyToDelete = kWork
                        break
                del dicWork[keyToDelete]
                dicWork[k] = v
                MinInDicCurrently =  999999999999  
                for kWork,vWork in dicWork.iteritems():
                    if vWork['Bytes'] > MaxInDicCurrently:
                        MaxInDicCurrently = vWork['Bytes']
                    if vWork['Bytes'] < MinInDicCurrently:
                        MinInDicCurrently = vWork['Bytes']
                        
    return dicWork
                
                
                        
                    
            
    
def humanizeBytes(bytes):
    bytes = float(bytes)
    if bytes >= 1099511627776:
        terabytes = bytes / 1099511627776
        size = '%.2fT' % terabytes
    elif bytes >= 1073741824:
        gigabytes = bytes / 1073741824
        size = '%.2fG' % gigabytes
    elif bytes >= 1048576:
        megabytes = bytes / 1048576
        size = '%.2fM' % megabytes
    elif bytes >= 1024:
        kilobytes = bytes / 1024
        size = '%.2fK' % kilobytes
    else:
        size = '%.2fb' % bytes
    return size
def reportProblems(dicProblemDirs):
    from operator import itemgetter
    items = dicProblemDirs.items()
    items.sort(key = itemgetter(1), reverse=True)
    with open('C:\\usr\\rshea\\data\\src\\Python\\DirAnalysis\\MSD-UAT-Fdrive-Analysis.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(["Dir Size (Friendly)", "Dir Size (Raw Bytes)", "Path to Dir"])
        for ll in items:
            print "%10s                        %s" % (humanizeBytes(ll[1]['Bytes']), ll[0])
            writer.writerow([humanizeBytes(ll[1]['Bytes']), ll[1]['Bytes'], ll[0]])
    
    print "*" * 50
    '''
    items.sort(key = itemgetter(2))
    for ll in items:
        print ll
        '''
    for k,v in dicProblemDirs.iteritems():
        print "%10s                        %s" % (humanizeBytes(v['Bytes']), k)
        
def main():
    path_Rgx_Obj = findDirPathBuildRegexSupportObj()
    size_Rgx_Obj = findSizeRegexSupportObj()
    
    lstLines = getDirDumpAsListOfLines()
    print "About to start the heavy lifting"
    dicDir = buildDicDir(lstLines, path_Rgx_Obj, size_Rgx_Obj, True)
    dicProblemDirs = analyseDirectories(dicDir, 20)
    reportProblems(dicProblemDirs)
    print "All done now"
    
    
if __name__ == "__main__":
    main()
