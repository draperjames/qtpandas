import numpy
import pytest
from pandasqt.models.SupportedDtypes import SupportedDtypes, SupportedDtypesTranslator

@pytest.fixture()
def expected_support():
    numpy_datatypes = [numpy.bool_, numpy.bool, numpy.int_,
                 numpy.intc, numpy.intp, numpy.int8,
                 numpy.int16, numpy.int32, numpy.int64,
                 numpy.uint8, numpy.uint16, numpy.uint32,
                 numpy.uint64, numpy.float_, numpy.float16,
                 numpy.float32, numpy.float64]

    python_datatypes = [bool, int, float, object]

    return numpy_datatypes + python_datatypes


@pytest.fixture()
def descriptions():
    return [(object, 'text'), (bool, 'true/false value'), (None, 'fooo')]

@pytest.fixture()
def obj():
    return SupportedDtypes

class TestSupportedDtypes(object):

    def test_init(self):
        assert isinstance(SupportedDtypes, SupportedDtypesTranslator)

    def test_types(self, expected_support, obj):
        for datatype in expected_support:
            assert datatype in obj.allTypes()

    def test_lists(self, obj):
        types = obj.strTypes() + obj.boolTypes() + obj.intTypes() + obj.uintTypes() + obj.floatTypes() + obj.datetimeTypes()

        for t in types:
            assert t in obj.allTypes()

    def test_description(self, expected_support, obj):
        for datatype in expected_support:
            assert obj.description(datatype) is not None

        from StringIO import StringIO
        s = StringIO()
        assert obj.description(s) is None
        assert obj.description(str) is None
        assert obj.description(numpy.complex_) is None

        # lists, tuples, dicts refer to numpy.object types and
        # return a 'text' description - working as intended or bug?
        assert obj.description(dict) is not None
        assert obj.description(list) is not None
        assert obj.description(tuple) is not None

    def test_dtype(self, descriptions, obj):
        for (expected_type, desc) in descriptions:
            assert obj.dtype(desc) == expected_type

    def test_names(self, obj):
        names = obj.names()
        types = obj.allTypes()

        for data in zip(types, names):
            assert data in obj._all

    def test_tuple_at(self, obj):
        names = obj.names()
        types = obj.allTypes()

        for index, data in enumerate(zip(types, names)):
            assert obj.tupleAt(index) == data

        assert not obj.tupleAt(33)
