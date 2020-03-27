import os
import sys
from functools import reduce
import numpy as np
from pydub import AudioSegment
from pydub.utils import make_chunks


class AudioIntensityAnalyzer:
    def __init__(self, filepath):
        self._sound = AudioSegment.from_mp3(file=filepath)

        self._cache = {
            'rms': {},
            'thresholds': {}
        }

    # Chunk length in ms
    def get_average_root_mean_square(self, chunk_length=1):
        if chunk_length in self._cache['rms']:
            return self._cache[chunk_length]

        total = reduce(lambda total, elem: total + elem.rms, make_chunks(self._sound, chunk_length), 0)
        average = total / (self._sound.duration_seconds / chunk_length * 1000)

        self._cache['rms'][chunk_length] = average
        return average

    def get_rms_threshold(self, chunk_length, threshold_quantile):
        cache_key = str(chunk_length) + '__' + str(threshold_quantile)
        if cache_key in self._cache['thresholds']:
            return self._cache['thresholds'][cache_key]

        sound = np.array([s.rms for s in self._sound[::chunk_length]])
        quantile_value = np.quantile(sound, threshold_quantile)

        self._cache['thresholds'][cache_key] = quantile_value
        return quantile_value


if __name__ == '__main__':
    # file = 'dolphins.mp3' if len(sys.argv) < 2 else sys.argv[1]

    # script_path = os.path.abspath(os.path.join(__file__, '../../../', 'fixtures/'))
    # file_path = os.path.join(script_path, file)

    # audio_intensity_analyzer = AudioIntensityAnalyzer(file_path)

    # print(audio_intensity_analyzer.get_average_root_mean_square(1000))
    # print(audio_intensity_analyzer.get_rms_threshold(1000, 0.5))
    # print(audio_intensity_analyzer.get_rms_threshold(1000, 0.8))
    # print(audio_intensity_analyzer.get_rms_threshold(1000, 0.9))
