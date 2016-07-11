import pytest

from pandasqt.encoding import Detector

@pytest.fixture
def detector():
    return Detector()

class TestDetector(object):

    def test_init(self, detector):
        assert detector.active

    def test_detect(self, detector, csv_file, csv_file_utf8):
        assert detector.detect(csv_file) == 'us-ascii'
        assert detector.detect(csv_file_utf8) == 'utf-8'