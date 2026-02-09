# Характеристики технологий доступа к сети Internet

| **Технология** | **Краткое описание** | **Пропускная способность** | **Задержка (latency)** |
|---|---|---|---|
| **ISDN** | Integrated Services Digital Network - цифровая телефонная сеть для передачи голоса и данных по медным линиям | BRI: 128 Kbps (2×64 Kbps)<br>PRI: 1.544 Mbps (T1) или 2.048 Mbps (E1) | 20-40 ms | 
| **ADSL** | Asymmetric Digital Subscriber Line - асимметричная технология по телефонным линиям (download > upload) | Download: 1-24 Mbps<br>Upload: 64 Kbps - 3.5 Mbps | 10-50 ms |
| **DOCSIS** | Data Over Cable Service Interface Specification - передача данных по коаксиальному кабелю (кабельное ТВ) | DOCSIS 3.0: до 1 Gbps<br>DOCSIS 3.1: до 10 Gbps<br>DOCSIS 4.0: до 10 Gbps (симметрично) | 5-30 ms |
| **Ethernet 10 Mbps** | Базовый стандарт локальных сетей (10BASE-T) | 10 Mbps | < 1 ms (LAN) |
| **Ethernet 100 Mbps** | Fast Ethernet (100BASE-TX) | 100 Mbps | < 1 ms (LAN) |
| **Ethernet 1 Gbps** | Gigabit Ethernet (1000BASE-T/SX/LX) | 1 Gbps | < 0.5 ms (LAN) |
| **Ethernet 10 Gbps** | 10 Gigabit Ethernet (10GBASE-T/SR/LR) | 10 Gbps | < 0.1 ms (LAN) |
| **Ethernet 40 Gbps** | 40 Gigabit Ethernet (40GBASE-SR4/LR4) | 40 Gbps | < 0.05 ms (LAN) | IEEE 802.3ba (не RFC) |
| **Ethernet 100 Gbps** | 100 Gigabit Ethernet (100GBASE-SR10/LR4) | 100 Gbps | < 0.05 ms (LAN) |
| **PON (GPON)** | Passive Optical Network - оптоволоконная сеть с пассивными разветвителями для FTTH | GPON: 2.5 Gbps down / 1.25 Gbps up<br>XG-PON: 10 Gbps down / 2.5 Gbps up<br>XGS-PON: 10 Gbps (симметрично) | 1-5 ms |
| **WiFi 802.11b** | Беспроводная сеть 2.4 GHz (первое поколение массового WiFi) | до 11 Mbps | 5-10 ms |
| **WiFi 802.11g** | 2.4 GHz с улучшенной модуляцией (OFDM) | до 54 Mbps | 5-10 ms |
| **WiFi 802.11n** | Dual-band (2.4/5 GHz), MIMO, первый "быстрый" WiFi | до 600 Mbps (4×4 MIMO) | 5-15 ms |
| **WiFi 802.11a** | 5 GHz, параллельно с 802.11b, меньше помех | до 54 Mbps | 5-10 ms |
| **WiFi 802.11h** | 5 GHz с управлением мощностью и выбором канала (DFS/TPC) | до 54 Mbps | 5-10 ms |
| **WiFi 802.11ac** | WiFi 5, только 5 GHz, MU-MIMO, широкие каналы | до 6.9 Gbps (8×8 MIMO, 160 MHz) |
| **WiFi 802.11ax** | WiFi 6/6E, OFDMA, лучше в плотных сетях, 2.4/5/6 GHz | до 9.6 Gbps (теоретически) | 5-20 ms |
| **WiMAX** | Worldwide Interoperability for Microwave Access - беспроводная сеть для широкой зоны покрытия | IEEE 802.16d: до 75 Mbps (фиксированный)<br>IEEE 802.16e: до 40 Mbps (мобильный) | 25-50 ms |
| **3G (UMTS/HSPA)** | Third Generation - мобильная сеть третьего поколения | UMTS: 384 Kbps - 2 Mbps<br>HSPA: до 14.4 Mbps<br>HSPA+: до 42 Mbps | 100-500 ms |
| **4G (LTE/LTE-A)** | Fourth Generation - Long Term Evolution | LTE: до 300 Mbps<br>LTE-Advanced: до 1 Gbps<br>LTE-Advanced Pro: до 3 Gbps | 20-70 ms |
| **5G (NR)** | Fifth Generation - New Radio, mmWave, network slicing | Sub-6 GHz: до 1-2 Gbps<br>mmWave: до 10-20 Gbps (пиковая) | 1-10 ms (Ultra-Reliable Low Latency) |
| **VSAT** | Very Small Aperture Terminal - спутниковая связь через геостационарные спутники (GEO) | 1-100 Mbps (зависит от тарифа) | 500-700 ms (из-за высоты орбиты ~36000 км) |
| **HTS (High Throughput Satellite)** | Спутники с высокой пропускной способностью (multi-beam, Ka-band) | 25-300 Mbps (для пользователей)<br>Суммарная: до 1 Tbps на спутник |

