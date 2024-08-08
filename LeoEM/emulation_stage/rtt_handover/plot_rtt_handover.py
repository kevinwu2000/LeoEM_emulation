import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, timezone

# Function to read RTT data from a CSV file
def read_rtt_data(csv_file):
    rtt_data = []
    try:
        with open(csv_file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header row
            for row in reader:
                if row[1]:  # Ensure RTT is not empty
                    timestamp, rtt = float(row[0]), float(row[1])
                    rtt_data.append((timestamp, rtt))
    except PermissionError:
        print(f"Permission denied: '{csv_file}'. Please check the file permissions.")
    except FileNotFoundError:
        print(f"File not found: '{csv_file}'. Please check the file path.")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
    return rtt_data

# Function to normalize timestamps to start from zero
def normalize_timestamps(rtt_data):
    min_timestamp = min(data[0] for data in rtt_data)
    return [(timestamp - min_timestamp, rtt) for timestamp, rtt in rtt_data]

# Function to resample RTT data and plot with or without adjusted handover times
def resample_and_plot_rtt(rtt_data, handover_log, plot_with_handover_file, plot_without_handover_file, stats_file_path):
    if not rtt_data:
        print("No RTT data to plot.")
        return

    min_timestamp = min(data[0] for data in rtt_data)
    max_timestamp = max(data[0] for data in rtt_data)
    # Normalize the timestamps to start from 0
    rtt_data = normalize_timestamps(rtt_data)

    # Extracting timestamps and RTTs
    timestamps = [data[0] for data in rtt_data]
    rtts = [data[1] for data in rtt_data]

    # Calculate average and maximum RTT
    average_rtt = np.mean(rtts)
    max_rtt = np.max(rtts)
    min_rtt = np.min(rtts)

    # Write the statistics to a text file
    try:
        with open(stats_file_path, 'w') as stats_file:
            stats_file.write(f"Average RTT: {average_rtt:.2f} seconds\n")
            stats_file.write(f"Maximum RTT: {max_rtt:.2f} seconds\n")
            stats_file.write(f"Minimum RTT: {min_rtt:.2f} seconds\n")
        print(f"Statistics saved as {stats_file_path}")
    except Exception as e:
        print(f"An error occurred while writing the statistics file: {e}")

    # Resample timestamps to fit into 0-300 seconds range
    min_ts, max_ts = min(timestamps), max(timestamps)
    resampled_timestamps = [(ts - min_ts) / (max_ts - min_ts) * 300 for ts in timestamps]

    # Plot RTT over resampled time without handover events
    plt.figure(figsize=(12, 6))
    plt.scatter(resampled_timestamps, rtts, s=4, c='blue', alpha=0.6, edgecolors='none', label='RTT measurements')
    plt.plot(resampled_timestamps, rtts, linestyle='-', linewidth=0.3, color='blue', alpha=0.8)  # Light, thin line

    # Customize the plot
    plt.title('RTT Over Time')
    plt.xlabel('Time (seconds)')
    plt.ylabel('RTT (seconds)')
    plt.xlim(0, 300)  # Set x-axis limit to 0-300 seconds
    plt.ylim(0, max(rtts) * 1.1)  # Set y-axis limit to slightly above max RTT
    plt.grid(True)
    plt.legend(loc='upper right')

    # Save the plot to a file
    try:
        plt.savefig(plot_without_handover_file)
        plt.close()
        print(f"Plot without handover saved as {plot_without_handover_file}")
    except PermissionError:
        print(f"Permission denied: '{plot_without_handover_file}'. Please check the file permissions.")
    except Exception as e:
        print(f"An error occurred while saving the plot: {e}")

    # Plot RTT over resampled time with handover events
    plt.figure(figsize=(12, 6))
    plt.scatter(resampled_timestamps, rtts, s=4, c='blue', alpha=0.6, edgecolors='none', label='RTT measurements')
    plt.plot(resampled_timestamps, rtts, linestyle='-', linewidth=0.3, color='blue', alpha=0.8)  # Light, thin line

    # Read the handover log file
    try:
        handover_times = []
        with open(handover_log, 'r') as file:
            for line in file:
                timestamp = datetime.strptime(line.strip(), '%Y-%m-%d %H:%M:%S.%f %Z')
                handover_times.append(timestamp.timestamp())

        # Normalize handover timestamps using the min_timestamp from the RTT data
        normalized_handover_times = [(timestamp - min_timestamp) for timestamp in handover_times]

        # Scale to the 0-300 seconds range
        resampled_handover_times = [ts / (max_ts - min_ts) * 300 for ts in normalized_handover_times]

        # Add vertical red lines for each resampled handover timestamp
        for ts in resampled_handover_times:
            plt.axvline(x=ts, color='red', linestyle='--', alpha=0.5, label='Handover' if ts == resampled_handover_times[0] else "")
    except FileNotFoundError:
        print(f"File not found: '{handover_log}'. Please check the file path.")
    except Exception as e:
        print(f"An error occurred while processing the handover log file: {e}")

    # Customize the plot
    plt.title('RTT Over Time with Handover Events')
    plt.xlabel('Time (seconds)')
    plt.ylabel('RTT (seconds)')
    plt.xlim(0, 300)  # Set x-axis limit to 0-300 seconds
    plt.ylim(0, max(rtts) * 1.1)  # Set y-axis limit to slightly above max RTT
    plt.grid(True)
    plt.legend(loc='best')

    # Save the plot to a file
    try:
        plt.savefig(plot_with_handover_file)
        plt.close()
        print(f"Plot with handover saved as {plot_with_handover_file}")
    except PermissionError:
        print(f"Permission denied: '{plot_with_handover_file}'. Please check the file permissions.")
    except Exception as e:
        print(f"An error occurred while saving the plot: {e}")

# Main function
def main():
    csv_file = 'rtt_data.csv'
    handover_log = 'handover.log'
    plot_with_handover_file = 'resampled_rtt_with_handover.png'
    plot_without_handover_file = 'resampled_rtt_without_handover.png'
    stats_file_path = 'rtt_stats.txt'
    
    # Read RTT data from CSV
    rtt_data = read_rtt_data(csv_file)
    
    if rtt_data:
        # Plot resampled RTT over time with and without handover events
        resample_and_plot_rtt(rtt_data, handover_log, plot_with_handover_file, plot_without_handover_file, stats_file_path)

if __name__ == "__main__":
    main()
