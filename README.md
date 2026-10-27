# orders_autoloader (Declarative Automation Bundle)

One bundle, two targets (dev, prod), two resources:
- `orders_pipeline`: declarative pipeline, Auto Loader via `read_files` into `orders_bronze`
- `orders_job`: Lakeflow Job running an Auto Loader notebook with a task retry

## Before you start (once)

1. Install the CLI and sign in
   - Mac: `brew tap databricks/tap && brew install databricks`
   - `databricks auth login --host https://<your-workspace-url>`
2. Put your workspace URL in `databricks.yml` (both targets).
3. Create the target schemas and make sure the landing and checkpoint volumes exist:

```sql
CREATE SCHEMA IF NOT EXISTS dbx_siva_dev.bronze_dev;
CREATE SCHEMA IF NOT EXISTS dbx_siva_dev.bronze_prod;
CREATE VOLUME IF NOT EXISTS dbx_siva_dev.bronze.landing;
CREATE VOLUME IF NOT EXISTS dbx_siva_dev.bronze.checkpoints;
```

4. Put a first file in the landing folder `/Volumes/dbx_siva_dev/bronze/landing/orders/`.

## Commands

```bash
databricks bundle validate -t dev
databricks bundle deploy   -t dev
databricks bundle summary  -t dev
databricks bundle run orders_pipeline -t dev
databricks bundle run orders_job      -t dev

databricks bundle validate -t prod
databricks bundle deploy   -t prod
databricks bundle run orders_job -t prod
```

## Schema evolution test (the Day 2 lab, now through the bundle)

1. Run `orders_job` once with only the baseline file.
2. Drop a file with a new column in the landing folder.
3. Run `orders_job` again. Attempt 1 fails with UnknownFieldException, attempt 2 passes.
4. Run `orders_pipeline` and compare what the pipeline does with the same file.

## If validate complains

- Serverless environment error on the job: run `databricks bundle init` with the default-python
  template in a scratch folder and copy its `environments` block into `resources/orders_job.yml`.
- Production mode asks for `run_as` or permissions: uncomment the `run_as` block under `targets.prod`.

## Git

```bash
git init
git checkout -b day2-auto-loader
git add .
git commit -m "Add orders_autoloader bundle"
git remote add origin <your-repo-url>
git push -u origin day2-auto-loader
```
