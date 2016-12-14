import os
import pytest
from qtpandas.models.DataFrameModelManager import DataFrameModelManager
from tests.main import MainTestClass


class TestClass(MainTestClass):

    @pytest.fixture
    def sample_file(self, df, output_dir) -> str:
        file_path = os.path.join(output_dir, "test_dfm_manager_file.csv")
        if not os.path.exists(file_path):
            df.to_csv(file_path)
        return file_path

    @pytest.fixture
    def manager(self) -> DataFrameModelManager:
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











