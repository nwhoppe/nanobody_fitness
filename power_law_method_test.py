#!/usr/bin/env python

# this file is part of the github repository: https://github.com/nwhoppe/nanobody_fitness
# author: nwhoppe
# created: 7/30/20

# Import a model and the plotting module
from gpmap import GenotypePhenotypeMap
from epistasis.models import EpistasisLinearRegression
from epistasis.pyplot import plot_coefs


# Genotype-phenotype map data.
wildtype = "0000"
wt_fi = 59.6
phenotypes_fi = [
    49.98591467200834,
    62.86717596864121,
    200.31146722138152,
    52.859114141993615,
    3.9272299397015185,
    7.043580721395412,
    6.631891390245911,
    5.118042141899316,
    91.06930781910255,
    75.80024094525044,
    13.702849418169393,
    102.60157756124704,
    44.08228493673587,
    25.938853861679835,
    10.837063200544316,
]

phenotypes = [x / wt_fi for x in phenotypes_fi]

genotypes = [
    "1010",
    "1001",
    "1011",
    "1000",
    "0110",
    "0101",
    "0111",
    "0100",
    "1110",
    "1101",
    "1111",
    "1100",
    "0010",
    "0001",
    "0011",
]
print('here')
# Create genotype-phenotype map object.
gpm = GenotypePhenotypeMap(wildtype=wildtype,
                           genotypes=genotypes,
                           phenotypes=phenotypes)
print(gpm)
# Initialize an epistasis model.
model = EpistasisLinearRegression(order=3)
print(model)
# Add the genotype phenotype map.
model.add_gpm(gpm)

# Fit model to given genotype-phenotype map.
model.fit()
print(model)
# Plot coefficients (powered by matplotlib).
plot_coefs(model, figsize=(3, 5))
