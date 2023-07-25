import cv2
from functools import reduce
from time import sleep

def generate_detections(rois, results, detections, detections_roi, all_detections, all_detections_roi):
    """Generate detections for each frame"""
    result = results[0]
    detections_roi = [[] for _ in range(len(rois))]
    for r in result.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = r 
        if class_id == 0:
            detections.append([int(x1), int(y1), int(x2), int(y2), int(score)])
            all_detections.append((int(x1), int(y1), int(x2), int(y2)))
            if rois is not None:
                for i, roi in enumerate(rois):
                    if roi[0] <= x1 < roi[0] + roi[2] and roi[1] <= y1 < roi[1] + roi[3] and roi[0] < x2 <= roi[0] + roi[2] and roi[1] < y2 <= roi[1] + roi[3]:
                        print(f"i is {i}")
                        print(f"detections roi is {detections_roi}")
                        detections_roi[i].append([int(x1), int(y1), int(x2), int(y2), int(score)])
                        all_detections_roi[i].append((int(x1), int(y1), int(x2), int(y2)))
    return detections, detections_roi, all_detections, all_detections_roi

def draw_frame_info(tracker, frame, colors, show_me, rois, colors_roi):
    """Draw bounding boxes and region of interests on frames"""
    if tracker.tracks is not None:
        for track in tracker.tracks:
            bbox = track.bbox
            x1, y1, x2, y2 = bbox
            track_id = track.track_id
                
            if show_me:
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (colors[track_id % len(colors)]), 2)
                for i, roi in enumerate(rois):
                    cv2.rectangle(frame, (int(roi[0]), int(roi[1])), (int(roi[0])+ int(roi[2]), int(roi[1])+int(roi[3])), (colors_roi[i % len(colors_roi)]), 4 )
    return frame

def update_tracker(tracker, frame, detections, all_people, rois, all_people_roi, detections_roi):
    """Update tracker and gather information of unique people in each ROI"""
    if detections:
        tracker.update(frame, detections)
        for track in tracker.tracks:
            all_people.add(track.track_id)

    if rois is not None:
        for i, roi in enumerate(rois):
            # print(f"detections is {detections} inside update_tracker")
            # detections_roi = detections[i]
            # print(f'detections_roi is {detections_roi}')
            if detections_roi[i]:
                print(f"right before the offending line, detections_roi (interpreted as detections) is {detections_roi}")
                tracker.update(frame, detections_roi[i])
                for track in tracker.tracks:
                    all_people_roi[i].add(track.track_id)
    return all_people, all_people_roi

def update_intersections(all_people_roi, intersections, debug):
    """Update intersections between different ROIs"""
    wait = False
    for i, unique_people in enumerate(all_people_roi):
        for j, unique_people2 in enumerate(all_people_roi):
            if unique_people != unique_people2:
                inters = unique_people.intersection(unique_people2)
                if inters:
                    if j in intersections.keys() and i in intersections[j].keys():
                        break
                    if i not in intersections.keys():
                        intersections[i] = {j:inters}
                    else:
                        if j in intersections[i].keys():
                            if inters != intersections[i][j] and debug:
                                wait = True
                        intersections[i][j] = inters
    return intersections, wait

def display_intersections(frame, intersections, video_width, video_height):
    """Display intersections on frame"""
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.0
    color = (255, 255, 255)  # Text color (in BGR format)
    thickness = 2  # Text thickness
    texts = []
    for i in intersections:
        for j in intersections[i]:
            texts.append(f"{len(intersections[i][j])} personas se movieron entre las zonas {i} y {j}")
            
    for i, text in enumerate(texts):
        text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)
        text_width, text_height = text_size
        position = (int((video_width - text_width) / 2), video_height - int(0.05 *i * video_height))  
        cv2.putText(frame, text, position, font, font_scale, color, thickness)
    return frame

def display_transitions(frame, transitions, video_width, video_height):
    print(f"transitions is {transitions}")
    sleep(1)
    """Display intersections on frame"""
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.0
    color = (255, 255, 255)  # Text color (in BGR format)
    thickness = 2  # Text thickness
    texts = []
    for transition, count in transitions.items():
        roi1, roi2 = transition
        texts.append(f"{count} personas se movieron desde la zona {roi1} a la {roi2}")
        
    for i, text in enumerate(texts):
        text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)
        text_width , text_height = text_size
        # Specify the position to write the text
        position = (int((video_width - text_width) / 2), video_height - int(0.05 * i * video_height))
        cv2.putText(frame, text, position, font, font_scale, color, thickness)
    return frame
"""
def update_roi_transitions(transitions, last_roi, track_id, current_roi):
    if track_id in last_roi and last_roi[track_id] is not None and last_roi[track_id] != current_roi:
        # This person has moved from one ROI to another
        transition = (last_roi[track_id], current_roi)
        if transition not in transitions:
            transitions[transition] = 0
        transitions[transition] += 1
    last_roi[track_id] = current_roi
    return last_roi"""
    
"""def update_all_roi_transitions(all_people_roi, transitions, last_roi):
    print(f"all_people_roi is {all_people_roi}")
    for i, unique_people in enumerate(all_people_roi):
        print(f"all_people_roi is {all_people_roi}")
        print(f"i (i.e current_roi) is {i}")
        print(f"unique people is {unique_people}")
        for track_id in unique_people:
            last_roi = update_roi_transitions(transitions, last_roi, track_id, i)
    return transitions, last_roi
"""
def update_all_roi_transitions(all_people_roi, transitions, last_roi):
    for i, person_set in enumerate(all_people_roi):
        for person in person_set:
            if last_roi[person] is not None and last_roi[person] != i:
                if (last_roi[person], i) not in transitions:
                    transitions[(last_roi[person], i)] = 0
                transitions[(last_roi[person], i)] += 1
            last_roi[person] = i
    return transitions, last_roi

