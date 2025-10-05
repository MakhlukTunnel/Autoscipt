#!/usr/bin/python
import socket, threading, select, signal, sys, time, getopt, traceback, json, typing
from typing import List, Tuple

# Defaults
DEFAULT_BIND_ADDR = '0.0.0.0'
DEFAULT_BIND_PORT = 8880
DEFAULT_LISTEN_HOST = '127.0.0.1'
DEFAULT_LISTEN_PORT = 22
BUFFER_SIZE = 4096 * 4
TIMEOUT = 60
RESPONSE = 'HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n\r\n'

def printlog(*args, **kwargs):
    print(*args, **kwargs)
    sys.stdout.flush()

class Config:
    def __init__(self):
        self.bindings: List[Binding] = []
        self.listenings: List[Listening] = []
        self.buffer = BUFFER_SIZE
        self.timeout = TIMEOUT
        self.response = RESPONSE

class Binding:
    def __init__(self, address: str, port: int):
        self.address = address
        self.port = port

class Listening:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

def parse_indexed_arg(arg: str) -> Tuple[int, str, int]:
    """Parse index:address:port format"""
    parts = arg.split(':', 2)
    if len(parts) != 3:
        raise ValueError(f"Invalid format: {arg}")
    return int(parts[0]), parts[1], int(parts[2])

def load_config(config_file: str, cmd_bind: list, cmd_listen: list) -> Config:
    """Load configuration with index-based override"""
    config = Config()
    
    # Load from JSON file
    if config_file:
        try:
            with open(config_file, 'r') as f:
                data = json.load(f)
                config.bindings = [Binding(b['address'], b['port']) for b in data['bindings']]
                config.listenings = [Listening(l['host'], l['port']) for l in data['listenings']]
                config.buffer = data.get('buffer', BUFFER_SIZE)
                config.response = data.get('response', RESPONSE)
        except Exception as e:
            printlog(f"Config error: {e}")
            sys.exit(1)

    # Process command line bindings
    for index, addr, port in cmd_bind:
        while len(config.bindings) <= index:
            config.bindings.append(Binding(DEFAULT_BIND_ADDR, DEFAULT_BIND_PORT))
        config.bindings[index] = Binding(addr, port)

    # Process command line listenings
    for index, host, port in cmd_listen:
        while len(config.listenings) <= index:
            config.listenings.append(Listening(DEFAULT_LISTEN_HOST, DEFAULT_LISTEN_PORT))
        config.listenings[index] = Listening(host, port)

    return config

class Server(threading.Thread):
    def __init__(self, index: int, binding: Binding, listening: Listening, config: Config):
        super().__init__()
        self.index = index
        self.binding = binding
        self.listening = listening
        self.config = config
        self.running = False
        self.lock = threading.Lock()

    def run(self):
        """Main server loop"""
        self.sock = socket.socket(socket.AF_INET)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(2)
        self.sock.bind((self.binding.address, self.binding.port))
        self.sock.listen(5)
        self.running = True
        
        printlog(f"[*] Binding {self.index}: {self.binding.address}:{self.binding.port} -> {self.listening.host}:{self.listening.port}")

        try:
            while self.running:
                try:
                    client_sock, addr = self.sock.accept()
                    client_sock.setblocking(True)
                    self.handle_connection(client_sock, addr)
                except socket.timeout:
                    continue
        finally:
            self.running = False
            self.sock.close()

    def handle_connection(self, client_sock: socket.socket, addr: tuple):
        """Handle new connection"""
        handler = ConnectionHandler(client_sock, addr, self.listening, self.config)
        handler.start()

    def stop(self):
        """Stop the server"""
        self.running = False

