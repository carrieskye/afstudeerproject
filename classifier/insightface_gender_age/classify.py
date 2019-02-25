import os
import cv2
import mxnet as mx
from classifier.insightface_gender_age.mtcnn_detector import MtcnnDetector
from classifier.insightface_gender_age.common import face_preprocess
import numpy as np

image_size = (112, 112)
prefix = 'models/insightface_gender_age/model/model'
epoch = 0
gpu = -1
# mtcnn option, 1 means using R+O, 0 means detect from beginning
layer = 'fc1'
det = 0
det_minsize = 50
det_threshold = [.6, .7, .8] if det == 0 else [0, 0, .2]

ctx = mx.cpu()  # mx.gpu(gpu-id) to use gpu

sym, arg_params, aux_params = mx.model.load_checkpoint(prefix, epoch)
all_layers = sym.get_internals()
sym = all_layers[layer + '_output']
model = mx.mod.Module(symbol=sym, context=ctx, label_names=None)
model.bind(data_shapes=[('data', (1, 3, image_size[0], image_size[1]))])
model.set_params(arg_params, aux_params)

mtcnn_path = './models/insightface_gender_age/mtcnn-model'
detector = MtcnnDetector(model_folder=mtcnn_path,
                         ctx=ctx, num_worker=1, accurate_landmark=True,
                         threshold=det_threshold)


def classify(frame, face):
    x, y, w, h = face

    # width, height = face_img.shape

    face_img = frame[y:y+h, x:x+w]
    face_img_resize = cv2.resize(face_img, (112, 112))
    #face_img = frame[x1:x2, y1:y2]

    # cv2.imshow('FACE', face_img_resize)
    ret = detector.detect_face(face_img, det)
    if ret is None:
        print("Got no face?")
        return None, None, None
    bbox, points = ret
    if bbox.shape[0] == 0:
        print("not good bounding box?")
        return None, None, None

    bbox = bbox[0, 0:4]
    points = points[0, :].reshape((2, 5)).T
    # print("bbox  ", bbox)
    # print("points", points)
    nimg = face_preprocess.preprocess(face_img, bbox, points, image_size='112,112')
    nimg = cv2.cvtColor(nimg, cv2.COLOR_BGR2RGB)
    aligned = np.transpose(nimg, (2, 0, 1))
    input_blob = np.expand_dims(aligned, axis=0)
    data = mx.nd.array(input_blob)
    db = mx.io.DataBatch(data=(data,))

    model.forward(db, is_train=False)
    ret = model.get_outputs()[0].asnumpy()
    g = ret[:, 0:2].flatten()
    g_max = np.argmax(g)
    gender = 'M' if g_max > .5 else 'F'
    a = ret[:, 2:202].reshape((100, 2))
    a = np.argmax(a, axis=1)
    age = int(sum(a))

    return age, gender, g_max

