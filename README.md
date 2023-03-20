**Privileged Executable File Auditing**
-------------------------------------------------------------------------------

0. Description

In this assignment you will develop an auditing tool that searches for
privileged setuid executables and executables with capabilities on a Linux
system. Your program, called "findpriv", will scan all files on the system (or
in the supplied directory), identify all executables, and report:

1) The number of files scanned, and the number of executables found.
2) The list of executables (name and full path) that have the setuid bit set.
3) The list of executables (name and full path) with capabilities, along
   with the specific capabilities each of them has been granted with.

Your program should conform to the following specification:

findpriv [-s] [-c] [-p path]

-s  Search for setuid executables.
-c  Search for executables with capabilities.
-p  Search only in the directory specified by 'path'.

If no command-line option is provided, findpriv should search the entire
system for both setuid executables and executables with capabilities.

As an example, the following invocation of findpriv will search only for
executables with capabilities in the directory /usr/bin:

findpriv -c -p /usr/bin

1. Hints

To determine if a file is an executable, you can check its permissions. For
debugging purposes, you can observe the output of "ls -l" and see if a file
has the 'x' permission, which indicates that it is an executable. Similarly,
's' indicates that the setuid bit is set. In addition to "ls", you can also
use the "find" utility.

In your code, you can programmatically check for the 'x' and 's' permissions
using the Python "os" module (see the functions "os.stat" and "os.access").

To view the capabilities of an executable file, you can use the "getcap"
command. Because Python does not provide an easy way to get a file's
capabilities, you can use the "subprocess.Popen" function to run "getcap" on
each executable and parse its output.

Some useful resources:
https://man7.org/linux/man-pages/man1/ls.1p.html
https://man7.org/linux/man-pages/man7/capabilities.7.html
https://man7.org/linux/man-pages/man8/getcap.8.html
https://en.wikipedia.org/wiki/Setuid
https://docs.python.org/3/library/os.html
https://docs.python.org/3/library/argparse.html

2. Example Output

$ findpriv -p /usr/bin
Scanned 2173 files, found 2173 executables
setuid executables:
/usr/bin/chfn
/usr/bin/gpasswd
/usr/bin/mount
/usr/bin/passwd
/usr/bin/pkexec
/usr/bin/su
/usr/bin/sudo
capability-aware executables:
/usr/bin/dumpcap  cap_net_admin, cap_net_raw
/usr/bin/fping    cap_net_raw
/usr/bin/ping     cap_net_raw
