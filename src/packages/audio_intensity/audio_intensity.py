import os
import sys
from statistics import quantiles
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

        total = 0
        for chunk in make_chunks(self._sound, chunk_length):
            total += chunk.rms
        average = total / (self._sound.duration_seconds / chunk_length * 1000)

        self._cache['rms'][chunk_length] = average
        return average

    def get_rms_threshold(self, chunk_length, num_intervals, threshold_quantile):
        cache_key = str(chunk_length) + '__' + str(num_intervals)
        if cache_key in self._cache['thresholds']:
            return self._cache['thresholds'][cache_key][threshold_quantile]

        # If sample space is exhaustive, calculate the quantile with no room for error
        method = 'inclusive' if chunk_length == 1 else 'exclusive'

        sound = [s.rms for s in self._sound[::chunk_length]]
        list_of_quantiles = quantiles(sound, n=num_intervals, method=method)

        self._cache['thresholds'][cache_key] = list_of_quantiles
        return list_of_quantiles[threshold_quantile]

if __name__ == '__main__':
    file = 'dolphins.mp3' if len(sys.argv) < 2 else sys.argv[1]

    script_path = os.path.abspath(os.path.join(__file__, '../../../', 'fixtures/'))
    file_path = os.path.join(script_path, file)

    audio_intensity_analyzer = AudioIntensityAnalyzer(file_path)

    print(audio_intensity_analyzer.get_average_root_mean_square(1000))
    print(audio_intensity_analyzer.get_rms_threshold(1000, 10, 8))