from machine import Pin, I2C, PWM
from mfrc522 import MFRC522
import ssd1306
import time


# 1. CONFIGURATION 

# RFID (SPI0)
RST_PIN = 0
SS_PIN = 1
SCK_PIN = 2
MOSI_PIN = 3
MISO_PIN = 4

# LED RGB
PIN_RED   = 13
PIN_GREEN = 12
PIN_BLUE  = 11

# OLED
OLED_SDA = 20
OLED_SCL = 21

# 2. INITIALISATION
print("--- Démarrage Contrôle d'Accès RFID ---")

# a. LED RGB
pwm_r = PWM(Pin(PIN_RED)); pwm_r.freq(1000)
pwm_g = PWM(Pin(PIN_GREEN)); pwm_g.freq(1000)
pwm_b = PWM(Pin(PIN_BLUE)); pwm_b.freq(1000)

def set_color(r, g, b):
    pwm_r.duty_u16(65535 - r)
    pwm_g.duty_u16(65535 - g)
    pwm_b.duty_u16(65535 - b)

# État initial : Bleu (Attente)
set_color(0, 0, 65535)

# b. OLED
oled = None
try:
    i2c = I2C(0, sda=Pin(OLED_SDA), scl=Pin(OLED_SCL), freq=400000)
    oled = ssd1306.SSD1306_I2C(128, 64, i2c)
    oled.fill(0); oled.text("Systeme RFID", 0, 0); oled.show()
    print("OLED OK")
except:
    print("Erreur OLED")

# c. RFID
try:
    reader = MFRC522(spi_id=0, sck=2, miso=4, mosi=3, cs=1, rst=0)
    print("Lecteur RFID OK")
except Exception as e:
    print("Erreur RFID:", e)

# LISTE DES BADGES AUTORISÉS
authorized_tags = [ "0x12ac3203" ] 

# 3. BOUCLE PRINCIPALE
print("Prêt. Passez un badge...")

while True:
    reader.init()
    (stat, tag_type) = reader.request(reader.REQIDL)
    
    if stat == reader.OK:
        (stat, uid) = reader.SelectTagSN()
        
        if stat == reader.OK:
            uid_hex = "0x%02x%02x%02x%02x" % (uid[0], uid[1], uid[2], uid[3])
            print("Badge Lu :", uid_hex)
            
            if uid_hex in authorized_tags:
                # ACCES AUTORISÉ (Vert)
                print(">>> ACCES AUTORISE")
                set_color(0, 65535, 0)
                if oled:
                    oled.fill(0)
                    oled.text("ACCES OK", 0, 0)
                    oled.text(uid_hex, 0, 20)
                    oled.show()
            else:
                # ACCES REFUSÉ (Rouge)
                print(">>> ACCES REFUSE")
                set_color(65535, 0, 0)
                if oled:
                    oled.fill(0)
                    oled.text("ACCES REFUSE", 0, 0)
                    oled.text(uid_hex, 0, 20)
                    oled.show()
            
            time.sleep(2)
            
            # Retour à l'état d'attente (Bleu)
            set_color(0, 0, 65535)
            if oled:
                oled.fill(0)
                oled.text("Pret...", 0, 0)
                oled.show()