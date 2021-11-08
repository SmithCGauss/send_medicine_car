# Main Module Example
#
# When your OpenMV Cam is disconnected from your computer it will either run the
# 灰度
#
import sensor, image, time, pyb
from image import SEARCH_EX, SEARCH_DS
from pyb import UART

led = pyb.LED(3) # Red LED = 1, Green LED = 2, Blue LED = 3, IR LEDs = 4.
usb = pyb.USB_VCP() # This is a serial port object that allows you to

#import json
uart = UART(3, 9600)
thresholds_num = [(0, 223)]#数字的颜色阈值

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 1000)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking
clock = time.clock()

# 只有比“pixel_threshold”多的像素和多于“area_threshold”的区域才被
# 下面的“find_blobs”返回。 如果更改相机分辨率，
# 请更改“pixels_threshold”和“area_threshold”。 “merge = True”合并图像中所有重叠的色块。
templates = ["/1.pgm","/2.pgm","/3.pgm","/4.pgm","/5.pgm","/6.pgm","/7.pgm","/8.pgm"]
templates_l = ["/3l.pgm","/4l.pgm","/5l.pgm","/6l.pgm","/7l.pgm","/8l.pgm"]
templates_r = ["/3r.pgm","/4r.pgm","/5r.pgm","/6r.pgm","/7r.pgm","/8r.pgm"]
templates_flat = ["/3hg.pgm","/4hg.pgm","/5hg.pgm","/6hg.pgm","/7hg.pgm","/8hg.pgm"]
start_flag = 0  #1代表可以启动，0代表待命状态（默认）

while(True):
    clock.tick()
    img = sensor.snapshot().lens_corr(1.8)
    for blob in img.find_blobs(thresholds_num, pixels_threshold=100, area_threshold=100):
        #img.draw_rectangle(blob.rect())
        #img.draw_cross(blob.cx(), blob.cy())
        #print(blob.code())

        #等待人工喂图阶段
        if start_flag == 0:
            for t in templates:
                template = image.Image(t)
                end = image.Image("end.pgm")
                #对每个模板遍历进行模板匹配
                r = img.find_template(template, 0.82, step=4, search=SEARCH_DS)
            #find_template(template, threshold, [roi, step, search]),threshold中
            #的0.6是相似度阈值,roi是进行匹配的区域（左上顶点为（10，0），长80宽60的矩形），
            #注意roi的大小要比模板图片大，比frambuffer小。
            #把匹配到的图像标记出来
            #r为匹配区域的边界框元组(x,y,w,h),否则为None
                if r:
                    img.draw_rectangle(r, color=0)
                    if t == "/1.pgm":
                        temp = 1
                        uart.write("1")
                        print("一号病房")
                        led.on()
                        time.sleep_ms(1500)
                        led.off()
                        time.sleep_ms(1000)
                        led.on()
                        time.sleep_ms(1500)
                        led.off()
                        time.sleep_ms(1000)
                    if t == "/2.pgm":
                        temp = 2
                        uart.write("2")
                        print("二号病房")
                        led.on()
                        time.sleep_ms(1500)
                        led.off()
                        time.sleep_ms(1000)
                        led.on()
                        time.sleep_ms(1500)
                        led.off()
                        time.sleep_ms(1000)
                    if t == "/3.pgm":
                        temp = 3
                        print("三号病房")
                        led.on()
                        time.sleep_ms(1500)
                        led.off()
                        time.sleep_ms(1000)
                        led.on()
                        time.sleep_ms(1500)
                        led.off()
                        time.sleep_ms(1000)
                    if t == "/4.pgm":
                        temp = 4
                        print("四号病房")
                        led.on()
                        time.sleep_ms(1500)
                        led.off()
                        time.sleep_ms(1000)
                        led.on()
                        time.sleep_ms(1500)
                        led.off()
                        time.sleep_ms(1000)
                    if t == "/5.pgm":
                        temp = 5
                        print("五号病房")
                        led.on()
                        time.sleep_ms(1500)
                        led.off()
                        time.sleep_ms(1000)
                        led.on()
                        time.sleep_ms(1500)
                        led.off()
                        time.sleep_ms(1000)
                    if t == "/6.pgm":
                        temp = 6
                        print("六号病房")
                        led.on()
                        time.sleep_ms(1500)
                        led.off()
                        time.sleep_ms(1000)
                        led.on()
                        time.sleep_ms(1500)
                        led.off()
                        time.sleep_ms(1000)
                    if t == "/7.pgm":
                        temp = 7
                        print("七号病房")
                        led.on()
                        time.sleep_ms(1500)
                        led.off()
                        time.sleep_ms(1000)
                        led.on()
                        time.sleep_ms(1500)
                        led.off()
                        time.sleep_ms(1000)
                    if t == "/8.pgm":
                        temp = 8
                        print("八号病房")
                        led.on()
                        time.sleep_ms(1500)
                        led.off()
                        time.sleep_ms(1000)
                        led.on()
                        time.sleep_ms(1500)
                        led.off()
                        time.sleep_ms(1000)
                    start_flag = 1
                    uart.write("t")

#人工喂图结束，小车启动，开始寻线，openMV开始找所喂的图

        if (start_flag == 1)and((temp>=3) and (temp <= 8)):
            template = image.Image(templates_flat[temp-3])
            find_img = [template, end]
            for img in find_img:

                r = img.find_template(img, 0.40, step=6, search=SEARCH_EX)

                #template = image.Image(templates_l[temp-3])
                #l = img.find_template(template, 0.20, step=6, search=SEARCH_DS)
                #if r:
                    #print(temp)#输出所喂的图的编号
                    #print("right")
                #if l:
                    #print(temp)
                    #print("left")
                if r:
                    if img == end:
                        uart.write("s")
                        print("stop")
                    else :
                        x = r[0]+r[2]/2
                        if x >=80:
                            uart.write("r")
                            print("right")
                            print(temp)
                        else :
                            uart.write("l")
                            print("left")
                            print(temp)



        #print(clock.fps())
