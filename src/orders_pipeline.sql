-- Declarative pipeline source: Auto Loader via read_files into a streaming table.
-- ${landing_path} comes from the pipeline `configuration` in resources/orders_pipeline.yml
CREATE OR REFRESH STREAMING TABLE orders_bronze
AS SELECT
  *,
  _metadata.file_path AS source_file
FROM STREAM read_files(
  '${landing_path}',
  format => 'json'
);
