from machine import Pin, ADC, I2C, PWM
import time
from stepmotor import FullStepMotor
from servo import Servo
from ssd1306 import SSD1306_I2C

# CONFIGURATION BREADBOARD

# MOTEUR PAS À PAS
IN1 = 14; IN2 = 17; IN3 = 25; IN4 = 27

# SERVOMOTEUR
PIN_SERVO = 16

# JOYSTICK
PIN_VRX = 26  # Axe X 
PIN_VRY = 27  # Axe Y 
PIN_SW  = 22  # Bouton

# LED RGB 
PIN_RED = 13; PIN_GREEN = 12; PIN_BLUE = 11

# OLED 
OLED_SDA = 0; OLED_SCL = 1


print("--- TP3 : Moteurs (Breadboard) ---")

# 1. Servo
try:
    my_servo = Servo(PIN_SERVO)
    print("Servo OK")
except:
    print("Erreur Servo (Vérifier servo.py)")

# 2. Stepper
try:
    stepper = FullStepMotor.frompins(IN1, IN2, IN3, IN4)
    stepper.stepms = 5  
    print("Stepper OK")
except:
    print("Erreur Stepper (Vérifier stepmotor.py)")

# 3. Joystick
joy_x = ADC(Pin(PIN_VRX))
joy_y = ADC(Pin(PIN_VRY))
btn_rst = Pin(PIN_SW, Pin.IN, Pin.PULL_UP)

# 4. LED RGB
pwm_r = PWM(Pin(PIN_RED)); pwm_r.freq(1000)
pwm_g = PWM(Pin(PIN_GREEN)); pwm_g.freq(1000)
pwm_b = PWM(Pin(PIN_BLUE)); pwm_b.freq(1000)

def set_led(r, g, b): 
    pwm_r.duty_u16(65535 - r)
    pwm_g.duty_u16(65535 - g)
    pwm_b.duty_u16(65535 - b)

# 5. OLED
oled = None
try:
    i2c = I2C(0, sda=Pin(OLED_SDA), scl=Pin(OLED_SCL), freq=400000)
    oled = SSD1306_I2C(128, 64, i2c)
    oled.fill(0); oled.text("TP3 Ready", 0, 0); oled.show()
except:
    print("Erreur OLED")

# BOUCLE PRINCIPALE
print("Go! Axe X = Servo, Axe Y = Stepper")
while True:
    # 1. GESTION SERVO
    val_x = joy_x.read_u16()
    angle = int(val_x / 65535 * 180) 
    
    if 'my_servo' in locals():
        my_servo.set_angle(angle)

    if angle < 60:
        set_led(0, 65535, 0)   # Vert 
    elif angle < 120:
        set_led(65535, 65535, 0) # Jaune 
    else:
        set_led(65535, 0, 0)   # Rouge

    # 2. GESTION STEPPER 
    val_y = joy_y.read_u16()
    step_status = "Stop"
    
    if 'stepper' in locals():
        if val_y > 50000:
            stepper.step(20)
            step_status = ">>>"
        elif val_y < 15000:
            stepper.step(-20)
            step_status = "<<<"
            
        # Bouton Reset Position
        if btn_rst.value() == 0:
            stepper.reset()
            step_status = "Reset 0"

    # 3. AFFICHAGE OLED
    if oled:
        oled.fill(0)
        oled.text(f"Servo: {angle} deg", 0, 0)
        if 'stepper' in locals():
            oled.text(f"Step Pos: {stepper.pos}", 0, 20)
        oled.text(f"Mvt: {step_status}", 0, 40)
        oled.show()