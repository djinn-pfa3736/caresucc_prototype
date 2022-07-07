import cv2
import numpy as np
import mediapipe as mp

import pdb

def calc_inner(a, b):
    a = np.array(a)
    b = np.array(b)
    inner = np.sum(a*b)

    return inner

def calc_angle(x1, x2, x3):
    x1 = np.array(x1)
    x2 = np.array(x2)
    x3 = np.array(x3)

    a = x1 - x2
    b = x3 - x2

    inner = self.calc_inner(a, b)
    cos_theta = inner/(np.sqrt(np.sum(a**2))*np.sqrt(np.sum(b**2)))
    theta = np.rad2deg(np.arccos(cos_theta))

    return theta

def convert_to_vector(landmark):
    x = np.array([landmark.x, landmark.y, landmark.z])

    return x

def calc_angle_from_indices(landmarks, id1, id2, id3):
    x1 = self.convert_to_vector(landmarks.landmark[id1])
    x2 = self.convert_to_vector(landmarks.landmark[id2])
    x3 = self.convert_to_vector(landmarks.landmark[id3])

    theta = self.calc_angle(x1, x2, x3)

    return theta

def extract_angle_tables(file_name, pose):

    cap = cv2.VideoCapture(file_name)

    angle_tables = []
    angle_diff_tables = []
    frame_tables =  []
    image_tables = []
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            # continue
            break

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        # Draw the pose annotation on the image.
        image.flags.writeable = True

        angle_table = []
        angle_table.append(self.calc_angle_from_indices(results.pose_landmarks, 11, 12, 14))
        angle_table.append(self.calc_angle_from_indices(results.pose_landmarks, 12, 11, 13))
        angle_table.append(self.calc_angle_from_indices(results.pose_landmarks, 12, 14, 16))
        angle_table.append(self.calc_angle_from_indices(results.pose_landmarks, 14, 12, 24))
        angle_table.append(self.calc_angle_from_indices(results.pose_landmarks, 11, 12, 24))
        angle_table.append(self.calc_angle_from_indices(results.pose_landmarks, 12, 11, 23))
        angle_table.append(self.calc_angle_from_indices(results.pose_landmarks, 13, 11, 23))
        angle_table.append(self.calc_angle_from_indices(results.pose_landmarks, 11, 13, 15))
        angle_table.append(self.calc_angle_from_indices(results.pose_landmarks, 12, 24, 26))
        angle_table.append(self.calc_angle_from_indices(results.pose_landmarks, 12, 24, 23))
        angle_table.append(self.calc_angle_from_indices(results.pose_landmarks, 11, 23, 24))
        angle_table.append(self.calc_angle_from_indices(results.pose_landmarks, 11, 13, 25))
        angle_table.append(self.calc_angle_from_indices(results.pose_landmarks, 26, 24, 23))
        angle_table.append(self.calc_angle_from_indices(results.pose_landmarks, 25, 23, 24))
        angle_table.append(self.calc_angle_from_indices(results.pose_landmarks, 24, 26, 28))
        angle_table.append(self.calc_angle_from_indices(results.pose_landmarks, 23, 25, 27))

        angle_tables.append(angle_table)
        frame_tables.append(results.pose_landmarks)
        image_tables.append(image)

    angle_tables = np.array(angle_tables)
    angle_diff_tables = self.calc_diff(angle_tables)
    cap.release()

    return angle_tables, angle_diff_tables, frame_tables, image_tables

def calc_distance_between_frames(frame1, frame2):
    dist = np.sqrt(np.sum((frame1 - frame2)**2))/len(frame1)

    return dist

