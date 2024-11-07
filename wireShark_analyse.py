import pyshark
import pandas as pd

# Load the capture file with the display filter to get sent packets with 'boolean == True'
capture_true = pyshark.FileCapture('//10.171.48.242/Users/Sandeep/Adaptest/ws1.pcapng',
                                   display_filter='eth.src == 00:00:23:39:84:7e && goose.boolean == True')

# Load the capture without the filter for general inspection
capture_all_path = '//10.171.48.242/Users/Sandeep/Adaptest/ws1.pcapng'

# Define GOOSE reference for response signals
response_gocbref = "AA1J1Q01KF1LD0/LLN0$GO$gcb_A_REX_DS_A"

# Initialize variables for tracking timestamps and response times
response_data = []

# Step 1: Extract the timestamps of packets with `boolean == True`
sent_packets = []
for idx, packet in enumerate(capture_true):
    if idx >= 5:  # Limit to 5 samples
        break
    try:
        sniff_time = packet.sniff_time
        sent_packets.append(sniff_time)
        print(f"Sent 'true' signal detected at: {sniff_time}")
    except AttributeError as e:
        print("AttributeError encountered:", e)
        continue

capture_true.close()

# Step 2: Find response packets and calculate response time
for sent_timestamp in sent_packets:
    response_found = False
    capture_all = pyshark.FileCapture(capture_all_path, 
                                      display_filter='goose.gocbRef == "CI868_Ed2_icdLD0/LLN0$GO$new_gcb1" || goose.gocbRef == "AA1J1Q01KF1LD0/LLN0$GO$gcb_A_REX_DS_A"')
    for packet in capture_all:
        try:
            # Skip packets before the sent packet
            if packet.sniff_time <= sent_timestamp:
                continue

            # Check if the packet is a response packet and ensure it's not reused
            if packet.goose.gocbref == response_gocbref and (not response_data or packet.sniff_time > response_data[-1][1]):
                response_timestamp = packet.sniff_time
                response_time = (response_timestamp - sent_timestamp).total_seconds()
                response_data.append([sent_timestamp, response_timestamp, response_time])
                print(f"Response received at: {response_timestamp} with response time {response_time:.6f} seconds")
                response_found = True
                break  # Move to the next `true` signal as soon as we find the first response

        except AttributeError as e:
            print("AttributeError encountered:", e)
            continue

    if not response_found:
        print(f"No response found for sent packet at: {sent_timestamp}")

    capture_all.close()

# Step 3: Calculate average response time
if response_data:
    avg_response_time = sum([row[2] for row in response_data]) / len(response_data)
    print(f"\nAverage Response Time for 5 samples: {avg_response_time:.6f} seconds")

# Step 4: Save response data to CSV
response_df = pd.DataFrame(response_data, columns=["Sent Timestamp", "Response Timestamp", "Response Time (s)"])
csv_filename = "goose_response_times.csv"
response_df.to_csv(csv_filename, index=False)
print(f"Response data saved to {csv_filename}")
