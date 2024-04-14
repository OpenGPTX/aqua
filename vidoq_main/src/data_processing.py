import pandas as pd
import os

class MetaDataProcessor:
    """Class to process metadata."""

    def __init__(self, file_path):
        """Initialize MetaDataProcessor.

        Args:
            file_path (str): Path to the JSON file containing metadata.
        """
        self.file_path = file_path
        self.meta_data = pd.read_json(file_path, lines=True)

    def sample_meta_data(self, sample_size):
        """Sample metadata.

        Args:
            sample_size (int or str): Number of samples to be selected. If 'All', all samples are selected.

        Returns:
            pd.DataFrame: Sampled metadata.
        """
        if sample_size == 'All' or sample_size >= len(self.meta_data):
            sampled_data = self.meta_data
        else:
            sampled_data = self.meta_data.sample(n=sample_size, replace=False)

        metadata_columns = self.extract_metadata_columns()
        sampled_data[metadata_columns] = sampled_data['meta'].apply(lambda x: pd.Series({col: x.get(col, None) for col in metadata_columns}))
        sampled_data[metadata_columns] = sampled_data[metadata_columns].apply(pd.to_numeric, errors='coerce')

        return sampled_data

    def extract_metadata_columns(self):
        """Extract metadata columns.

        Returns:
            list: List of metadata columns.
        """
        all_metadata = self.meta_data['meta'].apply(lambda x: set(x.keys()) if isinstance(x, dict) else set())
        metadata_columns = sorted(set.union(*all_metadata))
        return metadata_columns

class WordCountProcessor:
    """Class to process word count data."""

    def __init__(self, file_path):
        """Initialize WordCountProcessor.

        Args:
            file_path (str): Path to the directory containing word count CSV files.
        """
        self.file_path = file_path
        
    def read_word_count_files(self):
        """Read word count CSV files.

        Returns:
            pd.DataFrame: Combined DataFrame of word count data.
        """
        column_names = ['file_name', 'language', 'num_documents', 'num_words', 'num_chars']
        dataframes = [pd.read_csv(os.path.join(self.file_path, filename), names=column_names)
                      for filename in os.listdir(self.file_path) if filename.endswith('.csv')]
        combined_df = pd.concat(dataframes, ignore_index=True)

        return combined_df
