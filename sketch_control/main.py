from machine import Pin, PWM, I2C, Timer
import time
from ssd1306 import SSD1306_I2C
import framebuf

ATT0 = 0 #Начальное положение атт110
listATT0 = {0:[[0,0,0],[0,1,0],[1,0,0],[1,1,0]],
            10:[[0,0,1],[0,1,0],[1,0,0],[1,1,0]],
            20:[[0,0,0],[0,1,1],[1,0,0],[1,1,0]],
            30:[[0,0,1],[0,1,1],[1,0,0],[1,1,0]],
            40:[[0,0,0],[0,1,0],[1,0,1],[1,1,0]],
            50:[[0,0,1],[0,1,0],[1,0,1],[1,1,0]],
            60:[[0,0,0],[0,1,1],[1,0,1],[1,1,0]],
            70:[[0,0,1],[0,1,1],[1,0,1],[1,1,0]],
            80:[[0,0,0],[0,1,0],[1,0,1],[1,1,1]],
            90:[[0,0,1],[0,1,0],[1,0,1],[1,1,1]],
            100:[[0,0,0],[0,1,1],[1,0,1],[1,1,1]],
            110:[[0,0,1],[0,1,1],[1,0,1],[1,1,1]],}
ATT1 = 0 #Начальное положение атт11
listATT1 = {0:[[0,0,0],[0,1,0],[1,0,0],[1,1,0]],
            1:[[0,0,1],[0,1,0],[1,0,0],[1,1,0]],
            2:[[0,0,0],[0,1,1],[1,0,0],[1,1,0]],
            3:[[0,0,1],[0,1,1],[1,0,0],[1,1,0]],
            4:[[0,0,0],[0,1,0],[1,0,1],[1,1,0]],
            5:[[0,0,1],[0,1,0],[1,0,1],[1,1,0]],
            6:[[0,0,0],[0,1,1],[1,0,1],[1,1,0]],
            7:[[0,0,1],[0,1,1],[1,0,1],[1,1,0]],
            8:[[0,0,0],[0,1,0],[1,0,1],[1,1,1]],
            9:[[0,0,1],[0,1,0],[1,0,1],[1,1,1]],
            10:[[0,0,0],[0,1,1],[1,0,1],[1,1,1]],
            11:[[0,0,1],[0,1,1],[1,0,1],[1,1,1]],}

led25 = Pin(25, Pin.OUT)
att0_A = Pin(19, Pin.OUT)
att0_B = Pin(20, Pin.OUT)
att0_C = Pin(21, Pin.OUT)
att1_A = Pin(16, Pin.OUT)
att1_B = Pin(17, Pin.OUT)
att1_C = Pin(18, Pin.OUT)

led25.value(1)

i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=400000)
print (i2c)
WIDTH = 128 # oled display width
HEIGHT = 32 # oled display height
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c) # Init oled display
oled.contrast(255) #яркость

oled.text("I", 50, 15)
oled.show()
time.sleep_ms(50)
oled.text("IT", 50, 15)
oled.show()
time.sleep_ms(50)
oled.text("ITL", 50, 15)
oled.show()

enc0_Click = Pin(10, Pin.IN, Pin.PULL_UP)
enc0_A = Pin(11, Pin.IN, Pin.PULL_UP)
enc0_B = Pin(12, Pin.IN, Pin.PULL_UP)
tim0 = Timer()
tim1 = Timer()
tim2 = Timer()
C = enc0_Click.value()
A = enc0_A.value()
B = enc0_B.value()
M = 0

def handler0(timer):
    global M, ATT0, ATT1, A, enc0_B, enc0_A 
    if enc0_A.value() != A:
        A = enc0_A.value()
        if enc0_B.value() != A:
            if M == 0:
                ATT0 +=10
                if ATT0 >= 110:
                    ATT0 = 110
            elif M == 1:
                ATT1 +=1
                if ATT1 >= 11:
                    ATT1 = 11
                
