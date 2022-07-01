import re

class log_t:
    def __init__(this, string):
        this.valid = False
        data =  re.search(r'Day (\d+), (\d+):(\d+):(\d+): .+?"(\d+, \d+, \d+, \d+)">(.+?)</>', string)
        if (data == None): return
        this.valid = True
        this.day = data.groups()[0]
        this.hour = data.groups()[1]
        this.min = data.groups()[2]
        this.sec = data.groups()[3]
        this.rgba = data.groups()[4]
        this.message = data.groups()[5]

    def ftime(this):
        return (((((int(this.day) * 24) + int(this.hour)) * 60) + int(this.min)) * 60) + int(this.sec)

    def hex_color(this):
        data =  re.search('(\d+), (\d+), (\d+), (\d+)', this.rgba)
        return '{:02x}'.format(int(float(data.groups()[0]) * 255), 'x') + '{:02x}'.format(int(float(data.groups()[1]) * 255), 'x') + '{:02x}'.format(int(float(data.groups()[2]) * 255), 'x')