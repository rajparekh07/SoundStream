import pyaudio
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import wave
from subprocess import check_output
import os
import base64
import zlib
from WSServer import WSServer
import threading
import socket
import qrcode

stop = False
defDev = ""

def record_sounds(output_file="record.wav", time=0):



    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 22000
    CHUNK = 512
    RECORD_SECONDS = time/1000
    WAVE_OUTPUT_FILENAME = output_file
    audio = pyaudio.PyAudio()
    # stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    stream = audio.open(format = FORMAT,
                                 channels = CHANNELS,
                                 rate = RATE,
                                 input = True,
                                 output = True,
                                 frames_per_buffer = CHUNK,
                                input_device_index = 2,
                                output_device_index = 1)
    frames = []
    f2 = []


    if time is not 0:
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK, False)
            stream.write(data)
            # print(data)
            WSServer.send(data)

            frames.append(data)
    else:
        try:
            print("Press Ctrl+C to exit...")
            while True:
                data = stream.read(CHUNK, False)
                # stream.write(data)
                WSServer.send(zlib.compress(data, 2))

                frames.append(data)
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(e)
            return -1

    stream.stop_stream()
    stream.close()
    audio.terminate()

    # WSServer.send(b"Hi")

    # WSServer.send(b''.join(frames))
    # WSServer.send(frames[3])
    # print(type(frames[3]))
    # print(base64.b64encode(frames[3]))
    wave_file = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wave_file.setnchannels(CHANNELS)
    wave_file.setsampwidth(audio.get_sample_size(FORMAT))
    wave_file.setframerate(RATE)
    wave_file.writeframes(b''.join(frames))
    wave_file.close()
    os.system("SwitchAudioSource -s '" + str.strip(str(defDev)) + "'")

    return 0

# record_sounds()

def serve():
    try:
        pass
        record_sounds()
    except:
        pass  

try:
    thread = threading.Thread(target=serve, args=())
    defDev = str.strip(str(check_output("SwitchAudioSource -c", shell=True).decode("utf-8"))) 
    os.system("SwitchAudioSource -s \"Soundflower (2ch)\"")
    thread.daemon = True                            # Daemonize thread
    thread.start() 

    def onConnect():
        pass

    def stop():
        pass

    WSServer.on("stop", stop)
    WSServer.bindOnConnection(onConnect)
except Exception as e:
    print(e)

ip = socket.gethostbyname(socket.gethostname())
port = 8000
img = qrcode.make('ws://'+ip+':'+str(port))
img.show()
server = SimpleWebSocketServer(ip, port, WSServer)
try:
    server.serveforever()
    
except KeyboardInterrupt as e:
    os.system("SwitchAudioSource -s '" + str.strip(str(defDev)) + "'")
    thread.join(0)
