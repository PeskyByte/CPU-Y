import curses
import psutil
import time
import platform

def main(win):
    curses.curs_set(0)
    win.clear()
    
    win.nodelay(True)

    windows = True
    if platform.system() != 'Windows':
        windows = False

    while True:
        win.clear()

        cpu_count = psutil.cpu_count(logical=False)
        cpu_thread = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()
        cpu_percent = psutil.cpu_percent()
        
        cpu_temperatures = "TEMPERATURE READINGS ARE NOT SUPPORTED BY WINDOWS"
        if not windows:
            temperatures = psutil.sensors_temperatures()
            cpu_temperatures = temperatures.get('coretemp') #the intel temperature driver
            if not cpu_temperatures:
                cpu_temperatures = temperatures.get('acpitz') or temperatures.get('k10temp') #amd


        total_virtual_memory = psutil.virtual_memory()[0] / 1024 / 1024 
        available_virtual_memory = psutil.virtual_memory()[1] / 1024 / 1024
        disk_partition = psutil.disk_partitions(all = False)

        battery_percentage = int(psutil.sensors_battery()[0])

        win.addstr("-----CPU-----")
        win.addstr("\nCPU CORES: "+ str(cpu_count))
        win.addstr("\nCPU THREADS: "+ str(cpu_thread))
        win.addstr("\nCPU FREQUENCY: "+ str(int(cpu_freq[0])) + " MHz")
        if windows:
            win.addstr("(FREQUENCY ON WINDOWS ONLY SUPPORTS A FIXED VALUE)")
        win.addstr("\nCPU PERCENTAGE: "+ str(cpu_percent) +"%")
        
        if not windows:
            win.addstr("\nCPU TEMPERATURE: "+ str(cpu_temperatures[0][1]) +" °C")

        win.addstr("\n\n-----MEMORY-----")
        win.addstr("\nTOTAL MEMORY: "+ str(int(total_virtual_memory)) + " MB")
        win.addstr("\nAVAILABLE MEMORY: "+ str(int(available_virtual_memory)) + " MB")
        
        win.addstr("\n\n-----BATTERY-----")
        win.addstr("\nPERCENTAGE: "+ str(battery_percentage) + "%")

        win.addstr("\n\n-----DISK-----")
        if windows:
            numberOfPartitions = 1
            for partition in disk_partition:
                win.addstr("\nPARTITION #" + str(numberOfPartitions))
                win.addstr("\n\tPATH: " + partition[1])
                win.addstr("\n\tFILE SYSTEM: "+ partition[2])
                win.addstr("\n\tTOTAL SPACE: "+ str(int(psutil.disk_usage(partition[0])[0]/1024/1024)) + " MB")
                
                numberOfPartitions += 1


        win.addstr("\n\n***PRESS Q TO EXIT***")

        win.refresh()
        time.sleep(0.8)
        
        key = win.getch()
        if key == ord('q') or key == ord('Q'):
            break
    
if __name__ == "__main__":
    curses.wrapper(main)