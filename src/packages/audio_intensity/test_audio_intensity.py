import math, json, os
from .audio_intensity import AudioIntensityAnalyzer

fixture_path = os.path.abspath(os.path.join(__file__ , '../../../', 'fixtures/'))

DOLPHINS = 'dolphins.mp3'

def _get_file_path(filename):
    return os.path.join(fixture_path, filename)

fixture_results = {}

with open(_get_file_path('dolphins.json')) as file:
    jsonData = file.read()
fixture_results[DOLPHINS] = json.loads(jsonData)

def test_average_root_mean_square():
    file_path = _get_file_path('dolphins.mp3')
    audio_intensity_analyzer = AudioIntensityAnalyzer(file_path)

    for result in fixture_results[DOLPHINS]['average_root_mean_square']:
        new_average = audio_intensity_analyzer.get_average_root_mean_square(result['chunk_length'])
        assert math.isclose(result['average'], new_average)

def test_root_mean_square_threshold():
    file_path = _get_file_path('dolphins.mp3')
    audio_intensity_analyzer = AudioIntensityAnalyzer(file_path)

    # Test if the threshold is sufficiently close when we halve the sampling rate
    assert math.isclose(
        audio_intensity_analyzer.get_rms_threshold(1, 10, 8),
        audio_intensity_analyzer.get_rms_threshold(2, 10, 8),
        rel_tol=0.05
    )