import socket
import json

_ENDPOINT = ("127.0.0.1", 10000)

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    vel = {
        "x": 0.0,  # m/s
        "w": 0.0,  # rad/s
    }


    from pynput.keyboard import Key, Listener

    def on_press(key):
        if hasattr(key, "char"):
            if key.char=="w":
                vel["x"]+=0.3
            elif key.char == "s":
                vel["x"]-=0.3
            elif key.char == "a":
                vel["w"]+=0.1
            elif key.char == "d":
                vel["w"]-=0.1
            else:
                pass
            data = json.dumps(vel)
            print(data)
            sock.sendto(data.encode('utf-8'), _ENDPOINT)
        else:
            pass

    with Listener(on_press=on_press) as listener:
        listener.join()