def align_frames(tables1, tables2, match_threshold):

    dist_mat = np.zeros((len(tables1), len(tables2)))
    for i in range(len(tables1)):
        for j in range(len(tables2)):
            dist_mat[i, j] = self.calc_distance_between_frames(tables1[i], tables2[j])

    dp_mat = np.zeros((len(tables1) + 1, len(tables2) + 1))

    dir_mat = np.zeros((len(tables1) + 1, len(tables2) + 1))
    for i in range(1, len(tables1) + 1):
        dir_mat[i, 0] = 2

    for i in range(1, len(tables1) + 1):
        for j in range(1, len(tables2) + 1):
            if dist_mat[i - 1, j - 1] <= match_threshold:
                match_val = 1
            else:
                match_val = -1

            val1 = dp_mat[i, j - 1]
            val2 = dp_mat[i - 1, j - 1] + match_val
            val3 = dp_mat[i - 1, j]

            max_val = np.max((val1, val2, val3))
            dp_mat[i, j] = max_val

            max_idx = np.argmax((val1, val2, val3))
            dir_mat[i, j] = max_idx

    pairs = []
    i = len(tables1)
    j = len(tables2)
    while i != 0 or j != 0:
        if dir_mat[i, j] == 0:
            pairs.append(['-', j - 1])
            j -= 1
        elif dir_mat[i, j] == 1:
            pairs.append([i - 1, j - 1])
            i -= 1
            j -= 1
        else:
            pairs.append([i - 1, '-'])
            i -= 1

    pairs.reverse()
    return pairs, dist_mat

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--file1', type=str, default='file1.MOV')
    parser.add_argument('--file2', type=str, default='file2.MOV')
    parser.add_argument('--threshold', type=float, default=0.4)
    # parser.add_argument('--output', type=str, default='compare.mp4')
    args = parser.parse_args()

    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5)

    joint_info = ['14-12-11', '13-11-12', '12-14-16', '14-12-24', '24-12-11', '23-11-12']
    joint_info += ['13-11-23', '11-13-15', '12-24-26', '12-24-23', '11-23-24', '11-23-25']
    joint_info += ['26-24-23', '25-23-24', '24-26-28', '23-25-27']

    print('*** Calculation of angles has been started!! ***')
    angle_tables_1, angle_diff_tables_1, frame_tables_1, image_tables_1 = self.extract_angle_tables(args.file1, pose)
    angle_tables_2, angle_diff_tables_2, frame_tables_2, image_tables_2 = self.extract_angle_tables(args.file2, pose)

    print('*** Alignment of frames has been started!! ***')
    pairs, dist_mat = align_frames(angle_tables_1, angle_tables_2, np.pi/18)
    pair_dist_vec = []
    for pair in pairs:
        if (pair[0] != '-') and (pair[1] != '-'):
            pair_dist_vec.append(dist_mat[pair[0], pair[1]])

    # print(str(np.mean(pair_dist_vec)) + ' ± ' + str(np.sqrt(np.var(pair_dist_vec))))
    # print(str(np.min(pair_dist_vec)) + ' - ' + str(np.max(pair_dist_vec)))

    pdb.set_trace()

    self.paired_images_1 = []
    self.paired_images_2 = []
    self.paired_angles_1 = []
    self.paired_angles_2 = []
    self.pair_matched_indices = []

    pair = self.pairs[0]

    first_frame_set_flag_1 = False
    first_frame_set_flag_2 = False
    first_gap_len_1 = 0
    first_gap_len_2 = 0
    previous_image_1 = pair[0]
    previous_image_2 = pair[1]
    previous_angle_1 = []
    previous_angle_2 = []
    for i in range(len(self.pairs)):
        pair = self.pairs[i]

        if pair[0] != '-':

            image1 = cv2.cvtColor(self.image_tables_1[pair[0]], cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(
                image1,
                self.frame_tables_1[pair[0]],
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

            if not first_frame_set_flag_1:
                for i in range(first_gap_len_1):
                    self.paired_images_1 = [image1] + self.paired_images_1
                    self.paired_angles_1 = [self.angle_tables_1[pair[0]]] + self.paired_angles_1
                first_frame_set_flag_1 = True
            else:
                self.paired_images_1.append(image1)
                self.paired_angles_1.append(self.angle_tables_1[pair[0]])
            previous_image_1 = image1
            previous_angle_1 = self.angle_tables_1[pair[0]]

        else:
            if not first_frame_set_flag_1:
                first_gap_len_1 += 1
            else:
                self.paired_images_1.append(previous_image_1)
                self.paired_angles_1.append(previous_angle_1)

        if pair[1] != '-':

            image2 = cv2.cvtColor(self.image_tables_2[pair[1]], cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(
                image2,
                self.frame_tables_2[pair[1]],
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

            if not first_frame_set_flag_2:
                for i in range(first_gap_len_2):
                    self.paired_images_2 = [image2] + self.paired_images_2
                    self.paired_angles_2 = [self.angle_tables_2[pair[1]]] + self.paired_angles_2
                first_frame_set_flag_2 = True
            else:
                self.paired_images_2.append(image2)
                self.paired_angles_2.append(self.angle_tables_2[pair[1]])
            previous_image_2 = image2
            previous_angle_2 = self.angle_tables_2[pair[1]]

        else:
            if not first_frame_set_flag_2:
                first_gap_len_2 += 1
            else:
                self.paired_images_2.append(previous_image_2)
                self.paired_angles_2.append(previous_angle_2)
