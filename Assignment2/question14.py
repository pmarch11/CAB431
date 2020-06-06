document_vectors  = {
              '39496': {'VM': 0.17, 'US': 0.01, 'Spy': 0.20, 'Sale': 0.00, 'Man': 0.02, 'GM': 0.20, 
                              'Espionag': 0.12, 'Econom': 0.11, 'Chief': 0.00, 'Bill': 0.00}, 
             '46547': {'VM': 0.10, 'US': 0.21, 'Spy': 0.10, 'Sale': 0.00, 'Man': 0.00, 'GM': 0.00, 
                            'Espionag': 0.22, 'Econom': 0.20, 'Chief': 0.00, 'Bill': 0.10},
              '46974': {'VM': 0.00, 'US': 0.23, 'Spy': 0.10, 'Sale': 0.20, 'Man': 0.05, 'GM': 0.10, 
                             'Espionag': 0.10, 'Econom': 0.10, 'Chief': 0.01, 'Bill': 0.00}, 
              '62325': {'VM': 0.17, 'US': 0.01, 'Spy': 0.20, 'Sale': 0.00, 'Man': 0.02, 'GM': 0.20, 
                             'Espionag': 0.12, 'Econom': 0.11, 'Chief': 0.00, 'Bill': 0.00}, 
              '6146':  {'VM': 0.10, 'US': 0.00, 'Spy': 0.00, 'Sale': 0.30, 'Man': 0.10, 'GM': 0.20, 
                             'Espionag': 0.00, 'Econom': 0.12, 'Chief': 0.10, 'Bill': 0.00}, 
              '18586': {'VM': 0.00, 'US': 0.30, 'Spy': 0.00, 'Sale': 0.30, 'Man': 0.20, 'GM': 0.00, 
                             'Espionag': 0.00, 'Econom': 0.20, 'Chief': 0.15, 'Bill': 0.20}, 
               '22170': {'VM': 0.20, 'US': 0.00, 'Spy': 0.00, 'Sale': 0.15, 'Man': 0.20, 'GM': 0.25, 
                             'Espionag': 0.00, 'Econom': 0.00, 'Chief': 0.00, 'Bill': 0.10} 
                    }
relevance_judgements = {'R101': {'0': ['6146', '18586', '22170'], '1': ['39496', '46547', '46974', '62325']}}

def train_Rocchio(document_vectors, relevance_judgements, given_topic):
    # Returns: centroid of relevant class
    for c in relevance_judgements:
        var d = #...
    return #...
    #not finished