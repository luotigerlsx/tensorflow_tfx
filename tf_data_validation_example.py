import argparse
import logging

import apache_beam as beam
import tensorflow_data_validation as tfdv
from apache_beam.options.pipeline_options import PipelineOptions, SetupOptions
from tensorflow_data_validation.coders import csv_decoder
from tensorflow_metadata.proto.v0 import statistics_pb2

DATA_LOCATION = 'gs://tfx_job/census_train.csv'
OUTPUT_LOCATION = 'gs://tfx_job/output'

CSV_COLUMNS = ['age', 'workclass', 'fnlwgt', 'education', 'education_num', 'marital_status', 'occupation',
               'relationship', 'race', 'gender', 'capital_gain', 'capital_loss', 'hours_per_week', 'native_country',
               'income_bracket']


def run_pipeline(flags, pipeline_option):
    input_path = flags.input_path
    output_path = flags.output_path
    column_names = CSV_COLUMNS

    with beam.Pipeline(options=pipeline_option) as p:
        # If a header is not provided, assume the first line in a file
        # to be the header.
        skip_header_lines = 1 if column_names is None else 0

        _ = (
                p
                | 'ReadData' >> beam.io.textio.ReadFromText(
            file_pattern=input_path, skip_header_lines=skip_header_lines)
                | 'DecodeData' >> csv_decoder.DecodeCSV(column_names=column_names)
                | 'GenerateStatistics' >> tfdv.GenerateStatistics()
                | 'WriteStatsOutput' >> beam.io.WriteToTFRecord(
            output_path,
            shard_name_template='',
            coder=beam.coders.ProtoCoder(
                statistics_pb2.DatasetFeatureStatisticsList)))


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    """Build and run the pipeline."""

    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', required=True)
    parser.add_argument('--output_path', required=True)

    flags, pipeline_args = parser.parse_known_args()

    pipeline_option = PipelineOptions(flags=pipeline_args)
    pipeline_option.view_as(SetupOptions).save_main_session = True

    run_pipeline(flags, pipeline_option)
