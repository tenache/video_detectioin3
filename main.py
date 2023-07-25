from deep_sort.deep_sort.tracker import Tracker
from deep_sort.tools import generate_detections as gdet 
import os
import cv2
from ultralytics import YOLO
from tracker import Tracker
import random
from detect_area2 import get_rois

from functools import reduce
from colors import generate_color_sets
from time import sleep

video_name = "camera_01-FRENTE_main_20230706103457.dav"
video_path = os.path.join(".","sample_data",video_name)


output_dir = "out_data"
video_out_path = os.path.join( output_dir, os.path.splitext(video_name)[0] + "_out.mp4")

rois = get_rois(video_path)


def detect_frames(
    video_name=video_name, 
    video_path=video_path,
    video_out_path =video_out_path, 
    show_me=True, 
    max_frames= None,
    rois=rois,
    debug = False
    ):
    print("We are here")

    # cap = cv2.VideoCapture("rtsp://thomas:thomas123456@172.20.208.1:554/cam/realmonitor?channel=1&subtype=0")
  
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error opening video file")
        
    video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"video height is {video_height}")
    print(f"frame count is {int(cap.get(cv2.CAP_PROP_FRAME_COUNT))} in the beginning")
    
    video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    all_people = set()
    all_people_roi = [set() for _ in range(len(rois))] 
    people_move = []
    intersections = {
        
    }
    
    
    ret, frame = cap.read()
    # print(f"frame is {frame}")

    # cap_out = cv2.VideoWriter(video_out_path, cv2.VideoWriter_fourcc(*'MP4V'), cap.get(cv2.CAP_PROP_FPS),(frame.shape[1], frame.shape[0]) )
    cap_out = cv2.VideoWriter(video_out_path, cv2.VideoWriter_fourcc(*'mp4v'), cap.get(cv2.CAP_PROP_FPS), (frame.shape[1], frame.shape[0]))

    print("we are here 2")
    
    model = YOLO("yolov8n.pt")
    # model = YOLO("yolov3n.pt")
    print("we are here 3")

    tracker = Tracker()
    
    print("we are here 4")
    

    colors, colors_roi = generate_color_sets(2, 10)
    all_detections = []
    all_detections_roi = [[] for _ in range(len(rois))]
    frame_count = 0
    if max_frames is None:
        max_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print(f"max_frames is {max_frames}")
    while ret and frame_count < max_frames:
        wait = False
    # while frame_count < 25:
        results = model(frame)
        result = results[0]
        detections = []
        detections_roi = [[] for _ in range(len(rois))]
        
        for r in result.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = r # all objects in coco_classes
            if class_id == 0:
                detections.append([int(x1), int(y1),int(x2), int(y2), int(score)])
                all_detections.append((int(x1),int(y1),int(x2),int(y2)))
                if rois is not None:
                    for i, roi in enumerate(rois):
                        if roi[0] <= x1 < roi[0] + roi[2] and roi[1] <= y1 < roi[1] + roi[3] and roi[0] < x2 <= roi[0] + roi[2] and roi[1] < y2 <= roi[1] + roi[3]:
                            detections_roi[i].append([int(x1), int(y1),int(x2), int(y2), int(score)])
                            all_detections_roi[i].append((int(x1),int(y1),int(x2),int(y2)))
                                   
        print(" we are here 5")
        if detections:
            print(f"detections is {detections}")
            tracker.update(frame, detections)  # the most importante function 
            for track in tracker.tracks:
                all_people.add(track.track_id)
                
        if rois is not None:
            for i, roi in enumerate (rois):
                if detections_roi[i]:
                    print(rois)
                    print(f"detectons_roi is {detections_roi}")
                    sleep(1)
                    print(f"detections_roi[i] is {detections_roi[i]}")
                    sleep(1)
                    tracker.update(frame, detections_roi[i])
                    for track in tracker.tracks:
                        all_people_roi[i].add(track.track_id)
                        
                      
        if rois is not None:
            for i, unique_people in enumerate(all_people_roi):
                for j, unique_people2 in enumerate(all_people_roi):
                    if unique_people != unique_people2:
                        inters = unique_people.intersection(unique_people2)
                        if inters:
                            if j in intersections.keys() and i in intersections[j].keys():
                                break
                            if i not in intersections.keys():
                                print(f"i is {i}")
                                print(f"j is {j}")
                                intersections[i] = {j:inters}
                            else:
                                if j in intersections[i].keys():
                                    if inters != intersections[i][j] and debug:
                                        wait = True
                                intersections[i][j] = inters
                            # people_move.append((inters, i, j))
              
       
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.0
        color = (255, 255, 255)  # Text color (in BGR format)
        thickness = 2  # Text thickness
        texts = []
        for i in intersections:
            for j in intersections[i]:
                texts.append(f"{len(intersections[i][j])} personas se movieron entre las zonas {i} y {j}")
                if wait and debug:
                    print(f"intersections[{i}][{j}] is {intersections[i][j]}")
                    # wait = False
                    k = cv2.waitKey(0) & 0xFF
                    if k ==ord('q'):
                        break
                
            
        # text = f"{len(reduce(set.union, all_people_roi))} personas de {len(all_people)} entraron "
        print("all people roi is ")
        print(set.union, all_people_roi)
        for i, text in enumerate(texts):
            text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)
            text_width, text_height = text_size
            # Specify the position to write the text
            position = (int((video_width - text_width) / 2), video_height - int(0.05 *i * video_height))  
            cv2.putText(frame, text, position, font, font_scale, color, thickness)  
                   
        
        if tracker.tracks is not None:
            print(f"len of tracker.tracks is {len(all_people)}")
            for track in tracker.tracks:
                bbox = track.bbox
                x1, y1, x2, y2 = bbox
                track_id = track.track_id
                
                # cv2.rectangle(frame, (x1, y1), (x2, y2), (colors[track_id % len(colors)]), 3)
                if show_me:
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (colors[track_id % len(colors)]), 2)
                    for i, roi in enumerate(rois):
                        cv2.rectangle(frame, (int(roi[0]), int(roi[1])), (int(roi[0])+ int(roi[2]), int(roi[1])+int(roi[3])), (colors_roi[i % len(colors_roi)]), 4 )

        
                    # cv2.rectangle(frame,((x1, y1),(x2, y2), (colors[track_id % len(colors)])),3)
            
                
        # print(detections)
        if show_me:    
            cv2.imshow("frame", frame)
            cv2.waitKey(10)
        cap_out.write(frame) # metemos el frame en el output file
        ret, frame = cap.read() # leemos nuevos frames
        frame_count +=1
        

    
    cap.release() # no estoy seguro que hace, pero el vago parecia asustado cuando se olvido...
    cap_out.release()  # no estoy seguro que hace, pero el vago parecia asustado cuando se olvido...
    cv2.destroyAllWindows() # hahahaha!
    print(f"frame count is {frame_count}")
    return all_detections, video_height, video_width 

if __name__ == "__main__":
    detect_frames()
    