import Adafruit_PCA9685
import time

class servo_Class:
    #"Channel" is the channel for the servo motor on PCA9685
    #"ZeroOffset" is a parameter for adjusting the reference position of the servo motor
    def __init__(self, Channel, ZeroOffset):
        self.Channel = Channel
        self.ZeroOffset = ZeroOffset

        #Initialize Adafruit_PCA9685
        self.pwm = Adafruit_PCA9685.PCA9685(address=0x40)
        self.pwm.set_pwm_freq(int(60))

    # Angle setting
    def SetPos(self,pos):
        #PCA9685 controls angles with pulses, 150~650 of pulses correspond to 0~180° of angle
        #pulse = int((650-150)/180*pos+150+self.ZeroOffset)
        pulse = int(pos)
        self.pwm.set_pwm(self.Channel, 0, pulse)

    # End processing
    def ServorCleanup(self):
        #The servo motor is set at 90°.
        self.SetPos(int(375))
        print('Servor stopped.')

    def MotorCleanup(self):
        # Set the throttle motor to the neutral position
        self.SetPos(int(370))  # Assuming 0.5 corresponds to the neutral position
        print('Motor stopped.')