class ConnectionHandler(threading.Thread):
    def __init__(self, client_sock: socket.socket, addr: tuple, listening: Listening, config: Config):
        super().__init__()
        self.client = client_sock
        self.addr = addr
        self.listening = listening
        self.config = config
        self.target: socket.socket = None
        self.log = f"{addr[0]}:{addr[1]}"

    def close(self):
        """Close connections"""
        try: self.client.close()
        except: pass
        try: self.target.close()
        except: pass

    def run(self):
        """Handle proxy logic"""
        try:
            data = self.client.recv(self.config.buffer)
            if not data:
                return

            # Try to get target from headers
            target_host, target_port = self.parse_headers(data)
            
            # If no header, use default listening for this binding
            if not target_host:
                target_host = self.listening.host
                target_port = self.listening.port

            self.connect_target(target_host, target_port)
            self.client.send(self.config.response.encode())
            self.tunnel()

        except Exception as e:
            printlog(f"[-] {self.log} - Error: {str(e)}")
        finally:
            self.close()

    def parse_headers(self, data: bytes) -> Tuple[str, int]:
        """Parse X-Real-Host header"""
        try:
            headers = data.decode().split('\r\n')
            for h in headers:
                if h.lower().startswith('x-real-host:'):
                    host_port = h.split(': ', 1)[1].strip()
                    if ':' in host_port:
                        host, port = host_port.split(':', 1)
                        return (host, int(port))
                    return (host_port, self.listening.port)
        except:
            pass
        return (None, None)

    def connect_target(self, host: str, port: int):
        """Connect to target server"""
        self.target = socket.socket(socket.AF_INET)
        self.target.connect((host, port))
        self.log += f" -> {host}:{port}"
        printlog(f"[+] {self.log}")

    def tunnel(self):
        """Forward data between client and target with optimized performance"""
        sockets = [self.client, self.target]
        buffer_size = self.config.buffer
        client_buffer = bytearray(buffer_size)
        target_buffer = bytearray(buffer_size)
        
        client_mem = memoryview(client_buffer)  # Zero-copy buffer
        target_mem = memoryview(target_buffer)
    
        last_activity = time.time()
        timeout = self.config.timeout
        error = False
    
        # Set non-blocking mode
        self.client.setblocking(False)
        self.target.setblocking(False)
    
        while True:
            try:
                r, w, e = select.select(sockets, sockets, sockets, timeout)
                # Jika ada error di socket
                if e:
                    error = True
                    break

                now = time.time()
                if now - last_activity > timeout:
                    break  # Hentikan koneksi jika timeout

                if r:
                    for sock in r:
                        if sock is self.client:
                            try:
                                recv_len = self.client.recv_into(client_mem, buffer_size)
                                if recv_len:
                                    last_activity = now
                                    self.target.sendall(client_mem[:recv_len])
                                else:
                                    break
                            except BlockingIOError:
                                continue
                        elif sock is self.target:
                            try:
                                recv_len = self.target.recv_into(target_mem, buffer_size)
                                if recv_len:
                                    last_activity = now
                                    self.client.sendall(target_mem[:recv_len])
                                else:
                                    break
                            except BlockingIOError:
                                continue

                if not r and not w:
                    break  # Jika tidak ada data masuk, keluar loop

            except Exception as e:
                printlog(f"[-] {self.log} - Tunnel error: {str(e)}")
                error = True
                break

        if error:
            self.close()

def print_usage():
    printlog("Index-Based Proxy")
    printlog("Usage:")
    printlog("  proxy.py -f config.json")
    printlog("  proxy.py -b <index:addr:port> -l <index:host:port>")
    printlog("\nExamples:")
    printlog("  proxy.py -f config.json")
    printlog("  proxy.py -b 0:0.0.0.0:80 -l 0:127.0.0.1:22")
    printlog("  proxy.py -b 1:0.0.0.0:8080 -l 1:127.0.0.1:143")

def parse_args():
    try:
        opts, _ = getopt.getopt(sys.argv[1:], "hf:b:l:", ["help", "file=", "bind=", "listen="])
    except getopt.GetoptError as e:
        printlog(f"Error: {str(e)}")
        print_usage()
        sys.exit(2)

    config_file = ""
    cmd_bind = []
    cmd_listen = []

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print_usage()
            sys.exit()
        elif opt in ('-f', '--file'):
            config_file = arg
        elif opt in ('-b', '--bind'):
            cmd_bind.append(parse_indexed_arg(arg))
        elif opt in ('-l', '--listen'):
            cmd_listen.append(parse_indexed_arg(arg))

    return config_file, cmd_bind, cmd_listen

def main():
    config_file, cmd_bind, cmd_listen = parse_args()
    config = load_config(config_file, cmd_bind, cmd_listen)

    printlog("\n[==== Proxy Configuration ====]")
    printlog(f"Buffer size: {config.buffer}")
    printlog("\nBindings:")
    for i, b in enumerate(config.bindings):
        printlog(f"  [{i}] {b.address}:{b.port}")
    printlog("\nListenings:")
    for i, l in enumerate(config.listenings):
        printlog(f"  [{i}] {l.host}:{l.port}")
    printlog("[=============================]\n")

    # Start servers for each binding
    servers = []
    for i, binding in enumerate(config.bindings):
        listening = config.listenings[i] if i < len(config.listenings) else Listening(
            DEFAULT_LISTEN_HOST, 
            DEFAULT_LISTEN_PORT
        )
        
        server = Server(i, binding, listening, config)
        server.start()
        servers.append(server)

    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        printlog("\n[!] Stopping servers...")
        for server in servers:
            server.stop()

if __name__ == '__main__':
    main()