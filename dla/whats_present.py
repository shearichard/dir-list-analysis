'''
whats_present.py

Given a list of file names provides information about which files are
present and which are absent from within a file listing. There's a good
number of tools out there that will do this as well but in my case I didn't
have access to those.

Usage:
  whats_present.py [-h] -i FILEDIR -o FILEOUT -t FILETEST

Options:
    -h --help    show this
    -i FILEDIR   specify directory listing file 
    -o FILEOUT   specify output file 
    -t FILETEST  specify test file 

'''
from docopt import docopt
from sets import Set

class DirectoryListing(object):
    def __init__(self, fileinpath, testpath):
        self.fileinpath = fileinpath 
        self.testpath = testpath 
        self.dicfiles = {}

        self.set_testfiles = None
        self.set_inputfiles = None
        self.lst_files_in_test_but_not_listing = []
        self.lst_files_in_listing_but_not_test = []

        self.__make_dic_from_filein()
        self.__make_test_set()
        self.__make_input_set()

    def __make_input_set(self):
        '''
        Make a Set object of all the input filenames
        '''
        lstwork = []
        for k in self.dicfiles:
            lstwork.append(self.dicfiles[k]['filename'])
        self.set_inputfiles = Set(lstwork)
         
    def __make_test_set(self):
        '''
        Make a Set object of all the filenames
        to be tested against
        '''
        lstwork = []
        with open(self.testpath, 'r') as f:
            for line in f:
                lstwork.append(line)
        self.set_testfiles = Set(lstwork)

    def __make_dic_from_fileinline(self, line):
        '''
        Given an input line from the file
        add an element to the instance var dict
        which corresponds to one file in the listing
        '''
        lstelems = line.split()
        try:
            mm, dd, yyyy  = lstelems[0].split("/")
        except ValueError:
            #Some lines aren't the format we want
            pass
        except IndexError:
            #Some lines aren't the format we want
            pass
        else:
            #At this stage the line is a goody
            #so make the date usable
            str_dt_iso = "%s-%s-%s" % (yyyy, mm, dd) 
            
            #file names can have spaces (unfortunaly)
            filename = " ".join(lstelems[4:])
            #deal with commas in size
            if lstelems[3] == """<DIR>""":
                pass
            else:
                size = int(lstelems[3].replace(',',''))
                #not sure what to use as key, use file name for now
                key = filename
                
                self.dicfiles[key] = {'filename': filename, 'size': size, 'dateiso' : str_dt_iso} 
        
    def __make_dic_from_filein(self):
        '''
        Based on a file which has at least one line which looks like this:

        12/15/2003  01:15 PM             3,383 000BE98E-7076-4CF8-8BFA-266E6EE4C9DF.GIF

        a dict of dicts is returned, keyed on file name.
        '''
        lstOut = []
        with open(self.fileinpath, 'r') as f:
            for line in f:
                self.__make_dic_from_fileinline(line)
    
def main(filein, filetest, fileout):
    print filein
    print filetest
    print fileout
    d = DirectoryListing(filein, filetest)
    import pprint
    pprint.pprint(d.dicfiles)
    print len(d.dicfiles)
    print filein
    print d.set_testfiles
    print d.set_inputfiles

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Whats Present 0.1')
    import sys
    print sys.argv[1]
    print sys.argv[2]
    print(arguments)
    main(arguments['-i'], arguments['-t'], arguments['-o'])
