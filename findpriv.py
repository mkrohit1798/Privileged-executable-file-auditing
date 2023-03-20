#!/usr/bin/env python3

import os
import sys
import stat
import argparse

def is_executable(filepath):
    # Check if a file is an executable by checking its permission

    if os.path.isfile(filepath):
        mode = os.stat(filepath).st_mode
        return stat.S_ISREG(mode) and (mode & stat.S_IXUSR)

def findpriv(path, search_setuid, search_capabilities):
    
    #Find executables with setuid or capabilities in the given path

    setuid_executables = []
    capability_executables = []
    count_files = 0
    count_executables = 0

    for root, dirs, files in os.walk(path):
        for file in files:
            filepath = os.path.join(root, file)
            count_files += 1
            if is_executable(filepath):
                count_executables += 1
                if search_setuid and os.stat(filepath).st_mode & stat.S_ISUID:
                    setuid_executables.append(filepath)
                if search_capabilities:
                    if os.popen("getcap {}".format(filepath)).read():
                        capability_executables.append(filepath)
    return setuid_executables, capability_executables, count_files, count_executables

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", help="Path to search for executables")
    parser.add_argument("-s", "--setuid", help="Search for setuid executables", action="store_true")
    parser.add_argument("-c", "--capabilities", help="Search for capability executables", action="store_true")
    args = parser.parse_args()

    path = args.path if args.path else '/'
    search_setuid = args.setuid
    search_capabilities = args.capabilities

    setuid_executables, capability_executables, count_files, count_executables = findpriv(path, search_setuid, search_capabilities)

    print("\nNumber of files scanned:", count_files)
    print("Number of executables found:", count_executables)

    if not search_setuid and not search_capabilities:
        setuid_execs = []
        cap_execs = []
        for root, dirs, files in os.walk(path):
            for file in files:
                filepath = os.path.join(root, file)
                count_files += 1
                if is_executable(filepath):
                    count_executables += 1
                    if os.stat(filepath).st_mode & stat.S_ISUID:
                        setuid_execs.append(filepath)
                    if os.popen("getcap {}".format(filepath)).read():
                        cap_execs.append(filepath)
        
        print("\nSetuid executables in entire system: ")
        for file in setuid_execs:
            print(file)
        
        print("\nCapability executables in entire system: ")
        for file in cap_execs:
            print(file)
    
    else:

        if search_setuid:
            print("\nSetuid executables:")
            for file in setuid_executables:
                print(file)
    

        if search_capabilities:
            print("\nCapability executables:")
            for file in capability_executables:
                print(file)
    

    

if __name__ == "__main__":
    main()
