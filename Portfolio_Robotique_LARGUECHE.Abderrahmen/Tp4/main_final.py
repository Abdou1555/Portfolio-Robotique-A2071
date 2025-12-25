import uasyncio as asyncio
from machine import UART, Pin

class BluetoothHC05:

    def __init__(self, tx_pin, rx_pin, led_pin, motor_pin, baudrate=9600):
        self.uart = UART(0, baudrate=baudrate, tx=Pin(tx_pin), rx=Pin(rx_pin))
        self.led = Pin(led_pin, Pin.OUT)
        self.motor = Pin(motor_pin, Pin.OUT)

    async def send_data(self, data):

        message = 'START:{}:END\n'.format(data)
        self.uart.write(message)
        await asyncio.sleep(0)

    def process_command(self, command):

        if command == 'LED_ON':
            self.led.value(1)
            print('LED turned ON')
        elif command == 'LED_OFF':
            self.led.value(0)
            print('LED turned OFF')
        elif command == 'MOTOR_START':
            self.motor.value(1)
            print('Motor started')
        elif command == 'MOTOR_STOP':
            self.motor.value(0)
            print('Motor stopped')
        else:
            print('Unknown command:', command)

    async def receive_data(self):

        while True:
            if self.uart.any():
                message = self.uart.readline()
                # Vérification du protocole START/END
                if message.startswith(b'START:') and message.endswith(b':END\n'):
                    return message[6:-5] # Extraction des données
            await asyncio.sleep(0)

    async def listen(self):

        while True:
            data = await self.receive_data()
            if data:
                self.process_command(data.decode())
            await asyncio.sleep(0)

# PROGRAMME
async def main():
    

    bluetooth = BluetoothHC05(tx_pin=0, rx_pin=1, led_pin=13, motor_pin=6)
    

    asyncio.create_task(bluetooth.listen())
    
    while True:
         
        await asyncio.sleep(1)

# Démarrage
if __name__ == '__main__':
    asyncio.run(main())