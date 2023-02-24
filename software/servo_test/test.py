import time

from adafruit_servokit import ServoKit

pca_right = ServoKit(channels=16, address=0x40)
pca_left = ServoKit(channels=16, address=0x41)

if __name__=="__main__":
    for i in range(16):
        pca_right.servo[i].angle = 90
        pca_left.servo[i].angle = 90
        time.sleep(0.5)
    
    # for i in range(16):
    #     pca_left.servo[i].angle = 90
    #     time.sleep(0.5)

    for i in range(16):
        angle = 90
        prev = 90
        while angle != 'n':
            angle = int(angle)
            if angle > prev:
                
                for j in range(prev, int(angle), 1):
                    pca_right.servo[i].angle = j
                    time.sleep(0.01)

            if angle < prev:
                print(list(range(prev, int(angle), -1)))
                for j in reversed(range(1, int(angle), 1)):
                    pca_right.servo[i].angle = j
                    time.sleep(0.01)
            
            prev = angle
            # pca_right.servo[i].angle = int(angle);
            angle  = input(f"Servo {i} angle:")
        else:
            continue

    #     pca_right.servo[i].angle = 90
    #     time.sleep(1000)
    #     pca_left.servo[i].angle = 60
    #     time.sleep(1000)
    # print(pca_left)