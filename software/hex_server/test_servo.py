from adafruit_servokit import ServoKit
from leg import Leg

pca_left = ServoKit(channels=16, address=0x41, frequency=50)
pca_right = ServoKit(channels=16, address=0x40, frequency=50)

legs = [
    # front right
    [
        pca_right.servo[12], 
        pca_right.servo[13],
        pca_right.servo[14]
    ],
        # correction=config.get('leg0Offset', [0, 0, 0])
    # center right
[
        pca_right.servo[8],
        pca_right.servo[9],
        pca_right.servo[10]
    ],
        [# correction=config.get('leg1Offset', [0, 0, 0])[
        pca_right.servo[2], 
        pca_right.servo[3],
        pca_right.servo[4]
    ],

    # rear left
[
        pca_left.servo[12], 
        pca_left.servo[13],
        pca_left.servo[14]
],
    # center left
[
        pca_left.servo[4], 
        pca_left.servo[5],
        pca_left.servo[6]
    ],
        # correction=config.get('leg4Offset', [0, 0, 0])

    # front left
[
        pca_left.servo[0], 
        pca_left.servo[1],
        pca_left.servo[2]
    ],

]

for i in legs:
    if legs.index(i) < 3:
        i[0].angle = 90
        i[1].angle = 90
        i[2].angle = 90
    else:
        i[0].angle = 90
        i[1].angle = 90
        i[2].angle = 90
# legs[0].reset(False)
# legs[1].reset(False)
# legs[2].reset(False)
# legs[3].reset(False)
# legs[4].reset(False)
# legs[5].reset(False)