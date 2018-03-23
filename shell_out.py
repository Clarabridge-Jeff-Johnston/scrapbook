#!/usr/bin/env python

import os, sys
import shlex
import subprocess

def shell_out(cmd, stdin=None, verbose=False):
    """
    Execute an external command.
    """
    args = shlex.split(cmd)
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    out, err = proc.communicate(stdin)
    exitcode = proc.returncode
    out_err = out.splitlines() + err.splitlines()
    if verbose == True: # prints results
        print("# CMD=\"%s\"\n# RC=\"%s\"" % (cmd, exitcode))
        for line in (out_err):
            print("# ~> %s" % (line.decode('utf-8')))
    return({"rc": exitcode, "out": out, "err": err})

if __name__ == '__main__':
    cmd1 = shell_out("uname -s", verbose=False)
    print("\nPiping output of last command (run silently) into the next...\n")
    cmd2 = shell_out("figlet", stdin=cmd1['out'], verbose=True)
    cmd3_script = '\n'.join([
        'for i in {1..9}; do',
        'echo $i',
        'done'
        ]).encode('utf-8')
    print("\ninput to bash:\n%s\n" % (cmd3_script.decode('utf-8')))
    cmd3 = shell_out("bash", stdin=cmd3_script, verbose=True)
