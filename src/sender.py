import socket, cv2, pickle, threading, time, struct

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host_ip = '0.0.0.0'
port = 7078

server_socket.bind((host_ip, port))
server_socket.listen()
print('Listening...')

def sender():
    print('Sender thread started...')
    session, addr = server_socket.accept()
    print('Connected....')
    if session:
        camera = cv2.VideoCapture(0)

        while(camera.isOpened()):
            ret, frame = camera.read()
            data = pickle.dumps(frame)
            data = struct.pack('Q', len(data)) + data
            try :
                session.sendall(data)
            except:
                session.close()

            cv2.imshow('You', frame)
            if cv2.waitKey(10) == 13:
                session.close()
                break
        
    cv2.destroyAllWindows()

t_sender = threading.Thread(target=sender)
t_sender.start()