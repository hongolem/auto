speedFactor = 80
pin_L = DigitalPin.P13
pin_R = DigitalPin.P2
pin_Trig = DigitalPin.P8
pin_Echo = DigitalPin.P15   #piny (+speedfactor)

path = 1
connected = 0
switch = 0
halt = True
whileswitch = 0         #switch variables

strip = neopixel.create(DigitalPin.P16, 4, NeoPixelMode.RGB)
pins.set_pull(pin_L, PinPullMode.PULL_NONE)
pins.set_pull(pin_R, PinPullMode.PULL_NONE)
bluetooth.start_uart_service()
basic.show_string("S")                                          #minor less important code

def motor_run(right = 0, left = 0, speed_factor = 80):
    PCAmotor.motor_run(PCAmotor.Motors.M1, Math.map(Math.constrain(left * (speedFactor / 100), -100, 100), -100, 100, -255, 255))
    PCAmotor.motor_run(PCAmotor.Motors.M4, Math.map(Math.constrain(right * (speedFactor / 100), -100, 100), -100, 100, -255, 255))
    
def motor_stop():
    PCAmotor.motor_stop(PCAmotor.Motors.M1)
    PCAmotor.motor_stop(PCAmotor.Motors.M4)             #run/stop motors
    
def on_forever():
    if switch == 0:
        sensor_L = pins.digital_read_pin(pin_L)
        sensor_R = pins.digital_read_pin(pin_R)
        obstacle_distance = sonar.ping(pin_Trig, pin_Echo, PingUnit.CENTIMETERS)
        if (sensor_L == path) and (sensor_R == path):
            motor_run(50, 50)
        elif (sensor_L != path) and (sensor_R != path):
            motor_stop()
            motor_run(-50, 50)
            basic.pause(100)
            motor_run(50, -50)
            basic.pause(100)
        elif (sensor_L == path) and (sensor_R != path):
            motor_run(50, 0)
        elif (sensor_L != path) and (sensor_R == path):
            motor_run(0, 50)
    elif switch == 1:
        pass
forever(on_forever)     #autonomní mód