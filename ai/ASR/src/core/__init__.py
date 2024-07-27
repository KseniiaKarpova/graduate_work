from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class SettingsModelV1(BaseSettings):
    path: str = 'models/v1/'
    encoder: str = path + "am/encoder.int8.onnx"
    decoder: str = path + "am/decoder.int8.onnx"
    joiner: str = path + "am/joiner.int8.onnx"
    tokens: str = path + "lang/tokens.txt"
    num_threads: int = 4
    sample_rate: int = 8000
    decoding_method: str = "modified_beam_search"
    hotwords: str = path + 'hot_words_ru_v1.txt'


class SettingsModelV2(BaseSettings):
    path: str = 'models/v2/'
    encoder: str = path + "am-onnx/encoder.onnx"
    decoder: str = path + "am-onnx/decoder.onnx"
    joiner: str = path + "am-onnx/joiner.onnx"
    tokens: str = path + "lang/tokens.txt"
    num_threads: int = 4
    sample_rate: int = 8000
    decoding_method: str = "modified_beam_search"
    hotwords: str = path + 'hot_words_ru_v2.txt'


class AsrCoreSettings(BaseSettings):
    max_size: int = ...
    valid_content_type: List[str] = ...
    valid_sample_rate: List[int] = ...
    recommended_sample_rate: int = ...
    max_val: int = ...
    num_samples: int = ...
    size_chunk: int = ...
    model_config: str = SettingsConfigDict(env_prefix='asr_core_')

class Settings(BaseSettings):
    basemodel = SettingsModelV2()
    core : AsrCoreSettings = AsrCoreSettings()

settings = Settings()