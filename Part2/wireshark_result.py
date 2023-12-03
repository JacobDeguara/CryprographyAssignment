from scapy.all import *
from collections import Counter

import pandas as pd

# Encripted table
bytelist_Encrypted = list()
scapy_cap = rdpcap("Part2/WireShark_Capture/EncryptedTextCommunication.pcapng")

for packet in scapy_cap:
    bytelist_Encrypted.append(bytes(packet["TCP"].payload))

bytes_Encrypted = b"".join(bytelist_Encrypted)
decoded_string = str(bytes_Encrypted, encoding="iso8859-1")

res = Counter(decoded_string)
Encryptedlist = list()
for element in res.keys():
    Encryptedlist.append([res.get(element), str(element.encode("iso8859-1"))])

df = pd.DataFrame(Encryptedlist)

df.to_excel("export_Encrypted_Frequency.xlsx", index=False)
df.to_latex("export_Encrypted_Frequency.tex")

bytelist_Plain = list()
scapy_cap = rdpcap("Part2/WireShark_Capture/PlainTextCommunication.pcapng")

for packet in scapy_cap:
    bytelist_Plain.append(bytes(packet["TCP"].payload))

bytes_Plain = b"".join(bytelist_Plain)
decoded_string = str(bytes_Plain, encoding="iso8859-1")

res = Counter(decoded_string)
Plainlist = list()
for element in res.keys():
    Plainlist.append([res.get(element), str(element.encode("iso8859-1"))])

df = pd.DataFrame(Plainlist)

df.to_excel("export_Plain_Frequency.xlsx", index=False)
df.to_latex("export_Plain_Frequency.tex")
