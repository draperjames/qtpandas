# -*- coding: utf-8 -*-

from pandasqt.compat import Qt, QtCore, QtGui


import pytest

from pandasqt.views.BigIntSpinbox import BigIntSpinbox

class TestClass(object):

    @pytest.fixture
    def spinbox(self, qtbot):
        widget = BigIntSpinbox()
        qtbot.addWidget(widget)
        return widget

    def test_init(self, spinbox):
        assert spinbox

    def test_value(self, spinbox):
        assert spinbox.value() == 0
        spinbox._lineEdit.setText('')   # runs into exception
        assert spinbox.value() == 0

    def test_minimumMaximum(self, spinbox):
        assert spinbox.minimum() == -18446744073709551616
        assert spinbox.maximum() == 18446744073709551615

    def test_setMinimumMaximum(self, spinbox):
        spinbox.setMinimum(0)
        spinbox.setMinimum(long(0))
        spinbox.setMinimum(1)
        spinbox.setMinimum(long(1))
        spinbox.setMinimum(-1)
        spinbox.setMinimum(long(-1))
        with pytest.raises(TypeError) as excinfo:
            spinbox.setMinimum('')
        assert "int or long" in str(excinfo.value)

        spinbox.setMaximum(0)
        spinbox.setMaximum(long(0))
        spinbox.setMaximum(1)
        spinbox.setMaximum(long(1))
        spinbox.setMaximum(-1)
        spinbox.setMaximum(long(-1))
        with pytest.raises(TypeError) as excinfo:
            spinbox.setMaximum('')
        assert "int or long" in str(excinfo.value)

    def test_setValue(self, spinbox):
        assert spinbox.setValue(10)
        assert spinbox.value() == 10

        assert spinbox.setValue(18446744073709551615 + 1)
        assert spinbox.value() == spinbox.maximum()

        assert spinbox.setValue(-18446744073709551616 - 1)
        assert spinbox.value() == spinbox.minimum()

    def test_singleStep(self, spinbox):
        assert spinbox.singleStep() == 1

        assert spinbox.setSingleStep(10) == 10
        assert spinbox.setSingleStep(-10) == 10
        with pytest.raises(TypeError) as excinfo:
            spinbox.setSingleStep('')
            spinbox.setSingleStep(0.1212)
        assert "int" in str(excinfo.value)

        assert spinbox.setSingleStep(0) == 0

    def test_stepEnabled(self, spinbox):
        assert spinbox.StepUpEnabled
        assert spinbox.StepDownEnabled
        assert spinbox.stepEnabled() == spinbox.StepUpEnabled | spinbox.StepDownEnabled

        spinbox.setMinimum(0)
        spinbox.setMaximum(10)
        spinbox._lineEdit.setText(str(-1))
        assert spinbox.stepEnabled() == spinbox.StepUpEnabled
        spinbox._lineEdit.setText(str(11))
        assert spinbox.stepEnabled() == spinbox.StepDownEnabled

    def test_stepBy(self, spinbox):
        spinbox.setMinimum(0)
        spinbox.setMaximum(10)
        spinbox.setValue(0)
        spinbox.stepBy(1)
        assert spinbox.value() == 1
        spinbox.stepBy(-1)
        assert spinbox.value() == 0

        spinbox.setMinimum(0)
        spinbox.setMaximum(10)
        spinbox.setValue(0)

        spinbox.stepBy(-1)
        assert spinbox.value() == 0 # should be minimum cause -1 is out of bounds

        spinbox.setValue(10)
        spinbox.stepBy(1)
        assert spinbox.value() == 10 # should be maximum cause 11 is out of bounds