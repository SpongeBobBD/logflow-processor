
# Logflow Processor

This Python project generates and analyzes network flow logs. It includes a data generator to create log files and lookup tables, and an analyzer that processes the logs to output counts of tags and port/protocol combinations.

## Project Structure

- `generate_data.py`: Script to generate a network log file and lookup table.
- `log_analyzer.py`: Script to analyze log files, count tags, and save the results.
- `config.ini`: Configuration file for lookup table and log/output file prefixes.
- `network_logs_<date>.log`: Date-specific generated log file.
- `output_<date>.txt`: Date-specific results file.
- `port_protocol_lookup.csv`: CSV file mapping ports/protocols to tags.

## Requirements

- Python 3.x
- No additional libraries required.

## Setup and Installation

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd logflow-processor
    ```

2. Ensure Python 3.x is installed.

## Usage

### 1. Generate Data

To create a network flow log file and lookup table:

```bash
python generate_data.py --max_log_size_mb <size_in_mb> --max_lookup_entries <entry_count>
```

- `--max_log_size_mb`: Max log file size in MB (default: 10 MB).
- `--max_lookup_entries`: Max number of entries in the lookup table (default: 10,000).

This will create a log file (`network_logs_<date>.log`) and a lookup table (`port_protocol_lookup.csv`).

### 2. Analyze Logs

To analyze the generated log file and save results:

```bash
python log_analyzer.py
```

The analyzer reads configurations from `config.ini` and processes the log file, producing an output file with counts of tags and port/protocol combinations.

### Configuration

Edit `config.ini` to set file paths and prefixes:

```ini
[Files]
lookup_table_file = port_protocol_lookup.csv
log_file_prefix = network_logs
output_file_prefix = output
```

### Output

The output CSV file contains:

- Tag counts (sorted by frequency, with "Untagged" listed last).
- Port/Protocol counts.

### Error Handling

If the log version (first column) is not `2`, the analyzer logs an error and stops processing.

## Example Workflow

1. Generate log data:
   ```bash
   python generate_data.py --max_log_size_mb 1 --max_lookup_entries 10
   ```

2. Analyze the generated log data:
   ```bash
   python log_analyzer.py
   ```

## Testing

I’ve performed several tests to verify accuracy and performance:

- Validated tag counts and different port/protocol combinations for accuracy.
- Tested performance with a 5 MB log file and 10,000 lookup entries.
- Verified error handling and logging when encountering unsupported log versions.
