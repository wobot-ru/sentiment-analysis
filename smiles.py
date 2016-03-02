# -*- coding: utf-8 -*-
smiles = {
    # positive emoticons
    u'&lt;3': u' любить ',
    u':d': u' любить ',
    u':dd': u' любить ',
    u'8)': u' любить ',
    u':-)': u' любить ',
    u':)': u' любить ',
    u';)': u' любить ',
    u'(-:': u' любить ',
    u'(:': u' любить ',

    # negative emoticons:
    u':/': u' ненавидеть ',
    u':&gt;': u' ненавидеть ',
    u':-(': u' ненавидеть ',
    u':(': u' ненавидеть ',
    u':S': u' ненавидеть ',
    u':-S': u' ненавидеть ',
}

ordered_smiles = [k for (k_len, k) in reversed(sorted([(len(k), k) for k in list(smiles.keys())]))]


def smiles_preprocessor(doc):
    doc = doc.lower()
    for k in ordered_smiles:
        doc = doc.replace(k, smiles[k])
    return doc
