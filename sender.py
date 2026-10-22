from scapy.all import IP, UDP, Raw, send

# Capture Input
secret = input("Secret text: ")

# Encode Message
data = secret.encode()
n = len(data)  # Note size of data --> receiver is told how many packets (1 pckt/byte) should be read

# Send header packet - tell receiver length of message
header_id = (0 << 8) | n
send(IP(dst="127.0.0.1", id=(0 << 8 | n)) / UDP(sport=4600, dport=4600), verbose = False);
print(f"Header: length={n} id={(0 << 8) | n}")

# Embed data in Packets; upper half = curr, lower byte = data
for i, b in enumerate(data):
    curr = i + 1
    id_value = (curr << 8) | b 
    send(IP(dst="127.0.0.1", id=id_value) / UDP(sport=4600, dport=4600), verbose = False);
    print(f"curr={curr} byte = {b} ('{chr(b)}') id={id_value}")