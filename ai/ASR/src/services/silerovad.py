from functools import lru_cache
import torch
from core import settings


class OnnxWrapper():

    def __init__(self, path, force_onnx_cpu=False):
        global np
        import onnxruntime
        if force_onnx_cpu and 'CPUExecutionProvider' in onnxruntime.get_available_providers():
            self.session = onnxruntime.InferenceSession(path, providers=['CPUExecutionProvider'])
        else:
            self.session = onnxruntime.InferenceSession(path)
        self.session.intra_op_num_threads = 1
        self.session.inter_op_num_threads = 1

        self.reset_states()
        self.sample_rates = settings.core.valid_sample_rate

    def _validate_input(self, x, sr: int):
        if len(x.shape) == 1:
            x = x.unsqueeze(0)
        if len(x.shape) > 2:
            raise ValueError(f"Too many dimensions for input audio chunk {x.dim()}")

        if sr != 16000 and (sr % 16000 == 0):
            step = sr // 16000
            x = x[::step]
            sr = 16000

        if sr not in self.sample_rates:
            raise ValueError(f"Supported sampling rates: {self.sample_rates} (or multiply of 16000)")

        if sr / x.shape[1] > 31.25:
            raise ValueError("Input audio chunk is too short")

        return x, sr

    def reset_states(self, batch_size=1):
        self._h = np.zeros((2, batch_size, 64)).astype('float32')
        self._c = np.zeros((2, batch_size, 64)).astype('float32')
        self._last_sr = 0
        self._last_batch_size = 0

    def __call__(self, x, sr: int):

        x, sr = self._validate_input(x, sr)
        batch_size = x.shape[0]

        if not self._last_batch_size:
            self.reset_states(batch_size)
        if (self._last_sr) and (self._last_sr != sr):
            self.reset_states(batch_size)
        if (self._last_batch_size) and (self._last_batch_size != batch_size):
            self.reset_states(batch_size)

        if sr in self.sample_rates:
            ort_inputs = {'input': x, 'h': self._h, 'c': self._c, 'sr': np.array(sr).astype('int64')}
            ort_outs = self.session.run(None, ort_inputs)
            out, self._h, self._c = ort_outs
        else:
            raise ValueError()

        self._last_sr = sr
        self._last_batch_size = batch_size

        return out

    def audio_forward(self, x, sr: int, num_samples: int = settings.core.num_samples):
        outs = []
        x, sr = self._validate_input(x, sr)

        if x.shape[1] % num_samples:
            pad_num = num_samples - (x.shape[1] % num_samples)
            x = torch.nn.functional.pad(x, (0, pad_num), 'constant', value=0.0)

        self.reset_states(x.shape[0])
        for i in range(0, x.shape[1], num_samples):
            wavs_batch = x[:, i:i + num_samples]
            out_chunk = self.__call__(wavs_batch, sr)
            outs.append(out_chunk)

        stacked = torch.cat(outs, dim=1)
        return stacked.cpu()


class Vad:

    @lru_cache()
    def __init__(self, threshold):
        self.threshold = threshold
        self.model = OnnxWrapper('models/vad/silero_vad.onnx', force_onnx_cpu=True)

    def _prepare_audio(self, audio):
        audio1 = np.frombuffer(audio, dtype=np.int16)
        audio1 = audio1.astype(np.float32) / settings.core.max_val
        chunk = np.concatenate((audio1, np.zeros((settings.core.size_chunk))))
        return chunk[:settings.core.size_chunk].reshape((1, settings.core.size_chunk)).astype(np.float32)

    def is_speech(self, audio, sample_rate):
        out = self.model(self._prepare_audio(audio), sample_rate)
        return out[0][0] > self.threshold

    def reset(self):
        self.model.reset_states()
