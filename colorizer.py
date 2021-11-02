import numpy as np
import cv2

def add_color(file_path):
    net = cv2.dnn.readNetFromCaffe('.\\model\\colorization_deploy_v2.prototxt', '.\\model\\colorization_release_v2.caffemodel')
    points = np.load('.\\model\\pts_in_hull.npy')

    class8 = net.getLayerId("class8_ab")
    conv8 = net.getLayerId("conv8_313_rh")
    points = points.transpose().reshape(2, 313, 1, 1)
    net.getLayer(class8).blobs = [points.astype("float32")]
    net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]

    img = cv2.imread(file_path)
    scaled = img.astype("float32") / 255.0
    lab_img = cv2.cvtColor(scaled, cv2.COLOR_BGR2LAB)

    resized_img = cv2.resize(lab_img, (224, 224))
    L = cv2.split(resized_img)[0]
    L -= 50

    net.setInput(cv2.dnn.blobFromImage(L))
    ab = net.forward()[0, :, :, :].transpose((1, 2, 0))

    ab = cv2.resize(ab, (img.shape[1], img.shape[0]))

    L = cv2.split(lab_img)[0]
    colorized_img = np.concatenate((L[:, :, np.newaxis], ab), axis=2)

    colorized_img = cv2.cvtColor(colorized_img, cv2.COLOR_LAB2BGR)
    colorized_img = np.clip(colorized_img, 0, 1)

    colorized_img = (255 * colorized_img).astype("uint8")
    return colorized_img
