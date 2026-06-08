import sys
import csv
from collections import defaultdict
from scapy.all import PcapReader, IP, TCP, UDP

def extraer_features(pcap_file, csv_file):
    # Diccionario para almacenar las estadísticas por IP
    stats = defaultdict(lambda: {
        "count": 0,
        "ports": set(),
        "bytes": 0,
        "first_ts": None,
        "last_ts": None
    })

    print(f"Procesando {pcap_file}...")
    
    # Leer el archivo PCAP
    with PcapReader(pcap_file) as pcap:
        for pkt in pcap:
            if IP not in pkt:
                continue
            
            src_ip = pkt[IP].src
            pkt_len = len(pkt)
            ts = float(pkt.time)

            entry = stats[src_ip]
            entry["count"] += 1
            entry["bytes"] += pkt_len

            if entry["first_ts"] is None:
                entry["first_ts"] = ts
            entry["last_ts"] = ts

            if TCP in pkt:
                entry["ports"].add(pkt[TCP].dport)
            elif UDP in pkt:
                entry["ports"].add(pkt[UDP].dport)

    # Exportar los resultados a CSV
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['ip', 'pps', 'puertos', 'bytes'])
        
        for ip, data in stats.items():
            duration = data["last_ts"] - data["first_ts"]
            # Evitar división por cero si todos los paquetes llegaron en el mismo milisegundo
            pps = data["count"] / duration if duration > 0 else data["count"]
            
            writer.writerow([ip, round(pps, 2), len(data["ports"]), data["bytes"]])
            
    print(f"Extracción completada. Guardado en: {csv_file}\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python3 extraer_features.py <entrada.pcap> <salida.csv>")
    else:
        extraer_features(sys.argv[1], sys.argv[2])