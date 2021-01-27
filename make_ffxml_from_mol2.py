#!/usr/bin/env python2

# this file is part of the github repository: https://github.com/nwhoppe/nanobody_fitness
# author: nwhoppe
# created: 11/29/20
import argparse
import parmed as pmd


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""run phenix.elbow to get input files""")
    required = parser.add_argument_group('required')
    required.add_argument('-m', '--mol2', required=True)
    required.add_argument('-f', '--frcmod', required=True)
    args = parser.parse_args()

    # Load the Amber FF
    ff = pmd.openmm.OpenMMParameterSet.from_parameterset(
        pmd.amber.AmberParameterSet(args.frcmod)
    )

    # Load mol2 files
    mol2 = pmd.load_file(args.mol2)

    # If there are multiple residue definitions, mol2 will be a pmd.modeller.ResidueTemplateContainer
    # Otherwise it will be a pmd.modeller.ResidueTemplate
    if isinstance(mol2, pmd.modeller.ResidueTemplateContainer):
        ff.residues = mol2.to_library()
    else:
        ff.residues[mol2.name] = mol2

    # Now you can write the FF XML file
    ff.write('APG.xml')