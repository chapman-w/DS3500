import gadapi as api



def main():
    # ititialize the API
    gadapi = api.GADAPI()
    gadapi.loan_gad('gad.csv')

    # search parameters
    phenotype = 'asthma'
    num_pub = 3

    # filter gad data to build dataframe for my Sankey vis
    local = gadapi.extract_local_network(phenotype, num_pub)
    print(local)

    # Generate our sankey diagram
    sk.show_sankey(local, 'phenotype', 'gene', vals='npubs')