def handler1(timer):
    global M, ATT0, ATT1, B, enc0_B, enc0_A 
    if enc0_B.value() != B:
        B = enc0_B.value()
        if enc0_A.value() != B:
            if M == 0:
                ATT0 -=10
                if ATT0 <= 0:
                    ATT0 = 0
            elif M == 1:
                ATT1 -=1
                if ATT1 <= 0:
                    ATT1 = 0

def click_but(timer):
    global M
    if enc0_Click.value() == 0:
        time.sleep_ms(300)
        M += 1
        if M >= 2:
            M = 0
        
tim0.init(freq=100, mode=Timer.PERIODIC, callback=handler0)
tim1.init(freq=100, mode=Timer.PERIODIC, callback=handler1)
tim2.init(freq=100, mode=Timer.PERIODIC, callback=click_but)

oldATT0 = 100
oldATT1 = 10
timex = 50
def q_att0(qwer):
    global oldATT0
    if qwer != oldATT0:
        led25.value(0)
        att0_C.value(listATT0.get(qwer)[0][0])# 0
        att0_A.value(listATT0.get(qwer)[0][1])# 1
        att0_B.value(listATT0.get(qwer)[0][2])# 0
        print ('att0', att0_C.value(), att0_A.value(), att0_B.value())
        time.sleep_ms(timex)
        att0_C.value(listATT0.get(qwer)[1][0])
        att0_A.value(listATT0.get(qwer)[1][1])
        att0_B.value(listATT0.get(qwer)[1][2])
        print ('att0', att0_C.value(), att0_A.value(), att0_B.value())
        time.sleep_ms(timex)
        att0_C.value(listATT0.get(qwer)[2][0])
        att0_A.value(listATT0.get(qwer)[2][1])
        att0_B.value(listATT0.get(qwer)[2][2])
        print ('att0', att0_C.value(), att0_A.value(), att0_B.value())
        time.sleep_ms(timex)
        att0_C.value(listATT0.get(qwer)[3][0])
        att0_A.value(listATT0.get(qwer)[3][1])
        att0_B.value(listATT0.get(qwer)[3][2])
        print ('att0', att0_C.value(), att0_A.value(), att0_B.value())
        time.sleep_ms(timex)
        led25.value(1)
        oldATT0 = qwer

def q_att1(qwer):
    global oldATT1
    if qwer != oldATT1:
        led25.value(0)
        att1_C.value(listATT1.get(qwer)[0][0])# 0
        att1_A.value(listATT1.get(qwer)[0][1])# 1
        att1_B.value(listATT1.get(qwer)[0][2])# 0
        print ('att1', att1_C.value(), att1_A.value(), att1_B.value())
        time.sleep_ms(timex)
        att1_C.value(listATT1.get(qwer)[1][0])
        att1_A.value(listATT1.get(qwer)[1][1])
        att1_B.value(listATT1.get(qwer)[1][2])
        print ('att1', att1_C.value(), att1_A.value(), att1_B.value())
        time.sleep_ms(timex)
        att1_C.value(listATT1.get(qwer)[2][0])
        att1_A.value(listATT1.get(qwer)[2][1])
        att1_B.value(listATT1.get(qwer)[2][2])
        print ('att1', att1_C.value(), att1_A.value(), att1_B.value())
        time.sleep_ms(timex)
        att1_C.value(listATT1.get(qwer)[3][0])
        att1_A.value(listATT1.get(qwer)[3][1])
        att1_B.value(listATT1.get(qwer)[3][2])
        print ('att1', att1_C.value(), att1_A.value(), att1_B.value())
        time.sleep_ms(timex)
        led25.value(1)
        oldATT1 = qwer
    
while True:
    q_att0(ATT0)
    q_att1(ATT1)
    
    
    oled.fill(0)
    oled.text("ITL",0,0)
    oled.hline(0, 8, 127, 8)
    oled.text("8496H: {} dB".format(ATT0),10,12)
    oled.text("8494H: {} dB".format(ATT1),10,24)
    oled.show()#вывести на экран
        
        
