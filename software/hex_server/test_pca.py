from board import SCL, SDA
import busio
import time
# Import the PCA9685 module.
from adafruit_pca9685 import PCA9685

# Create the I2C bus interface.
i2c_bus = busio.I2C(SCL, SDA)

# Create a simple PCA9685 class instance.
pca_right = PCA9685(i2c_bus, address=0x40)
pca_left = PCA9685(i2c_bus, address=0x41)
pca_right.frequency = 50
pca_left.frequency = 50


min_cycles = 1500 # 0
max_cycles = 8000 # 180
mid_cycles = 3250 # 90

alpha_min=3250
alpha_max=6500
alpha_mid=4875

beta_min=2000
beta_max=8000
beta_mid=5000

gamma_min=2000
gamma_max=8000
gamma_mid=5000

while True:
    mode = input("Mode:")
    if mode == 'auto':
        # for i in [(1,2,3),(4,5,6),(12,13,14)]:
        #     for s in i:
        #         pca_right=
        # for j in [(1,2,3),(4,5,6),(12,13,14)]:
        for ch in pca_left.channels:
            ch.duty_cycle = 5000
            time.sleep(0.100)

        for ch in pca_right.channels:
            ch.duty_cycle = 5000
            time.sleep(0.100)

    else:
        side = input("Enter side:")
        board = pca_left if side == 'left' else pca_right
        pin = input("Enter pin:")
        
        try:
            cycle = input("Enter duty cycle:")
            while cycle is not 'b':
                board.channels[int(pin)].duty_cycle = int(cycle)
                cycle = input("Enter duty cycle:")
        except Exception as e:
            print(e)
            raise e