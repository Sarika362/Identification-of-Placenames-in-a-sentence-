from deep_translator import GoogleTranslator


def translator(sentence):

    translated = GoogleTranslator(source='auto', target='en').translate(sentence)
    return translated
