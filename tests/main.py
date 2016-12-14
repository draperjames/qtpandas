import os
import pytest
import pandas as pd


class MainTestClass(object):

    @pytest.fixture
    def df(self) -> pd.DataFrame:
        sample_cols = ['id', 'name', 'address', 'updated']
        sample_recs = [[1000, 'zeke', '123 street'],
                       [1001, 'larry', '688 road'],
                       [1002, 'fred', '585 lane']]
        for rec in sample_recs:
            rec.append(pd.NaT)
        return pd.DataFrame(sample_recs, columns=sample_cols)

    @pytest.fixture
    def output_dir(self) -> str:
        fp = os.path.join(os.path.dirname(__file__), "output")
        if not os.path.exists(fp):
            os.mkdir(fp)
        return fp

    @pytest.fixture
    def fixtures_dir(self) -> str:
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
