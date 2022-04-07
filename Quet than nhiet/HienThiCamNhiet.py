##########################################
# MLX90640 Thermal Camera w Raspberry Pi
# -- 2Hz Sampling with Simple Routine
##########################################
#
import time,board,busio
import numpy as np
import adafruit_mlx90640
import matplotlib.pyplot as plt
import cv2
import math

from threading import Thread
import socket #ip
#---------Flask----------------------------------------
from flask import Flask, Response
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    #return "Default Message"
    return render_template("index.html")

@app.route('/video_feed')
def video_feed():
    #global cap
    return Response(main(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
                    
#-----------------------------------------------------------


i2c = busio.I2C(board.SCL, board.SDA, frequency=400000) # setup I2C
mlx = adafruit_mlx90640.MLX90640(i2c) # begin MLX90640 with I2C comm
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_16_HZ # set refresh rate
mlx_shape = (24,32)

# setup the figure for plotting
plt.ion() # enables interactive plotting
fig,ax = plt.subplots(figsize=(12,7))
therm1 = ax.imshow(np.zeros(mlx_shape),vmin=0,vmax=60) #start plot with zeros
cbar = fig.colorbar(therm1) # setup colorbar for temps
cbar.set_label('Temperature [$^{\circ}$C]',fontsize=13) # colorbar label

frame = np.zeros((24*32,)) # setup array for storing all 768 temperatures
t_array = []
scaling = 20

width = scaling * 32
height = scaling * 24

img = np.zeros([height,width,3])
imgGray = np.zeros([height,width,3])
def main():
    while True:
        t1 = time.monotonic()
        try:
            mlx.getFrame(frame) # read MLX temperatures into frame var
            
            # reshape data into matrix
            output = frame.reshape(24,32)
            
            # scaling
            minValue = 20 #math.floor(np.amin(output))
            maxValue = 40 #math.ceil(np.amax(output))
            output = output - minValue      
            output = output * 255/ (maxValue - minValue) # Now scaled to 0 - 255   

            # resize image
            dim = (width, height)
            output = cv2.resize(output, dim, interpolation = cv2.INTER_LINEAR )
                
            # apply colormap
            imgGray = output.astype(np.uint8)
            img = cv2.applyColorMap(imgGray, cv2.COLORMAP_JET)
            
            # put min/max text on image
            text = "Min: " + str(minValue) +  " C  Max: " + str(maxValue)+ " C"  
            font = cv2.FONT_HERSHEY_SIMPLEX  
            org = (20, 50) 
            image = cv2.putText(img, text, org, font, 1, (255, 255, 255) , 2, cv2.LINE_AA) 
    #         cv2.imshow("image", img);
            ret, jpeg = cv2.imencode('.jpg', img)
            pic = jpeg.tobytes()
            
            #Flask streaming
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + pic + b'\r\n\r\n')

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except ValueError:
            continue # if error, just read again

if __name__ == '__main__':
        
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.connect(('8.8.8.8',80))
    localhost=s.getsockname()[0]
    app.run(host = localhost, port = 8002)
#    app.run(host='0.0.0.0', port=2204, threaded=True) # Run FLASK
    main()


