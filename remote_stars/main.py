import numpy as np
import matplotlib.pyplot as plt
import socket
from skimage.measure import label, regionprops

host = "84.237.21.36"

port = 5152

def recvall(sock,n):
    data = bytearray()
    while len(data) <n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host,port))
    beat = b"nope"

    plt.ion()
    plt.figure()

    while beat != b"yep":
    
        sock.send(b"get")
        bts = recvall(sock, 40002)
        #print(len(bts))

        im1 = np.frombuffer(bts[2:40002], dtype="uint8").reshape(bts[0],bts[1])
        #im2 = np.frombuffer(bts[40004:], dtype="uint8").reshape(bts[40002],bts[40003])

        #pos1 = np.unravel_index(np.argmax(im1),im1.shape)
        #pos2 = np.unravel_index(np.argmax(im2),im2.shape)
        binary = im1>100
        labeled = label(binary)
        regions = regionprops(labeled)
        if len(regions)<2:
            print("Звезды слиплись")
            continue
        pos1 = regions[0].centroid
        pos2 = regions[1].centroid
        print(pos1,pos2)
        result =((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2)**(0.5)
        sock.send(f"{round(result,1)}".encode())
        print(round(result,1))
        print(sock.recv(10))

        plt.clf()
        plt.subplot(121)
        plt.imshow(im1)
        #plt.subplot(122)
        #plt.imshow(im2)
        plt.pause(1)

        sock.send(b"beat")
        beat = sock.recv(10)
