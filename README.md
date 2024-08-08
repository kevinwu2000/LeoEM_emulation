# LeoEM Modification

This repository contains modifications to the Low Earth Orbit Emulator (LeoEM) for studying throughput and round-trip time (RTT) in Low Earth Orbit (LEO) networks. The modifications focus testing throughput and RTT of LEO, and comparing them of SaTCP with traditional TCP.

## Running the Emulation

Follow these steps to set up and run the emulation:

1. **Start the POX Learning Switch:**

   Run the following command in the background:
   ```bash
   python3 ~/pox/pox.py misc.learning_switch
   ```

2. **Prepare the Mininet Environment:**

    Clean up any existing Mininet configurations:
    ```bash
    sudo mn -c
    ```

3. **Choose Your Route and Run the Emulator:**

    ```bash
    cd LeoEM/emulation_stage/
    ```

    Example:
    ```bash
    sudo python3 emulator.py Starlink_SD_Shanghai_15_ISL_path.log
    ```

## After emulation

**Plotting throughput**

1. **Put files in correct position:**

    Put `cycle_time.log`, `handover.log`, `throughput_routeName.log` into `/throughput_handover`

2. **Modify plot_thoughput_handover.py**

    Change the **throughput_file_path** variable to the correct log file name.

3. **Plotting**

    ```bash
    cd thoughput_handover
    sudo python3 plot_thoughput_handover.py
    ```

4. **Result**

    It will generate 2 plots: `thorughput_over_time_with_handover.png` and `thorughput_over_time_no_handover.png`.
    
    Also a txt file `throughput_stats.txt` with avg, max and min throughput.

**Plotting RTT**

1. **Put files in correct position:**

    Put `iperf_traffic.pcap` and `handover.log`(same as throughput plotting) into `/rtt_handover`.

2. **Run script to generate CSV file**

    ```bash
    cd rtt_handover
    ./generate_rtt_csv.sh
    ```
    After running, it will generate `rtt_data.csv` for plotting.

3. **Plotting**

    ```bash
    sudo python3 plot_rtt_handover.py
    ```

4. **Result**

    It will generate 2 plots: `resampled_rtt_with_handover.png` and `resampled_rtt_without_handover.png`.
    
    Also a txt file `rtt_stats.txt` with avg, max and min RTT.