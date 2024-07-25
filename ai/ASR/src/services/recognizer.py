from functools import lru_cache

import core
import sherpa_onnx


@lru_cache
def get_settings():
    return core.SettingsModelV2()


settings = get_settings()


@lru_cache()
def get_recognizer():
    return sherpa_onnx.OfflineRecognizer.from_transducer(
        encoder=settings.encoder,
        decoder=settings.decoder,
        joiner=settings.joiner,
        tokens=settings.tokens,
        num_threads=settings.num_threads,
        sample_rate=settings.sample_rate,
        decoding_method=settings.decoding_method,
    )
