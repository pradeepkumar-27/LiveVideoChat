import socket, cv2, pickle, threading, time, struct

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def receiver():
    #ip = input("Enter recepient IP : ")
    client_socket.connect(('192.168.225.129', 7078))
    print('Connection suucessfull')
    data = b""
    payload_size = struct.calcsize('Q')
    while True:
        while len(data) < payload_size:
            packet = client_socket.recv(4096)
            if not packet:
                break
            data += packet
        packed_frame_size = data[ : payload_size]
        data = data[payload_size:]
        frame_size = struct.unpack('Q', packed_frame_size)[0]

        while len(data) < frame_size:
            data += client_socket.recv(4096)
        frame = data[ : frame_size]
        data = data[frame_size : ]
        frame = pickle.loads(frame)
        cv2.imshow('Client', frame)
        if cv2.waitKey(10) == 13:
            break
    cv2.destroyAllWindows()
    
t_receiver = threading.Thread(target=receiver)
t_receiver.start()