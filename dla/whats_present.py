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


def main(filein, filetest, fileout):
    print filein
    print filetest
    print fileout

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Whats Present 0.1')
    import sys
    print sys.argv[1]
    print sys.argv[2]
    print(arguments)
    main(arguments['-i'], arguments['-t'], arguments['-o'])
