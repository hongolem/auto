pin_L = DigitalPin.P13
pin_R = DigitalPin.P2
pin_Trig = DigitalPin.P8
pin_Echo = DigitalPin.P15   #piny

path = 1
counting = 0
connected = 0
modeSwitch = 0
crossroadSwitch = 0
ultrasonicSwitch = 0
ultrasonicON_OFF = 0
speedFactor = 80    #switchable variables

pins.set_pull(pin_L, PinPullMode.PULL_NONE)
pins.set_pull(pin_R, PinPullMode.PULL_NONE)
bluetooth.start_uart_service()
basic.show_string("S")                               #less important code

def motor_run(right = 0, left = 0, speedFactor = 80):
    PCAmotor.motor_run(PCAmotor.Motors.M1, Math.map(Math.constrain(left * (speedFactor / 100), -100, 100), -100, 100, -255, 255))
    PCAmotor.motor_run(PCAmotor.Motors.M4, Math.map(Math.constrain(right * (speedFactor / 100), -100, 100), -100, 100, -255, 255))
    
def motor_stop():
    PCAmotor.motor_stop(PCAmotor.Motors.M1)
    PCAmotor.motor_stop(PCAmotor.Motors.M4)             #run/stop motors

def on_forever():
    global counting
    if modeSwitch == 0:
        sensor_L = pins.digital_read_pin(pin_L)
        sensor_R = pins.digital_read_pin(pin_R)
        if (sensor_L == path) and (sensor_R == path):
            if crossroadSwitch == 0:
                motor_run(50, 50)
            elif crossroadSwitch == 1:
                motor_stop()
            counting = 0                                    #jede automaticky když je na křižovatce/čeká na povely
        elif (sensor_L != path) and (sensor_R != path):
            motor_stop()
            if counting >= 10:
                motor_run(-50, 50)
                basic.pause(870)
                motor_stop()
                counting = 0
            elif counting < 10:
                counting = counting + 1
                motor_stop()
                motor_run(-50, 50)
                basic.pause(150)
                motor_run(50, -50)
                basic.pause(110)                            #když nevidí cestu začne se mírně otáčet ze strany na stranu, ale když dlouho nic nenachází udělá 180
        elif (sensor_L == path) and (sensor_R != path):
            motor_run(50, 0)
            counting = 0                                    #jede vlevo
        elif (sensor_L != path) and (sensor_R == path):
            motor_run(0, 50)
            counting = 0                                    #jede vpravo
    elif modeSwitch == 1:
        pass                                                #zapnuto manuální řízení
forever(on_forever)                                                 #autonomní mód

def onIn_background():
    global modeSwitch
    if ultrasonicON_OFF == 0:
        basic.pause(500)
        obstacle_distance = sonar.ping(pin_Trig, pin_Echo, PingUnit.CENTIMETERS)
        if obstacle_distance < 15:
            if ultrasonicSwitch == 0:
                modeSwitch = 1
                motor_stop()
                motor_run (50, -50, 80)
                basic.pause(870)
                motor_stop()
                modeSwitch = 0                  #funkce otočí se od překážky
            elif ultrasonicSwitch == 1:
                modeSwitch = 1
                pause(200)
                sensor_L = pins.digital_read_pin(pin_L)
                sensor_R = pins.digital_read_pin(pin_R)
                motor_run(50, -50)
                basic.pause(525)
                motor_stop()
                basic.pause(500)
                motor_run(50, 50)
                basic.pause(1900)
                motor_stop()
                basic.pause(500)
                motor_run(-50, 50)
                basic.pause(530)
                motor_stop()
                basic.pause(500)
                motor_run(50, 50)
                basic.pause(2500)
                motor_stop()
                basic.pause(500)
                motor_run(-50, 50)
                basic.pause(525)
                motor_stop()
                basic.pause(500)
                basic.pause(500)
                motor_run(50, 50)
                basic.pause(1900)
                modeSwitch = 0                  #funkce objede překážku
    elif ultrasonicON_OFF == 1:
        pass                                    #funkce je vyplá
    control.in_background(onIn_background)
control.in_background(onIn_background)              #ultrasonic funkce

def on_bluetooth_connected():
    global connected, modeSwitch, path, crossroadSwitch, ultrasonicSwitch, ultrasonicON_OFF
    basic.show_icon(IconNames.HEART)
    connected = 1
    while connected == 1:
        uartData = str(bluetooth.uart_read_until(serial.delimiters(Delimiters.HASH)))
        console.log_value("data", uartData)
        print(uartData)
        if uartData == "A":
            motor_run(75, 75)
            basic.pause(500)
            motor_stop()                                                    #jízda rovně
        elif uartData == "B":
            motor_run(-75, -75)
            basic.pause(500)
            motor_stop()                                                    #jízda zpět
        elif uartData == "C":
            motor_run(50, -50)
            basic.pause(300)
            motor_stop()                                                    #jízda doleva
        elif uartData == "D":
            motor_run(-50, 50)
            basic.pause(300)
            motor_stop()                                                    #jízda doprava
        elif uartData == "G":
            path = 0 if (path == 1) else 1                                      #přepínání barvy cesty
        elif uartData == "H":
            crossroadSwitch = 0 if (crossroadSwitch == 1) else 1                #přepínání z automatic voliče cesty na manuál
        elif uartData == "I":
            modeSwitch = 0 if (modeSwitch == 1) else 1
            motor_stop()                                                        #manuální/automatické řízení
        elif uartData == "J":
            ultrasonicSwitch = 0 if (ultrasonicSwitch == 1) else 1              #přepínání mezi: při mechanické překážce se otočí/objede
        elif uartData == "K":
            ultrasonicON_OFF = 0 if (ultrasonicON_OFF == 1) else 1              #vypnutí/zapnutí ultrasonic sensoru
        elif uartData == "L":
            motor_run (50, -50, 80)
            basic.pause(870)
            motor_stop()                                                        #180° otočka
        elif uartData == "0":
            pass
bluetooth.on_bluetooth_connected(on_bluetooth_connected)                            #bluetooth mód

def on_bluetooth_disconnected():
    global connected
    basic.show_icon(IconNames.SAD)
    connected = 0
bluetooth.on_bluetooth_disconnected(on_bluetooth_disconnected)
bluetooth.uart_write_number(0)

#praktické testování U.S.S.
#+nemít zaplý automat po dokončení U.S.S (mby)
#pause, motor_stop do motor_run
#ultrasonic vypnut když jede manual