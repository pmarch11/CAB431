""" def calc_df(coll):
    df_ = {}
    for x in list(coll):
        for doc in coll[x]:
            for term in coll[doc]:
                try:
                    df_[term] += 1
                except KeyError:
                    df_[term] = 1
    return df_
 """
def calc_df(coll):
    """Calculate DF of each term in vocab and return as term:df dictionary."""
    df_ = {}
    for id, doc in coll.get_docs().items():
        for term in doc.get_term_list():
            try:
                df_[term] += 1
            except KeyError:
                df_[term] = 1
    return df_


if __name__ == '__main__':

    import sys
    import coll

    if len(sys.argv) != 2:
        sys.stderr.write("USAGE: %s <coll-file>\n" % sys.argv[0])
        sys.exit()
    stopwords_f = open('common-english-words.txt', 'r')
    stop_words = stopwords_f.read().split(',')
    stopwords_f.close()
    coll_ = coll.parse_rcv_coll(sys.argv[1], stop_words)
    df_ = calc_df(coll_)
    print('There are ' + str(coll_.get_num_docs()) + 'documents in this data set and contains ' + str(len(df_)) + ' terms')
    for (term, df_) in iter(sorted(df_.items(), key=lambda x: x[1],reverse=True)):
        print(term + ' : ' + str(df_))
