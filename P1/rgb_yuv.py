import numpy as np


def rgb_to_yuv(rgb):
    if min(rgb) < 0 or max(rgb) > 255:  # check for valid rbg range
        return []

    R = rgb[0] 
    G = rgb[1]
    B = rgb[2]

    Y = R * 0.257 + G * 0.504 + B * 0.098 + 16
    U = R * -0.148 + G * -0.291 + B * 0.439 + 128
    V = R * 0.439 + G * -0.368 + B * -0.071 + 128

    return np.array([Y, U, V])


def yuv_to_rgb(yuv):
    Y = yuv[0]
    U = yuv[1]
    V = yuv[2]

    R = 1.164 * (Y - 16) + 1.596 * (V - 128)
    G = 1.164 * (Y-16) - 0.813 * (V-128) - 0.391 * (U-128)
    B = 1.164 * (Y-16) + 2.018 * (U-128)

    return np.array([R, G, B])


# input parameters from terminal
choice = str(raw_input("Covert from rgb or yuv? "))

if choice == "rgb":
    rgb = []
    rgb.append(int(raw_input("Enter R: ")))
    rgb.append(int(raw_input("Enter G: ")))
    rgb.append(int(raw_input("Enter B: ")))
    rgb = np.array(rgb)

    yuv = rgb_to_yuv(rgb)  # conversion
    if(yuv == []):
        print('Wrong RGB input')
    else:
        print('The YUV conversion is: ' + str(yuv))
elif choice == 'yuv': 
    yuv = []
    yuv.append(float(raw_input("Enter Y: ")))
    yuv.append(float(raw_input("Enter U: ")))
    yuv.append(float(raw_input("Enter V: ")))
    yuv = np.array(yuv)
    print('The RGB conversion is: ' + str(yuv_to_rgb(yuv)))  # conversion
else:
    print('Wrong choice')

