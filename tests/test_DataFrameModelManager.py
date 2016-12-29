from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
import os
import pytest
import pandas as pd
from qtpandas.models.DataFrameModelManager import DataFrameModelManager



class MainTestClass(object):

    @pytest.fixture
    def df(self):
        sample_cols = ['id', 'name', 'address', 'updated']
        sample_recs = [[1000, 'zeke', '123 street'],
                       [1001, 'larry', '688 road'],
                       [1002, 'fred', '585 lane']]
        for rec in sample_recs:
            rec.append(pd.NaT)
        return pd.DataFrame(sample_recs, columns=sample_cols)

    @pytest.fixture
    def output_dir(self):
        fp = os.path.join(os.path.dirname(__file__), "output")
        if not os.path.exists(fp):
            os.mkdir(fp)
        return fp

    @pytest.fixture
    def fixtures_dir(self):
        fp = os.path.join(os.path.dirname(__file__), "fixtures")
        if not os.path.exists(fp):
            os.mkdir(fp)
        return fp

    @pytest.fixture
    def project_root_dir(self, fixtures_dir):
        return os.path.join(fixtures_dir, "fixed_root_dir/fixed_project")

    @pytest.fixture
    def project_log_dir(self, project_root_dir):
        return os.path.join(project_root_dir, "logs")

    @pytest.fixture
    def project_settings_path(self, project_root_dir):
        return os.path.join(project_root_dir, "sample_project_config.ini")

    @pytest.fixture
    def example_file_path(self, project_root_dir):
        return os.path.join(project_root_dir, "example.csv")

class TestClass(MainTestClass):

    @pytest.fixture
    def sample_file(self, df, output_dir):
        file_path = os.path.join(output_dir, "test_dfm_manager_file.csv")
        if not os.path.exists(file_path):
            df.to_csv(file_path)
        return file_path

    @pytest.fixture
    def manager(self):
        return DataFrameModelManager()

    def test_read_file_basics(self, sample_file, manager):
        manager.read_file(sample_file)
        model = manager.get_model(sample_file)
        df = manager.get_frame(sample_file)
        assert sample_file in manager.file_paths
        assert model.dataFrame().index.size == df.index.size
        assert sample_file in manager._paths_read

    def test_save_file(self, sample_file, manager):

        manager.read_file(sample_file)
        check_path = os.path.splitext(sample_file)[0] + "_check.csv"

        manager.save_file(sample_file, save_as=check_path, keep_orig=True)

        assert check_path in manager.file_paths
        assert sample_file in manager.file_paths
        assert os.path.exists(check_path)
        os.remove(check_path)

        manager.save_file(sample_file, save_as=check_path, keep_orig=False)

        assert check_path in manager.file_paths
        assert sample_file not in manager.file_paths
        assert os.path.exists(check_path)
        os.remove(check_path)
