import nltk
import spacy


nlp = spacy.load('en_core_web_trf')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')


def identify_place_names(sentence):
    # Tokenize the sentence using spaCy
    doc = nlp(sentence)

    # Identify place names using spaCy's named entity recognition (NER) model
    place_names = []
    for ent in doc.ents:
        if ent.label_ == 'GPE':
            place_names.append(ent.text)

    # Identify place names using NLTK's noun phrase chunking
    grammar = r'''
    NP: {<DT>?<JJ>*<NN>}
    '''
    chunks = nltk.pos_tag(nltk.word_tokenize(sentence))
    chunks = nltk.ne_chunk(chunks, grammar)

    for chunk in chunks:
        if type(chunk) == nltk.tree.Tree and chunk.label() == 'NP':
            place_names.append(' '.join([token.word for token in chunk]))

    return place_names
