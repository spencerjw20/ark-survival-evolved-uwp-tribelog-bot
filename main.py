import memory
import log_parse
import web_hook

last_time = 0
ran = False

while True:
    log = memory.get_tribelog()
    if log == None: 
        memory.time.sleep(5)
        print('log error')
        continue
    for day in log:
        t = log_parse.log_t(day)
        if not t.valid: continue
        rtime = t.ftime()
        if (last_time < rtime):
            last_time = rtime
            if (ran): 
                print('Day')
                web_hook.send_hook('Day %s, %s:%s:%s' % (t.day, t.hour, t.min, t.sec), t.message, t.hex_color())
    ran = True
    memory.time.sleep(1)