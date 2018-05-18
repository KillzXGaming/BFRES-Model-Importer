import os, sys, argparse
from BFRES_Vertex import readCSV, readBFRES

if len (sys.argv) < 3 :
    print('Usage: BFRES_Vertex.py "BFRES file" "CSV file"')	
    sys.exit (1)

parser = argparse.ArgumentParser()
parser.add_argument("bfres", metavar="bfresfile", type=str, help=".bfres file to edit")
parser.add_argument("csv", metavar="csvfile", type=str, help=".csv file to inject into bfres")
parser.add_argument('-f','--indexfmdl',type=int, help='Specify the model to inject into', required=False)
args = parser.parse_args()

cvsIn = open(sys.argv[2], "r")

f = open(sys.argv[1], "rb+") 

readCSV(cvsIn)
readBFRES(f, args.indexfmdl)