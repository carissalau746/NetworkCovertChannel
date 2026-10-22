# Save and Reopen packet capture
from scapy.all import sniff, wrpcap, rdpcap, IP, UDP

packets_read = {}
message = ""
size = None

# Capture Filter and Inspect Packets
def handle(pkt):
    global size
    if IP in pkt and UDP in pkt:
        val = pkt[IP].id
        curr = val >> 8     # Upper: Current point in sequence of bytes
        low = val & 0xFF    # Lower: Encoded Byte

        if curr == 0:
            if size is None:
                size = low
                print("Header: length = ", low)
        else:
            if curr not in packets_read:
                packets_read[curr] = low

def done(pkt):
    return size is not None and len(packets_read) >= size

captured = sniff(
    iface="Software Loopback Interface 1",
    filter="udp port 4600",
    prn=handle,
    stop_filter=done, # Stop once all bytes are collected
    store=True,
    timeout=30,
)

if size is not None:
    message = "".join(chr(packets_read[i]) for i in range(1, size + 1))
    print("Decoded message: ", message)
else:
    print("Failed to decode message")

wrpcap("clau25_covert_channel.pcap", captured)
print("Saved capture to clau25_covert_channel.pcap")