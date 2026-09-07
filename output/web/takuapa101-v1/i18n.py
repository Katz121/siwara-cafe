import json
from pathlib import Path

_translations = {}
_loaded_lang = None

def load(lang):
    global _translations, _loaded_lang
    _translations = {}
    _loaded_lang = lang
    
    # Load romanisation first
    rom_path = Path('data/i18n/romanisation.json')
    if rom_path.exists():
        with open(rom_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, dict):
                _translations.update(data)
                
    # Load all json files in data/i18n/{lang}
    lang_dir = Path(f'data/i18n/{lang}')
    if lang_dir.exists():
        for p in lang_dir.glob('*.json'):
            with open(p, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    # For flat structures like ui.json
                    for k, v in data.items():
                        if isinstance(v, str):
                            _translations[k] = v
                        else:
                            # Might be nested or specific objects like places.json
                            # Just store them anyway, maybe by an identifier if they have one?
                            # But t(text) is usually for strings.
                            pass
                            
def t(text, lang='en'):
    if _loaded_lang != lang:
        load(lang)
    return _translations.get(text, text)
