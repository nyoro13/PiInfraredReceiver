# reference: https://blog.bschwind.com/2016/05/29/sending-infrared-commands-from-a-raspberry-pi-without-lirc/

import wiringpi as pi
from datetime import datetime

if __name__ == '__main__':
    RECEIVER_PIN = 4
    
    pi.wiringPiSetupGpio()
    pi.pullUpDnControl(RECEIVER_PIN, pi.PUD_DOWN)
    pi.pinMode(RECEIVER_PIN, pi.INPUT)
    
    while True:
        # 未受診時はHIGH
        pin = pi.HIGH

        # 受信するまで待つ
        while pin == pi.HIGH:
            pin = pi.digitalRead(RECEIVER_PIN)

        # 受信開始
        startTime = datetime.now()
        command = []

        numHigh = 0
        previousPin = pi.LOW

        while True:
            if pin != previousPin:
                now = datetime.now()
                pulseLength = now - startTime
                startTime = now

                command.append((previousPin, pulseLength.microseconds))

            if pin == pi.HIGH:
                numHigh = numHigh + 1
            else:
                numHigh = 0

            if numHigh > 10000:
                break

            previousPin = pin
            pin = pi.digitalRead(RECEIVER_PIN)

        print('----------start---------')
        s = 0
        for (val, pulse) in command:
            s = s + pulse
            print(val, pulse)
        print('----------End-----------')

        print("Size of array is " + str(len(command)))
        print(s)

