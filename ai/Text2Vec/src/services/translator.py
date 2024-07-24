from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from core.config import settings


model = None
tokenizer = None
translation_pipeline = None

def load_model():
    return AutoModelForSeq2SeqLM.from_pretrained(settings.translation.checkpoint)

def init_tokenizer():
    return AutoTokenizer.from_pretrained(settings.translation.checkpoint)

def init_translator():
    return pipeline("translation",
                    model=model,
                    tokenizer=tokenizer,
                    src_lang=settings.translation.source_lang,
                    tgt_lang=settings.translation.target_lang,
                    max_length = settings.translation.max_length)

def translation(text: str) -> str:
    translated_text = ''
    for t in text.split('. '):
        output = translation_pipeline(t)
        translated = output[0]["translation_text"]
        translated_text = translated_text  + translated + '. '
    return translated_text