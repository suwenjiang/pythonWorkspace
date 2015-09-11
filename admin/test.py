import argparse
import os
import sys
parser = argparse.ArgumentParser()

parser.add_argument("p",help="input directory or path of log file ",action="store")
parser.add_argument("-c",'--complete',metavar='',help="completely output format")

parser.add_argument("-l","--log",help="use msgType[warning,info,fine,verbose,severe,debug] to filter the log",\
                    choices=["w","i","f","v","s","d"],action="store")
parser.add_argument("-m","--machine",metavar='',help="machine name",action="store")
parser.add_argument("-t","--time",metavar='',help="time to filter log",action="store")




args=parser.parse_args()
print args.p
if not os.path.isfile(args.p) and not os.path.isdir(args.p):
    print "please input a valid directory or .log file"
    sys.exit()


if args.log:
    if not args.log in ['w','i','f','v','s','d']:
        print "please choose a value from ['w','i','f','v','s','d']"
        sys .exit()
    else:
        print "do something"


