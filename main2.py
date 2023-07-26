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

from helper_functions_main import generate_detections,\
draw_frame_info, update_tracker, update_intersections, display_intersections, update_all_roi_transitions, display_transitions
import warnings


video_name = "camera_01-FRENTE_main_20230706103457.dav"
video_path = os.path.join(".","sample_data",video_name)


output_dir = "out_data"
video_out_path = os.path.join( output_dir, os.path.splitext(video_name)[0] + "_out.mp4")

rois = get_rois(video_path)

YOLO_PATH = "/home/tenache89/blackfish/video_detectioin3/download/runs/detect/train4/weights/best.pt"


# TODO: mejorar transitions
def detect_frames(video_name, video_path, \
                  video_out_path, show_me=False, max_frames=None, rois=None, \
                    debug=False, display="intersections", yolo_path = YOLO_PATH):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError("Error opening video file")

    video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    
    ret, frame = cap.read()
    cap_out = cv2.VideoWriter(video_out_path, cv2.VideoWriter_fourcc(*'mp4v'), cap.get(cv2.CAP_PROP_FPS), (frame.shape[1], frame.shape[0]))
    if yolo_path is None:
        model = YOLO("yolov8n.pt")
    else:
        model = YOLO(yolo_path)
    tracker = Tracker()
    colors, colors_roi = generate_color_sets(2, 10)
    
    all_detections = []
    all_detections_roi = [[] for _ in range(len(rois))]
    all_people = set()
    all_people_roi = [set() for _ in range(len(rois))]
    intersections = {}
    
    # Initialization
    last_roi = {track_id: None for track_id in all_people}
    transitions = {}

    frame_count = 0
    max_frames = max_frames if max_frames else int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    while ret and frame_count < max_frames:
        results = model(frame)
        detections, detections_roi, all_detections, all_detections_roi = generate_detections(rois, results, [], [], all_detections, all_detections_roi)
        all_people, all_people_roi = update_tracker(tracker, frame, detections, all_people, rois, all_people_roi, detections_roi)
        
        for track_id in all_people:
            if track_id not in last_roi:
                last_roi[track_id] = None
        
        if display == "transitions":
            # After updating the tracker, you can update all ROI transitions
            transitions, last_roi = update_all_roi_transitions(all_people_roi, transitions, last_roi)
            frame = display_transitions(frame, transitions, video_width, video_height)
        elif display == "intersections":
            intersections, wait = update_intersections(all_people_roi, intersections, debug)
            frame = display_intersections(frame, intersections, video_width, video_height)
        else:
            warnings.warn(f"Invalid display type: {display}. Valid options are 'transitions' or 'intersections'. No information of people movement will be displayed")
            print('\n')
        frame = draw_frame_info(tracker, frame, colors, show_me, rois, colors_roi)
        
        if show_me:    
            cv2.imshow("frame", frame)
            cv2.waitKey(10)
        cap_out.write(frame)
        ret, frame = cap.read()
        frame_count += 1

    cap.release()
    cap_out.release()
    cv2.destroyAllWindows()
    
    return all_detections, video_height, video_width

if __name__ == "__main__":
    detect_frames(video_name, video_path, video_out_path, rois=rois)