import socket
import multiprocessing
common_ports = [21, 22, 23, 25, 80, 443, 110, 143, 3306, 5432]
def scan_port(target_host, target_port):
    try:
        # Create a socket object
        socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Set a timeout for the connection attempt (adjust as needed)
        socket_obj.settimeout(2)

        # Attempt to connect to the target host and port
        result = socket_obj.connect_ex((target_host, target_port))

        if result == 0:
            print(f"Port {target_port} is open on {target_host}")
        else:
            print(f"Port {target_port} is closed on {target_host}")

        # Close the socket
        socket_obj.close()

    except KeyboardInterrupt:
        print("\nScan terminated by user.")
        exit()
    except socket.gaierror:
        print("Hostname could not be resolved.")
        exit()
    except socket.error:
        print(f"Could not connect to port {target_port} on {target_host} (closed).")

def parallel_port_scan(target_host, target_ports):
    # Create a pool of worker processes
    pool = multiprocessing.Pool(processes=50)  # Adjust the number of processes as needed

    # Use the pool to scan the specified ports in parallel
    pool.starmap(scan_port, [(target_host, port) for port in target_ports])

def main():
    target_host = input("Enter the target host or IP address: ")

    print("Choose an option:")
    print("1. Scan specific ports")
    print("2. Scan common ports")
    print("3. Scan all ports")

    choice = input("Enter your choice (1/2/3): ")

    if choice == '1':
        target_ports = input("Enter the target port(s) to scan (comma-separated, e.g., 80,443): ").split(',')
        target_ports = [int(port.strip()) for port in target_ports]
        parallel_port_scan(target_host, target_ports)
    elif choice == '2':
        parallel_port_scan(target_host, common_ports)
    elif choice == '3':
        all_ports = list(range(1, 65536))  # Scan all possible ports (1-65535)
        parallel_port_scan(target_host, all_ports)
    else:
        print("Invalid choice. Please enter '1', '2', or '3'.")

if __name__ == "__main__":
    main()