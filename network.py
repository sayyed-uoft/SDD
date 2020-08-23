import numpy as np
import time
import cv2
import plot

CONFID = 0.5
THRESH = 0.5


class Yolo3:
    def __init__(self):
        pass

    def initialize(self, model_path):
        # Load Yolov3 weights
        weights_path = model_path + "yolov3.weights"
        config_path = model_path + "yolov3.cfg"
        self.net = cv2.dnn.readNetFromDarknet(config_path, weights_path)
        lnames = self.net.getLayerNames()
        self.layer_names = [lnames[layer[0] - 1] for layer in self.net.getUnconnectedOutLayers()]

    def detect_people(self, image):
        print("Start detecting ...")
        (H, W) = image.shape[:2]
        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        self.net.setInput(blob)
        start = time.time()
        layer_outputs = self.net.forward(self.layer_names)
        end = time.time()
        boxes = []
        confidences = []
        class_ids = []   
    
        for output in layer_outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                # detecting people in the image
                if class_id == 0:

                    if confidence > CONFID:

                        box = detection[0:4] * np.array([W, H, W, H])
                        (center_x, center_y, width, height) = box.astype("int")

                        x = int(center_x - (width / 2))
                        y = int(center_y - (height / 2))

                        boxes.append([x, y, int(width), int(height)])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)
                    
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, CONFID, THRESH)
        font = cv2.FONT_HERSHEY_PLAIN
        boxes1 = []
        for i in range(len(boxes)):
            if i in idxs:
                boxes1.append(boxes[i])
                x,y,w,h = boxes[i]

        print(len(boxes1))
        if len(boxes1) == 0:
            return image
            
        image_copy = np.copy(image)
        
        #image = plot.social_distancing_view(image_copy, bxs_mat, boxes1, risk_count) #TODO
        image = plot.detection_view(image_copy, boxes1)
        
        return image
