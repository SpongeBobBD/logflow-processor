import csv
import logging
import configparser
from collections import defaultdict
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

protocol_map = {
    "1": "icmp",
    "2": "igmp",
    "6": "tcp",
    "17": "udp",
    "41": "ipv6-encapsulation",
    "47": "gre",
    "50": "esp",
    "51": "ah",
    "58": "icmpv6",
    "89": "ospf",
    "132": "sctp"
}

def load_lookup_table(filename):
    """
    Reads the lookup table from a CSV file.

    Parameters:
        filename (str): Path to the CSV file with the lookup data.

    Returns:
        dict: A dictionary where each key is a (destination port, protocol) pair and each value is a tag.
    """
    lookup_table = {}
    try:
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for dstport, protocol, tag in reader:
                lookup_table[(dstport, protocol.lower())] = tag
        logging.info("Lookup table successfully loaded.")
    except FileNotFoundError:
        logging.error(f"Could not find the file: {filename}")
    except Exception as e:
        logging.error(f"Error occurred while loading lookup table from {filename}: {e}")
    return lookup_table

def parse_flow_logs(log_filename, lookup_table):
    """
    Processes a log file to count occurrences of tags and port/protocol combinations.

    Parameters:
        log_filename (str): Path to the flow log file.
        lookup_table (dict): Lookup dictionary mapping (destination port, protocol) to tags.

    Returns:
        tuple: Two dictionaries:
            - tag_counts: Counts of each tag found.
            - port_protocol_counts: Counts of each (destination port, protocol) pair.
    """
    tag_counts = defaultdict(int)
    port_protocol_counts = defaultdict(int)

    try:
        with open(log_filename, 'r') as logfile:
            for line in logfile:
                fields = line.split()

                # Check version in the first column
                if fields[0] != "2":
                    logging.error(f"Unsupported version {fields[0]} in log entry. Expected version 2.")
                    raise ValueError(f"Unsupported log version {fields[0]} encountered. Stopping processing.")

                dstport = fields[5]  # Assumes destination port is in the 6th column
                protocol_code = fields[7]  # Assumes protocol code is in the 8th column

                # Retrieve protocol name using the protocol map
                protocol = protocol_map.get(protocol_code, "unknown")

                # Retrieve tag or mark as "Untagged" if not found
                tag = lookup_table.get((dstport, protocol), "Untagged")
                tag_counts[tag] += 1
                port_protocol_counts[(dstport, protocol)] += 1
        logging.info("Flow logs processed successfully.")
    except FileNotFoundError:
        logging.error(f"Could not find the file: {log_filename}")
    except Exception as e:
        logging.error(f"Error while processing flow logs from {log_filename}: {e}")
        raise

    return tag_counts, port_protocol_counts

def save_results(tag_counts, port_protocol_counts, output_filename):
    """
    Writes tag counts and port/protocol counts to a CSV file.

    Parameters:
        tag_counts (dict): Dictionary containing each tag and its count.
        port_protocol_counts (dict): Dictionary with (destination port, protocol) as keys and their counts as values.
        output_filename (str): Path to the output CSV file.
    """
    try:
        with open(output_filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Tag Counts"])
            writer.writerow(["Tag", "Count"])

            # Sort tags by count in descending order and place "Untagged" at the end
            sorted_tags = sorted(
                ((tag, count) for tag, count in tag_counts.items() if tag != "Untagged"),
                key=lambda x: x[1],
                reverse=True
            )
            untagged_count = tag_counts.get("Untagged", 0)

            for tag, count in sorted_tags:
                writer.writerow([tag, count])

            # Add "Untagged" row at the bottom if it exists
            if untagged_count > 0:
                writer.writerow(["Untagged", untagged_count])

            writer.writerow([])
            writer.writerow(["Port/Protocol Combination Counts"])
            writer.writerow(["Port", "Protocol", "Count"])
            for (dstport, protocol), count in port_protocol_counts.items():
                writer.writerow([dstport, protocol, count])

        logging.info("Results successfully saved.")
    except Exception as e:
        logging.error(f"Failed to save results to {output_filename}: {e}")

def main():
    """
    Main function to load configuration, process logs, and save results.
    """
    # Load configuration settings
    config = configparser.ConfigParser()
    try:
        config.read("config.ini")
        lookup_table_file = config.get("Files", "lookup_table_file")
        log_file_prefix = config.get("Files", "log_file_prefix")
        output_file_prefix = config.get("Files", "output_file_prefix")
    except Exception as e:
        logging.error(f"Failed to read configuration: {e}")
        return

    date_str = datetime.now().strftime("%Y-%m-%d")
    log_file = f"{log_file_prefix}_{date_str}.log"
    output_file = f"{output_file_prefix}_{date_str}.txt"

    # Load the lookup table and parse logs
    lookup_table = load_lookup_table(lookup_table_file)
    if lookup_table:
        try:
            tag_counts, port_protocol_counts = parse_flow_logs(log_file, lookup_table)
            save_results(tag_counts, port_protocol_counts, output_file)
        except ValueError as e:
            logging.error(f"Processing halted due to error: {e}")

if __name__ == "__main__":
    main()
