import time
import pymem #https://pypi.org/project/Pymem/

pm = pymem.Pymem('ShooterGame.exe')
module_shooter_game = pymem.process.module_from_name(pm.process_handle, 'ShooterGame.exe')

global controller_ptr
controller_ptr = 0

def init():
    global controller_ptr
    sig = rb"\x44\x0F\x28\xC9\x48\x8B\xF9\x33\xF6\x44\x8B\xEE\x89\x74\x24\x70\x89\x74\x24\x78\xE8"
    hook = pymem.pattern.pattern_scan_module(pm.process_handle, module_shooter_game, sig)

    if type(hook) != int or not hook:
        sig = rb"\xFF\x15\x02\x00\x00\x00\xEB\x08"
        hook = pymem.pattern.pattern_scan_module(pm.process_handle, module_shooter_game, sig)
        if type(hook) != int or not hook:
            raise Exception("Hook Not Found")
        alloc = pm.read_ulonglong(hook + 8)
        controller_ptr = alloc + 24
        return

    alloc = pm.allocate(0x100)
    inject_code = b"\xFF\x15\x02\x00\x00\x00\xEB\x08"

    byte_alloc = alloc.to_bytes(8, byteorder = 'little', signed=False)
    inject_code += byte_alloc

    call_code = b"\x48\x89\x0D\x01\x00\x00\x00\xC3"

    call_code = pm.read_bytes(hook, len(inject_code)) + call_code
    pm.write_bytes(alloc, call_code, len(call_code))
    pm.write_bytes(hook, inject_code, len(inject_code))
    controller_ptr = alloc + len(call_code)

init()
time.sleep(3)

def controller():
    global controller_ptr
    return pm.read_ulonglong(controller_ptr)

def get_tribelog():
    control = controller()
    if control == 0: 
        return None

    ptr = control + 0xE30
    struct = pm.read_ulonglong(ptr), pm.read_int(ptr + 8), pm.read_int(ptr + 12)
    if struct[0] == 0:
        return None        
    x = 0    
    tribe = []
    while x < struct[1]:
        str_struct_ptr = struct[0] + (x * 16)
        str_struct = pm.read_ulonglong(str_struct_ptr), pm.read_int(str_struct_ptr + 8), pm.read_int(str_struct_ptr + 12)
        raw_string = pm.read_bytes(str_struct[0], str_struct[1] * 2).decode("utf-8", "strict")
        t = 0
        string = ""
        while t < str_struct[1]:
            string += (raw_string[t * 2])
            t += 1
        tribe.append(string)
        x += 1
    return tribe