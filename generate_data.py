import csv
import random
from datetime import datetime
import os
import argparse

def generate_log_file(output_file, max_size_mb):
    """
    Generate a network flow log file with a size limit of max_size_mb MB
    """
    max_bytes = max_size_mb * 1024 * 1024
    with open(output_file, 'w') as file:
        while os.path.getsize(output_file) < max_bytes:
            log_version = 2
            user_id = "123456789012"
            interface_id = f"eni-{random.choice('abcdef')}{random.randint(1, 9)}{random.choice('abcdef')}{random.randint(1, 9)}"
            source_ip = f"10.0.{random.randint(0, 255)}.{random.randint(0, 255)}"
            destination_ip = f"198.51.100.{random.randint(1, 255)}"
            dest_port = random.choice([22, 23, 25, 80, 110, 143, 443, 993, 3389, 49153])
            src_port = random.randint(1, 65535)
            protocol_id = random.choice(["6", "17"])  # 6: TCP, 17: UDP
            packet_count = random.randint(1, 100)
            byte_count = random.randint(100, 100000)
            start_time = 1620140761
            end_time = start_time + random.randint(1, 1000)
            connection_action = random.choice(["ACCEPT", "REJECT"])
            log_status = "OK"
            log_entry = f"{log_version} {user_id} {interface_id} {source_ip} {destination_ip} {dest_port} {src_port} {protocol_id} {packet_count} {byte_count} {start_time} {end_time} {connection_action} {log_status}\n"
            file.write(log_entry)

def generate_lookup_file(lookup_file, entry_count):
    """
    Generate a CSV lookup file with a specified number of mappings based on common port-protocol combinations.
    """
    port_protocol_map = {
        22: "tcp",
        23: "tcp",
        25: "tcp",
        53: "udp",
        80: "tcp",
        110: "tcp",
        143: "tcp",
        443: "tcp",
        993: "tcp",
        3389: "tcp",
        49153: "udp"
    }

    tag_options = ["sv_P1", "sv_P2", "sv_P3", "sv_P4", "sv_P5", "SV_P1", "SV_P2", "email", "Email"]

    with open(lookup_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["destination_port", "protocol", "tag"])

        for _ in range(entry_count):
            port = random.choice(list(port_protocol_map.keys()))
            protocol_type = port_protocol_map[port]
            tag_name = random.choice(tag_options)
            writer.writerow([port, protocol_type, tag_name])

def main(max_log_size_mb, max_lookup_entries):
    date_str = datetime.now().strftime("%Y-%m-%d")
    log_filename = f"network_logs_{date_str}.log"

    # Generate log file with specified size limit
    generate_log_file(log_filename, max_size_mb=max_log_size_mb)

    # Generate lookup file with the specified number of mappings
    generate_lookup_file("port_protocol_lookup.csv", entry_count=max_lookup_entries)

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Generate network logs and lookup table.")
    parser.add_argument("--max_log_size_mb", type=int, default=10, help="Maximum log file size in MB")
    parser.add_argument("--max_lookup_entries", type=int, default=10000, help="Maximum number of mappings in lookup table")
    args = parser.parse_args()

    # Run main function with provided arguments
    main(max_log_size_mb=args.max_log_size_mb, max_lookup_entries=args.max_lookup_entries)
