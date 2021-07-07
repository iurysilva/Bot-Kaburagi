from googletrans import Translator


def traduzir_do_ingles(text):
    tradutor = Translator()
    traducao = tradutor.translate(text, src="en", dest="pt")
    return traducao.text
