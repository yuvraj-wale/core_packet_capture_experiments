#!/bin/bash

# Start iperf3 server
iperf3 -s &

# Variables
SERVER_IP="127.0.0.1"
CAPTURE_SCRIPT="/home/yuraj/core_packet_capture_experiments/output"
RESULT_FILE="results.csv"

# Initialize the results file
echo "Rate,Duration,Packets Sent,Packets Received,Packets Captured" > $RESULT_FILE

# Function to run a single test
run_test() {
    local rate=$1
    local duration=$2

    # Start packet capture script and redirect its output to a file
    sudo $CAPTURE_SCRIPT > capture_output.txt 2>&1 &
    CAPTURE_PID=$!

    # Run iperf3 client to generate traffic
    iperf3 -c $SERVER_IP -u -b $rate -t $duration -l 1500 -J > iperf3_output.json

    # Wait for iperf3 to finish
    wait $!

    # Interrupt the packet capture script
    sudo kill -INT $CAPTURE_PID
    wait $CAPTURE_PID

    # Extract packet counts from iperf3 JSON output
    PACKETS_SENT=$(jq .end.sum.packets iperf3_output.json)
    PACKETS_RECEIVED=$(jq .end.sum.lost_packets iperf3_output.json)

    # Extract packet count from the capture script output
    PACKETS_CAPTURED=$(tail -n 1 capture_output.txt | grep -o '[0-9]*')
    PACKETS_CAPTURED=$((PACKETS_CAPTURED - 32))

    # Record the results in CSV file
    echo "$rate,$duration,$PACKETS_SENT,$PACKETS_RECEIVED,$PACKETS_CAPTURED" >> $RESULT_FILE
}

# Run tests for different rates and durations
for rate in 1M 10M 100M 1G; do
    for duration in 10 30 60 100 300; do
        run_test $rate $duration
    done
done

# Stop iperf3 server
pkill iperf3
