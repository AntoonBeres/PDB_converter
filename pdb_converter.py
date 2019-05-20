#!/usr/bin/python

#==========================================================================
# PDB to .xyz and.gjf converter
# Converts PDB files to .xyz and .gjf files, other destination file formats
# might be added later
#
#==========================================================================
# Part of source code taken from packmoltools/resolvate.py created by:
# John Chodera, Stanford University, 2007-03-05
#==========================================================================
# AUTHORS:
#
# Written by Antoon Beres, University of Antwerp, 20/05/2019
#==========================================================================
# TO DO:
# - Add support for other export file formats
# - Add usage() function for printing help
#==========================================================================
# Syntax:
# -convert .pdb to .xyz:
#   pdb_converter.py <in.pdb> <out.xyz>
# -convert .pdb to .gjf:
#   pdb_converter.py <in.pdb> <out.gjf>  !Tune the parameters for gjf first
#==========================================================================

import os
import sys

def readPDB(file, chain=' '):
    pdbfile = open(file)
    lines = pdbfile.readlines()
    pdbfile.close()

    sequence = []
    last_resSeq = None
    for line in lines:
        if line[0:5] == "ATOM ":
            field = {}
            field["serial"] = int(line[6:11])
            field["name"] = line[12:16]
            field["altLoc"] = line[16:17]
            field["resName"] = line[17:20]
            field["chainID"] = line[21:22]
            field["resSeq"] = int(line[22:26])
            field["iCode"] = line[26:27]
            field["coords"] = []
            coordsval = (line[33:55].split(' '))
            for i in coordsval:
                try:
                    field["coords"].append(float(i))
                except:
                    continue
            field["atomtype"] = (line[76:78]).lstrip()
            sequence.append(field)
    return sequence

def genXYZ(pdbdata):
    xyzFile = open("%s" % (sys.argv[2]), 'w')
    xyzFile.write('%s\n' % str(len(pdbdata)))
    xyzFile.write('Molecule Name\n')
    for i in pdbdata:
        xyzFile.write('%s ' % (i["atomtype"]))
        for coord in i["coords"]:
            xyzFile.write('%s ' % str(coord))
        xyzFile.write('\n')
    xyzFile.close()

def gengjf(pdbdata):

    #MODIFY THESE TO YOUR NEEDS!
#===============================================================================
    gjfFile = open("%s" % (sys.argv[2]), 'w')
    gjfFile.write('%chk=test.chk\n')
    gjfFile.write('%mem=48GB\n')
    gjfFile.write('%nprocshared=20\n')
    gjfFile.write('#P B3LYP/6-31G* freq EmpiricalDispersion=GD3BJ\n')
    gjfFile.write('\n')
    gjfFile.write('GJF TITLE HEADER')
    gjfFile.write('\n')
    gjfFile.write(' 0 1\n')
#===============================================================================
    for atom in pdbdata:
        gjfFile.write(atom["atomtype"])
        if len(atom["atomtype"]) == 1:
            gjfFile.write("      ")
        elif len(atom["atomtype"]) == 2:
            gjfFile.write("     ")
        gjfFile.write("0    ")
        for coord in atom["coords"]:
            if coord < 0:
                gjfFile.write('%s' % str(format(coord, '.6f')))
            elif coord >= 0:
                gjfFile.write(' %s' % str(format(coord, '.6f')))
            gjfFile.write("   ")
        gjfFile.write("\n")
    gjfFile.close()

def usage():
    print('Syntax:')
    print('pdb_converter.py <in.pdb> <out.*> (replace <in.pdb> and <out.*> with correct filenames)')
    print('examples:')
    print('convert .pdb to .xyz:')
    print('pdb_converter.py <in.pdb> <out.xyz>')
    print('convert .pdb to .gjf:')
    print('pdb_converter.py <in.pdb> <out.gjf>')


Pdbfile = sys.argv[1]
data = readPDB(Pdbfile)

if sys.argv[2].endswith('.gjf'):
    gengjf(data)
elif sys.argv[2].endswith('.xyz'):
    genXYZ(data)
else:
    print('ERROR, UNSUPPORTED EXPORT TYPE')
    print('')
    #usage()
