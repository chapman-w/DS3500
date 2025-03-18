import pandas as pd
import sankey as sk


def extract_local_network(gad, phenotype, min_pub):
    '''
    :param gad: gad data
    :param phenotype: phenotype of interest
    :param min_pub: minimum number of publications confirming a link to a gene
    :return: A new dataframe with the relevant disease-gene links --> sankey diagram with columns

    '''


    # filter for POSITIVE ('Y') associations only
    gad = gad[gad.association == 'Y']

    gad = gad[['phenotype', 'gene']]

    gad.phenotype = gad.phenotype.str.lower()

    gad = gad.groupby(['phenotype', 'gene']).size().reset_index(name='npubs')

    gad.sort_values('npubs', ascending=False, inplace=True)

    # discard associations with less than <min_pub> publications
    gad = gad[gad.npubs >= min_pub]

    gad_pheno = gad[gad.phenotype == phenotype]

    local = gad[gad.gene.isin(gad_pheno.gene)]

    return local



def main():

    # read gad data
    gad = pd.read_csv('../sankey/data/gad.csv')


    # search parameters
    phenotype = 'asthma'
    num_pub = 3

    # filter gad data to build dataframe for my Sankey vis
    local = extract_local_network(gad, phenotype, num_pub)
    print(local)

    # Generate our sankey diagram
    sk.show_sankey(local, 'phenotype', 'gene', 'npubs')




main()