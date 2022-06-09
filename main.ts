let speedFactor = 80
let pin_L = DigitalPin.P13
let pin_R = DigitalPin.P2
let pin_Trig = DigitalPin.P8
let pin_Echo = DigitalPin.P15
// piny (+speedfactor)
let path = 1
let connected = 0
let switch_ = 0
let halt = true
// switch variables
let strip = neopixel.create(DigitalPin.P16, 4, NeoPixelMode.RGB)
pins.setPull(pin_L, PinPullMode.PullNone)
pins.setPull(pin_R, PinPullMode.PullNone)
bluetooth.startUartService()
basic.showString("S")
// minor less important code
function motor_run(right: number = 0, left: number = 0, speed_factor: number = 80) {
    PCAmotor.MotorRun(PCAmotor.Motors.M1, Math.map(Math.constrain(left * (speedFactor / 100), -100, 100), -100, 100, -255, 255))
    PCAmotor.MotorRun(PCAmotor.Motors.M4, Math.map(Math.constrain(right * (speedFactor / 100), -100, 100), -100, 100, -255, 255))
}

function motor_stop() {
    PCAmotor.MotorStop(PCAmotor.Motors.M1)
    PCAmotor.MotorStop(PCAmotor.Motors.M4)
}

// run/stop motors
forever(function on_forever() {
    let sensor_L: number;
    let sensor_R: number;
    let obstacle_distance: number;
    if (switch_ == 0) {
        sensor_L = pins.digitalReadPin(pin_L)
        sensor_R = pins.digitalReadPin(pin_R)
        obstacle_distance = sonar.ping(pin_Trig, pin_Echo, PingUnit.Centimeters)
        if (sensor_L == path && sensor_R == path) {
            motor_run(50, 50)
        } else if (sensor_L != path && sensor_R != path) {
            motor_stop()
        } else if (sensor_L == path && sensor_R != path) {
            motor_run(50, 0)
        } else if (sensor_L != path && sensor_R == path) {
            motor_run(0, 50)
        }
        
    } else if (switch_ == 1) {
        
    }
    
})
// autonomní mód
// NEKOMPLETNÍ ČÁST!!!ZÁKAZ VSTUPU
bluetooth.onBluetoothConnected(function on_bluetooth_connected() {
    let uartData: string;
    let sensor_L: number;
    let sensor_R: number;
    
    basic.showIcon(IconNames.Heart)
    connected = 1
    while (connected == 1) {
        uartData = bluetooth.uartReadUntil(serial.delimiters(Delimiters.Hash))
        console.logValue("data", uartData)
        if (uartData == "M") {
            switch_ == 1
        }
        
        if (uartData == "L") {
            switch_ == 0
        }
        
        if (uartData == "0") {
            motor_run(0, 0)
        } else if (uartData == "A") {
            motor_run(50, 50)
        } else if (uartData == "B") {
            motor_run(-50, -50)
        } else if (uartData == "C") {
            motor_run(-50, 50)
        } else if (uartData == "D") {
            motor_run(50, -50)
        } else if (uartData == "G") {
            motor_run(-50, 50)
            basic.pause(870)
            motor_stop()
        } else if (uartData == "H") {
            sensor_L = pins.digitalReadPin(pin_L)
            sensor_R = pins.digitalReadPin(pin_R)
            motor_run(-50, 50)
            basic.pause(400)
            motor_stop()
            while (sensor_L != path && sensor_R != path) {
                motor_run(-50, 50)
                if (sensor_L == path || sensor_R == path) {
                    motor_stop()
                    break
                }
                
            }
        }
        
    }
})
// bluetooth mód
bluetooth.onBluetoothDisconnected(function on_bluetooth_disconnected() {
    
    basic.showIcon(IconNames.Sad)
    connected = 0
})
bluetooth.uartWriteNumber(0)
