import matplotlib.pyplot as plt
import re
import pandas as pd
import numpy as np
from datetime import datetime, timezone

# File paths
throughput_file_path = "throughput_Starlink_SD_Shanghai_15_ISL_path.log"
handover_log_path = "handover.log"
cycle_time_log_path = "cycle_time.log"
output_stats_file_path = "throughput_stats.txt"

# Define the time range for the plot (in seconds)
time_range = 300

# Initialize lists to store time and bitrate values
time_intervals = []
bitrates = []

# Step 1: Parse the throughput log file
try:
    with open(throughput_file_path, 'r') as file:
        for line in file:
            match = re.search(r'\[\s*\d+\]\s+(\d+\.\d+)-(\d+\.\d+)\s+sec\s+\d+\.\d+\s+MBytes\s+(\d+\.\d+)\s+Mbits/sec', line)
            if match:
                start_time = float(match.group(1))
                bitrate = float(match.group(3))
                time_intervals.append(start_time)
                bitrates.append(bitrate)
except FileNotFoundError:
    print(f"Error: The file {throughput_file_path} was not found.")
except Exception as e:
    print(f"Error: An error occurred while processing the file. {e}")

# Step 2: Resample the throughput data to fit the specified time range
time_intervals = np.array(time_intervals)
bitrates = np.array(bitrates)

# Find the maximum time in the data to determine the resampling factor
max_time = time_intervals[-1]

# Create new time intervals for the specified time range
resampled_time_intervals = np.linspace(0, max_time, time_range)

# Resample the bitrates using interpolation
resampled_bitrates = np.interp(resampled_time_intervals, time_intervals, bitrates)

# Normalize the resampled time intervals to be between 0 and 300 seconds
normalized_time_intervals = np.linspace(0, time_range, time_range)

# Step 3: Calculate average and maximum throughput for the resampled data
average_throughput = np.mean(resampled_bitrates)
max_throughput = np.max(resampled_bitrates)
min_throughput = np.min(resampled_bitrates)

# Write the statistics to a text file
try:
    with open(output_stats_file_path, 'w') as stats_file:
        stats_file.write(f"Average Throughput: {average_throughput:.2f} Mbits/sec\n")
        stats_file.write(f"Maximum Throughput: {max_throughput:.2f} Mbits/sec\n")
        stats_file.write(f"Minimum Throughput: {min_throughput:.2f} Mbits/sec\n")
except Exception as e:
    print(f"Error: An error occurred while writing the statistics file. {e}")

# Step 4: Parse the handover log file and convert timestamps to the relative format
timestamps = []

# Step 4.1: Read the cycle_time.log to get the first cycle timestamp
try:
    with open(cycle_time_log_path, 'r') as file:
        for line in file:
            match = re.search(r'Cycle 1:\s+(\d+-\d+-\d+\s+\d+:\d+:\d+)', line)
            if match:
                first_cycle_timestamp = datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S')
                # Make the timestamp timezone-aware
                first_cycle_timestamp = first_cycle_timestamp.replace(tzinfo=timezone.utc)
                break
except FileNotFoundError:
    print(f"Error: The file {cycle_time_log_path} was not found.")
except Exception as e:
    print(f"Error: An error occurred while processing the file {cycle_time_log_path}. {e}")

# Step 4.2: Read the handover log file to get the handover timestamps
try:
    with open(handover_log_path, 'r') as file:
        for line in file:
            timestamp = datetime.strptime(line.strip(), '%Y-%m-%d %H:%M:%S.%f %Z')
            # Ensure the timestamp is timezone-aware
            if timestamp.tzinfo is None:
                timestamp = timestamp.replace(tzinfo=timezone.utc)
            # Normalize the timestamp to start from the first cycle timestamp
            normalized_time = (timestamp - first_cycle_timestamp).total_seconds()
            # Scale the normalized timestamps to fit the 0-300 seconds range
            scaled_time = normalized_time / max_time * time_range
            timestamps.append(scaled_time)
except FileNotFoundError:
    print(f"Error: The file {handover_log_path} was not found.")
except Exception as e:
    print(f"Error: An error occurred while processing the handover log file. {e}")

# Step 5: Plot the resampled throughput data without handover events
plt.figure(figsize=(10, 5))
plt.plot(normalized_time_intervals, resampled_bitrates, label='Throughput (Mbits/sec)')
plt.title('Throughput Over Time')
plt.xlabel('Time (seconds)')
plt.ylabel('Bitrate (Mbits/sec)')
plt.grid(True)
plt.legend()
output_file_no_handover = 'throughput_over_time_no_handover.png'
plt.savefig(output_file_no_handover)
plt.show()
print(f"Plot without handover saved as {output_file_no_handover}")

# Step 6: Plot the resampled throughput data with handover events
plt.figure(figsize=(10, 5))
plt.plot(normalized_time_intervals, resampled_bitrates, label='Throughput (Mbits/sec)')

# Add vertical red lines for each scaled timestamp within the time range
for ts in timestamps:
    if ts <= time_range:
        plt.axvline(x=ts, color='red', linestyle='--', alpha=0.5, label='Handover' if ts == timestamps[0] else "")

# Customize the plot
plt.title('Throughput Over Time with Handover Events')
plt.xlabel('Time (seconds)')
plt.ylabel('Bitrate (Mbits/sec)')
plt.grid(True)
plt.legend(loc='best')
output_file_with_handover = 'throughput_over_time_with_handover.png'
plt.savefig(output_file_with_handover)
plt.show()
print(f"Plot with handover saved as {output_file_with_handover}")

# Print the statistics file output
print(f"Statistics saved as {output_stats_file_path}")
