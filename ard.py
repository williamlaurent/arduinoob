import serial
import subprocess
import os

class ArduinoPentestBot:
    def __init__(self, port, baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.arduino = None
        self.connected = False

    def connect(self):
        try:
            self.arduino = serial.Serial(self.port, self.baudrate, timeout=1)
            self.connected = True
            print(f"Connected to Arduino on port {self.port}")
        except serial.SerialException as e:
            print(f"Failed to connect: {e}")
            self.connected = False

    def disconnect(self):
        if self.connected:
            self.arduino.close()
            self.connected = False
            print("Disconnected from Arduino")

    def send_command(self, command):
        if self.connected:
            self.arduino.write(command.encode())
            response = self.arduino.readline().decode().strip()
            print(f"Sent: {command}\nReceived: {response}")
            return response
        else:
            print("Not connected to Arduino")
            return None

    def scan_for_ports(self):
        ports = []
        for port in serial.tools.list_ports.comports():
            ports.append(port.device)
        return ports

    def compile_arduino_sketch(self, sketch_path):
        if not os.path.exists(sketch_path):
            print("Sketch path does not exist")
            return

        try:
            subprocess.run(["arduino-cli", "compile", "--fqbn", "arduino:avr:uno", sketch_path])
            print("Sketch compiled successfully")
        except subprocess.CalledProcessError as e:
            print(f"Failed to compile sketch: {e}")

    def upload_arduino_sketch(self, sketch_path):
        if not os.path.exists(sketch_path):
            print("Sketch path does not exist")
            return

        try:
            subprocess.run(["arduino-cli", "upload", "--fqbn", "arduino:avr:uno", "--port", self.port, sketch_path])
            print("Sketch uploaded successfully")
        except subprocess.CalledProcessError as e:
            print(f"Failed to upload sketch: {e}")

if __name__ == "__main__":
    bot = ArduinoPentestBot(port="COM3")  # Ganti COM3 dengan port Arduino Anda
    bot.connect()

    # Contoh penggunaan
    bot.send_command("Hello Arduino")

    bot.disconnect()
