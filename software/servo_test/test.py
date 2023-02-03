from adafruit_servokit import ServoKit

pca_right = ServoKit(channels=16, address=0x40)
pca_left = ServoKit(channels=16, address=0x41)

if __name__=="__main__":

    pca_right.servo[7].angle = 90