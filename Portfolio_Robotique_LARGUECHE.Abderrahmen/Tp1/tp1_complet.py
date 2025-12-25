from machine import Pin, ADC, PWM, I2C, Timer
import time
import ssd1306

PIN_BLUE  = 11
PIN_GREEN = 12
PIN_RED   = 13

PIN_VRX = 27
PIN_VRY = 26
PIN_SW  = 22

OLED_SDA = 0
OLED_SCL = 1


# 1. LED RGB
pwm_r = PWM(Pin(PIN_RED))
pwm_g = PWM(Pin(PIN_GREEN))
pwm_b = PWM(Pin(PIN_BLUE))
pwm_r.freq(1000); pwm_g.freq(1000); pwm_b.freq(1000)

# 2. Joystick
adc_x = ADC(Pin(PIN_VRX))
adc_y = ADC(Pin(PIN_VRY))
btn   = Pin(PIN_SW, Pin.IN, Pin.PULL_UP)

# 3. OLED
oled = None
try:
    i2c = I2C(0, sda=Pin(OLED_SDA), scl=Pin(OLED_SCL), freq=400000)
    oled = ssd1306.SSD1306_I2C(128, 64, i2c)
except:
    print("Erreur OLED")


mode = 0  
last_btn_val = 1
last_time = 0


def set_color(r, g, b):
    pwm_r.duty_u16(65535 - r)
    pwm_g.duty_u16(65535 - g)
    pwm_b.duty_u16(65535 - b)


print("TP1 Démarré. Appuyez sur le joystick pour changer de mode.")

while True:
    current_time = time.ticks_ms()
    
    # GESTION DU BOUTON
    btn_val = btn.value()
    if btn_val == 0 and last_btn_val == 1: # Clic
        if time.ticks_diff(current_time, last_time) > 200: # Anti-rebond
            mode = (mode + 1) % 3
            last_time = current_time
    last_btn_val = btn_val

    # COMPORTEMENT
    r, g, b = 0, 0, 0
    mode_str = ""

    if mode == 0: # MANUEL (Joystick)
        mode_str = "Manuel"
        r = adc_x.read_u16()
        b = adc_y.read_u16()
        g = int((r + b) / 2)
        set_color(r, g, b)

    elif mode == 1: 
        mode_str = "Clignotant"
        if (current_time // 500) % 2 == 0:
            set_color(65535, 0, 0)
            r = 65535
        else:
            set_color(0, 0, 0)

    elif mode == 2:
        mode_str = "Transition"
        val = (current_time % 2000) 
        intensity = int((val / 2000) * 65535)

        set_color(0, 65535 - intensity, intensity)
        g = 65535 - intensity
        b = intensity

    # AFFICHAGE OLED
    if oled:
        oled.fill(0)
        oled.text(f"Mode: {mode_str}", 0, 0)
        oled.text(f"R: {int(r/655.35)}%", 0, 20)
        oled.text(f"G: {int(g/655.35)}%", 0, 32)
        oled.text(f"B: {int(b/655.35)}%", 0, 44)
        oled.show()