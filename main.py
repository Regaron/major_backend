import asyncio
import websockets
import base64
import matplotlib.pyplot as plt
import time


async def img_receive(web_socket, df):
    img_string = await web_socket.recv()
    img_string = img_string.split(",")
    print(img_string[1])
    img_data = base64.b64decode(img_string[0])
    # buf_arr = np.frombuffer(img_data, dtype=np.uint8)
    # print(buf_arr)
    # img = cv2.imdecode(buf_arr, 1)
    # plt.imshow(img)
    # plt.show()
    received_image = open('received.jpg', 'wb')
    received_image.write(img_data)

    img = plt.imread('received.jpg')
    plt.imshow(img)
    plt.show()
    # Call MaskRCNN Function
    # Send Its Output
    send_image = open('send.jpg', 'rb')
    image_read = send_image.read()
    image_encoded = base64.b64encode(image_read)
    image_encoded = image_encoded.decode("utf-8")
    act_building = 2
    pre_building = 3
    act_area = 20
    pre_area = 20
    await web_socket.send(image_encoded+","+str(act_building)+","+str(pre_building)+","+str(act_area)+","+str(pre_area))

start_server = websockets.serve(img_receive, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
