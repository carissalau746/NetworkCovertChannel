# Network Covert Channel

A proof-of-concept covert channel that transmits hidden messages inside the
16-bit IPv4 **Identification** header field — with no application-layer payload —
so the data isn't visible to payload-based traffic inspection. Built with Python
and Scapy.

> **Authorized use only.** This is an educational security project. It was
> developed and tested entirely on the local loopback interface. Only use
> techniques like this on systems and networks you own or are explicitly
> authorized to test.

## How it works

The message is sent one byte per packet. Each packet's 16-bit IP Identification
field is split in half:

- **Upper 8 bits** — a sequence number (the byte's position in the message)
- **Lower 8 bits** — the data byte itself

A header packet (sequence 0) carries the message length in its lower byte, so the
receiver knows when the message is complete. The receiver captures UDP port 4600,
stores each byte keyed by its sequence number, and reassembles the message in
order regardless of arrival order. Duplicate packets are ignored.

This design handles **ordering** (sequence numbers), **completion** (length
header), and **duplication** (dedup by sequence number).

## Usage

Requires an elevated terminal, since raw packet send/capture needs admin
privileges. On Windows, Npcap must be installed (bundled with Wireshark) with
loopback support.

Run in two Administrator terminals, **receiver first**:

python receiver.py
python sender.py


Enter the message at the sender prompt.

## Requirements

- Python 3
- Scapy (`pip install -r requirements.txt`)
- Npcap (Windows, for loopback capture)

## Detection & limitations

**Detectable:** the IP ID values look abnormal — normally random or monotonically
increasing, but here they fall into structured low ranges and increment by about
0x0100 per packet. A monitor could also flag the burst of many tiny payload-less
packets to one port.

**Limitations:** one byte per packet keeps throughput low; the 8-bit sequence
number caps messages at 255 bytes; there's no retransmission, so a dropped packet
breaks reassembly; and any device that rewrites the IP ID field (e.g. NAT)
destroys the hidden data.

## Environment tested

Windows 11, Python 3.14.7, Scapy 2.8.0, loopback interface.