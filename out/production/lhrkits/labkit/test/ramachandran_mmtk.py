# Please see accompanying webpage:
# 
# http://www.warwick.ac.uk/go/peter_cock/python/ramachandran/calculate/
#
# This code relies on Konrad Hinsen's Molecular Modelling Toolkit (MMTK):
#
# http://starship.python.net/crew/hinsen/MMTK/index.html
#
# It assumes the input file 1HMP.pdb is in the current directory,
# and generates an output file 1HMP_mmtk.tsv in the current directory.

def next_residue(residue) :
    """Expects an MMTK residue, returns the next residue
    in the chain, or None"""
    #Proteins go N terminal --> C terminal
    #The next reside is bonded to the C of this atom...
    for a in residue.peptide.C.bondedTo():
        if a.parent.parent != residue:
            return a.parent.parent
    return None

def residue_amino(residue) :
    """Expects an MMTK residue, returns the three
    letter amino acid code in upper case"""
    if residue :
        return residue.name[0:3].upper()
    else :
        return None

def residue_ramachandran_type(residue) :
    """Expects an MMTK residue, returns ramachandran 'type'
    (General, Glycine, Proline or Pre-Pro)"""
    if residue_amino(residue)=="GLY" :
        return "Glycine"
    elif residue_amino(residue)=="PRO" :
        return "Proline"
    elif residue_amino(next_residue(residue))=="PRO" :
        #exlcudes those that are Pro or Gly
        return "Pre-Pro"
    else :
        return "General"

import math
def degrees(rad_angle) :
    """Converts any angle in radians to degrees.

    If the input is None, the it returns None.
    For numerical input, the output is mapped to [-180,180]
    """
    if rad_angle is None :
        return None
    angle = rad_angle * 180 / math.pi
    while angle > 180 :
        angle = angle - 360
    while angle < -180 :
        angle = angle + 360
    return angle


pdb_code = "1HMP"

print "About to load MMTK and the PDB file..."
import MMTK.Proteins
protein = MMTK.Proteins.Protein("%s.pdb" % pdb_code, model="no_hydrogens")
print "Done"

print "About to save angles to file..."
output_file = open("%s_mmtk.tsv" % pdb_code,"w")
for chain in protein :
    print chain.name
    for residue in chain :
        phi, psi = residue.phiPsi()
        if phi and psi :
            #Don't write output when missing an angle
            output_file.write("%s:%s:%s\t%f\t%f\t%s\n" \
                % (pdb_code, chain.name, residue.name,
                   degrees(phi), degrees(psi),
                   residue_ramachandran_type(residue)))
output_file.close()
print "Done"
