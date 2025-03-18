
import pandas as pd
import sankey as sk

class GADAPI:

    def load_gad(self, filename):
        self.gad = pd.read_csv(filename) # our dataframe (database) - STATE VARIABLE
                                          # Lives as long as the object lives


    def get_phenotypes(self):
        gady = self.gad[self.gad.association == 'Y']
        gady.phenotype = gady.phenotype.str.lower()
        phen = gady.phenotype.unique()
        phen = [str(p) for p in phen if ";" not in str(p)]
        return sorted(phen)

    def extract_local_network(self, phenotype, min_pub):

        # filter for POSITIVE ('Y') associations only
        gad = self.gad[self.gad.association == 'Y']

        # filter columns
        gad = gad[['phenotype', 'gene']]

        # convert phenotype to lower case
        gad.phenotype = gad.phenotype.str.lower()

        # count publications for each phenotype/gene combination
        gad = gad.groupby(['phenotype', 'gene']).size().reset_index(name='npubs')

        # sort data (for fun)
        gad.sort_values('npubs', ascending=False, inplace=True)

        # discard associations with less than <min_pub> publications
        gad = gad[gad.npubs >= min_pub]

        # genes for the phenotype of interst
        gad_pheno = gad[gad.phenotype == phenotype]

        # Find all gad associations involving the phenotype-linked genes
        local = gad[gad.gene.isin(gad_pheno.gene)]

        return local

def main():

    # Initialize the API
    gadapi = GADAPI()
    gadapi.load_gad("gad.csv")


    # search parameters
    phenotype = 'asthma'
    num_pub = 3

    # filter gad data to build the dataframe for my sankey viz
    local = gadapi.extract_local_network(phenotype, num_pub)
    print(local)

    # Generate manually our sankey diagram
    sk.show_sankey(local, 'phenotype', 'gene', vals='npubs')


if __name__ == '__main__':
    main()

