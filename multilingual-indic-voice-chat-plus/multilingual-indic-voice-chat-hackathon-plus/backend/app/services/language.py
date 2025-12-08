
def detect_lang(text: str) -> str:
    for ch in text:
        code = ord(ch)
        if 0x0B80 <= code <= 0x0BFF:
            return 'ta'
        if 0x0900 <= code <= 0x097F:
            return 'hi'
        if 0x0C00 <= code <= 0x0C7F:
            return 'te'
    return 'en'
