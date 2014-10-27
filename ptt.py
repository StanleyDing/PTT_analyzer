import telnetlib
import re
import tempfile
import os

rn = '\r\n'
C_L = '\x0C'
C_Z = '\x1A'
ESC = '\x1B'

def send(tel, s):
    try:
        if not isinstance(s, bytes):
            s = s.encode('big5')
        tel.write(s)
    except OSError:
        print('Disconnected')

def wait(tel, exp, timeout=None):
    try:
        r = tel.read_until(exp.encode('big5'), timeout)
        r += tel.read_very_eager()
    except EOFError:
        print('Connection closed')
    print(r.decode('big5', 'ignore'))
    return r

if not os.path.isdir('./article'):
    os.mkdir('article')

tn = telnetlib.Telnet('ptt.cc')

# username
wait(tn, '註冊: ')
send(tn, input('username: ') + rn)

# password
wait(tn, '密碼: ')
send(tn, input('password: ') + rn)

dup_prompt = '重複登入的連線'.encode('big5')
press_prompt = '任意鍵'.encode('big5')

ret = tn.expect([press_prompt, dup_prompt])
if ret[0] == 1:
    send(tn, 'n' + rn)
send(tn, rn)

# in main menu now
send(tn, 's')
wait(tn, '選擇看板')

send(tn, 'Gossiping' + rn)
wait(tn, '任意鍵')
send(tn, rn)

wait(tn, '文章選讀')

top = b'\x1b\[0*;*33;45m.*\x1b\[1;30;47m.*\x1b\[m'
mid = b'\x1b\[0*;*34;46m.*\x1b\[1;30;47m.*\x1b\[m'
bot = b'\x1b\[0*;*44m.*\x1b\[1;30;47m.*\x1b\[m'

send(tn, 'l' + C_L)
for i in range(0, 20):
    line_int = [0, 0]
    fp = open(tempfile.mkstemp('.in', dir='./article')[0], 'w')

    while True:
        i = tn.expect([top, mid, bot], 5)
        if i[0] == -1:
            print(i[2])

        bar = i[1].group(0).decode('big5', 'ignore')
        line_match = re.search('([0-9]+)~([0-9]+)', bar)
        line_start = int(line_match.group(1))
        line_end = int(line_match.group(2))

        x = i[2].decode('big5', 'ignore')

        if line_int[1] >= line_start:
            n = line_int[1] - line_start + 1
            x = '\n'.join(x.split('\n')[n:])

        line_int = [line_start, line_end]
        fp.write(x + '\n')
        if i[0] == 2:
            break
        send(tn, ' ' + C_L)
    fp.close()
    send(tn, 'b' + C_L)

tn.close()
