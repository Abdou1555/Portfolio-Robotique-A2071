from machine import Pin, PWM

class Servo:
    def __init__(self, pin):
        self.pwm = PWM(Pin(pin))
        self.pwm.freq(50) # Fréquence 50Hz

    def set_angle(self, angle):
        if angle < 0: angle = 0
        if angle > 180: angle = 180
        
        # NOUVELLES VALEURS PLUS SÛRES (Standard SG90)
        # 0° = ~1638 (0.5ms), 180° = ~8192 (2.5ms)
        min_duty = 1638
        max_duty = 8192
        
        duty = int((angle / 180) * (max_duty - min_duty) + min_duty)
        self.pwm.duty_u16(duty)

    def stop(self):
        self.pwm.deinit()