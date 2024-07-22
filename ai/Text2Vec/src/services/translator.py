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
    output = translation_pipeline(text)
    translated_text = output[0]["translation_text"]
    return translated_text