import os
from unittest import TestCase
import numpy as np

from src.main.python.main import TraceWindow

class TestTraceWindow(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.file_path = 'temp.txt'


    def test_loadTraceFromAscii_DeepFRET(self):
        filename = '../resources/traces/fiddler_3dim_0.txt'
        _trace = TraceWindow.loadTraceFromAscii(filename)
        self.assertIsInstance(_trace.acc.int, np.ndarray)
        self.assertIsInstance(_trace.grn.int, np.ndarray)
        self.assertIsInstance(_trace.red.int, np.ndarray)
        self.assertEqual(_trace.get_bleaches(), (57, None, 57))

    def test_save_and_load_trace(self):
        self.addCleanup(os.remove, self.file_path)
        filename = '../resources/traces/fiddler_3dim_0.txt'
        _trace = TraceWindow.loadTraceFromAscii(filename)
        _trace.tracename = self.file_path
        _trace.export_trace_to_txt()
        _trace2 = TraceWindow.loadTraceFromAscii(self.file_path)

        self.assertTrue(np.allclose(_trace.grn.int, _trace2.grn.int))
        self.assertTrue(np.allclose(_trace.first_bleach, _trace2.first_bleach))

    def test_calculating_fret(self):
        filename = '../resources/traces/fiddler_3dim_0.txt'
        _trace = TraceWindow.loadTraceFromAscii(filename)
        fret_old = _trace.fret
        _trace.calculate_fret()
        fret_new = _trace.fret

        np.testing.assert_array_almost_equal(fret_new, fret_old, decimal=2)

    def test_reducing_trace_save_and_load(self):
        self.addCleanup(os.remove, self.file_path)
        filename = '../resources/traces/fiddler_3dim_0.txt'
        _trace = TraceWindow.loadTraceFromAscii(filename)
        _trace.red.int[:] = None
        _trace.red.bg[:] = None
        _trace.stoi[:] = None
        _trace.tracename = self.file_path
        _trace.export_trace_to_txt()
        _trace2 = TraceWindow.loadTraceFromAscii(self.file_path)

        assert np.allclose(_trace.first_bleach, _trace2.first_bleach)
        assert np.allclose(_trace.grn.int, _trace2.grn.int)
        assert np.allclose(_trace.grn.bg, _trace2.grn.bg)
        assert np.allclose(_trace.acc.int, _trace2.acc.int)
        assert np.allclose(_trace.acc.bg, _trace2.acc.bg)
        np.testing.assert_array_almost_equal(_trace.red.int, _trace2.red.int)
        np.testing.assert_array_almost_equal(_trace.red.bg, _trace2.red.bg)
        np.testing.assert_array_almost_equal(_trace.stoi, _trace2.stoi)

    def test_reducing_trace_calculating_fret(self):
        self.addCleanup(os.remove, self.file_path)
        filename = '../resources/traces/fiddler_3dim_0.txt'
        _trace = TraceWindow.loadTraceFromAscii(filename)
        _trace.red.int[:] = None
        _trace.red.bg[:] = None
        _trace.stoi[:] = None
        _df = _trace.get_export_df()
        _trace.fret[:] = None
        _trace.tracename = self.file_path
        _trace.export_trace_to_txt()
        _trace2 = TraceWindow.loadTraceFromAscii(self.file_path)
        _df2 = _trace2.get_export_df()

        np.testing.assert_array_almost_equal(_df['E'], _df2['E'])

