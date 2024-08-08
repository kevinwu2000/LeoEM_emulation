#!/bin/bash
pcap_file="iperf_traffic.pcap"
output_csv="rtt_data.csv"

tshark -r "$pcap_file" -T fields -e frame.time_epoch -e tcp.analysis.ack_rtt -Y "tcp.analysis.ack_rtt" -E header=y -E separator=, > "$output_csv"