#!/usr/bin/python
# -*- coding: utf-8 -*-

def humanize(size):
    output = float(size)
    keys = [' ', 'K', 'M', 'G', 'T']
    for suffix in keys:
        if float(size) / pow(1024, keys.index(suffix)) > 1.0:
            output = float(size) / pow(1024, keys.index(suffix))
        else:
            break
    if len('%.1f%s' % (output, suffix)) <= 4:
        return '%.1f%s' % (output, suffix)
    else:
        return '%3.0f%s' % (output, suffix)

def dir_usage(directory):
    import subprocess
    proc = subprocess.Popen(('du -s %s/*' % directory), shell=True,
                            stdout=subprocess.PIPE)

    entries = []
    for entry in proc.stdout.readlines():
        size, file_name = entry.rstrip().split('\t')
        entries.append({'file_name': file_name, 'size': int(size)})

    return sorted(entries, key=lambda x: x['size'], reverse=True)

if __name__ == '__main__':
    import sys, os, glob

    # dir = curdir or argv[1]
    if len(sys.argv) == 2:
        directory = sys.argv[1]
    elif len(sys.argv) > 2:
        usage()
        sys.exit(os.EX_USAGE)
    else:
        directory = os.path.abspath(os.curdir)

    colors = {}
    # Get LS_COLORS
    for instruction in os.environ['LS_COLORS'].split(':'):
        if instruction == '':
            break
        key, value = list(instruction.split('='))
        colors[key] = value

    # while True:
    while True:
        # do_work(dir)
        entries = dir_usage(directory)
        for entry in entries[0:20]:
            op_file_name = '\033[0m%s' % entry['file_name']
            if os.path.isdir(entry['file_name']):
                op_file_name = '\033[%sm%s\033[0m' % (colors['di'],
                                                      entry['file_name'])
            if os.path.islink(entry['file_name']):
                op_file_name = '\033[%sm%s\033[0m' % (colors['ln'],
                                                      entry['file_name'])
            if os.path.isfile(entry['file_name']):
                op_file_name = '\033[%sm%s\033[0m' % (colors['rs'],
                                                      entry['file_name'])
            for pattern in colors:
                if glob.fnmatch.fnmatch(entry['file_name'], pattern):
                    op_file_name = '\033[%sm%s\033[0m' % (colors[pattern],
                                                   entry['file_name'])
                    break
            print '%2d: %s\t%s' % (entries.index(entry) + 1,
                                   humanize(entry['size']), op_file_name)

        # read reply
        reply = ''
        while True:
            reply = raw_input("\nWhich directory would you like to enter? "
                              "('..' to go up one level): ").rstrip()
            if reply == '..':
                # Up one level
                break
            if reply.isdigit():
                reply = int(reply) - 1
            if reply >= 0 and reply < len(entries):
                # Into a directory in the list
                break
            # Enhancement: reply == relative path
            # Enhancement: reply == absolute path

        # dir = ...
        if reply == '..':
            directory = os.path.dirname(directory)
        elif type(reply) == int:
            directory = entries[reply]['file_name']
