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
from dla_temp_utils import getTempPath

from docopt import docopt
from sets import Set
import string

class DirectoryListing(object):
    def __init__(self, fileinpath, testpath):
        self.fileinpath = fileinpath 
        self.testpath = testpath 
        self.dicfiles = {}

        self.set_testfiles = None
        self.set_inputfiles = None

        self.__make_dic_from_filein()
        self.__make_test_set()
        self.__make_input_set()

    def files_in_test_but_not_listing(self):
        '''
        Returns a set of file names which are
        in the test set but not in the listing
        '''
        workset = self.set_testfiles.difference((self.set_inputfiles))
        return workset

    def files_in_listing_but_not_test(self):
        '''
        Returns a set of file names which are
        in the listing set but not in the test set 
        '''
        workset = self.set_inputfiles.difference((self.set_testfiles))
        return workset

    def __clean_non_printable(self, the_string):
        '''
        Removes control chars from string
        
        Assumes strings are ASCII
        '''
        return filter(lambda x: x in string.printable, the_string)
        
    def __make_input_set(self):
        '''
        Make a Set object of all the input filenames
        '''
        lstwork = []
        for k in self.dicfiles:
            fname_clean = self.__clean_non_printable(self.dicfiles[k]['filename'])
            lstwork.append(fname_clean)
        self.set_inputfiles = Set(lstwork)
         
    def __make_test_set(self):
        '''
        Make a Set object of all the filenames
        to be tested against
        '''
        lstwork = []
        with open(self.testpath, "rb") as f:
            lines = []
            for line in f:
                #Unix
                if line[-1] == "\n": 
                    line = line[:-1] 
                #Windows has both
                if line[-1] == "\r": 
                    line = line[:-1] 
                lstwork.append(line)


#        for line in lines:
#            fname_clean = self.__clean_non_printable(line)
#            lstwork.append(fname_clean)
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
    
def dump_set_to_file(fname, set):
    lout = []
    with open(fname, 'w') as f:
        for elem in sorted(set):
            f.write(elem + '\n')

def main(filein, filetest, fileout):
    import pprint
    d = DirectoryListing(filein, filetest)
    print "test"
    print(len(d.set_testfiles))
    print "input"
    print(len(d.set_inputfiles))
    s1 = d.files_in_test_but_not_listing()
    s2 = d.files_in_listing_but_not_test()
    print "files_in_test_but_not_listing"
    print(len(s1))
    #pprint.pprint(s1)
    p_s1 = getTempPath("s1.txt")
    dump_set_to_file(p_s1, s1)
    print("*" * 50)
    print "files_in_listing_but_not_test"
    print(len(s2))
    #pprint.pprint(s2)
    p_s2 = getTempPath("s2.txt")
    dump_set_to_file(p_s2, s2)
    print("*" * 50)
    print getTempPath("test1")
    print p_s1
    print p_s2

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Whats Present 0.1')
    main(arguments['-i'], arguments['-t'], arguments['-o'])
