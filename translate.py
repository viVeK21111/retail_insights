from easygoogletranslate import EasyGoogleTranslate

def translate(text):
    translator = EasyGoogleTranslate()
    result = translator.translate(text, target_language='en')
    return result