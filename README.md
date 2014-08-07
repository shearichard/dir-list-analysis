dir-list-analysis
=================

Various tools for analysing directory file listings

whats_present
=======
Given a list of file names provides information about which files are
present and which are absent from within a file listing. There's a good
number of tools out there that will do this as well but in my case I didn't
have access to those.

dir_size
=======
Given a windows file directory listing provides some analysis of which
directories use how much space. Essentially windirstat when all you can
get from the users is a directory listing

*The core processing works but some code was written a long time ago is not very PEP-8ish
and there's lots of hard-coded paths which need to got rid of and replaced with some 
command line args/config file supplied values*

