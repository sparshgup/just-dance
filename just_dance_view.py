import numpy as np
import cv2


class JustDanceView:
    def __init__(self, model):
        self.model = model
        self.score = 0

    def display_song_frame(self):
        # Display the score and to choose the next song or end game
        pass

    def display_start_game(self):
        # Displays initial frame to prompt the user to start the game
        pass

    def display_end_game(self):
        # Displays final frame with total score
        pass

    @staticmethod
    def display_frame(frame, window_name):
        cv2.imshow(window_name, frame)
        cv2.waitKey(10)

    def process_frame(self, frame):
        img = cv2.resize(frame, (192, 192))
        img = np.expand_dims(img, axis=0)
        key_points_with_scores = self.model.run_inference(img)
        return key_points_with_scores

    @staticmethod
    def draw_connections(frame, key_points, edges, confidence_threshold):
        y, x, c = frame.shape
        shaped = key_points * [y, x, 1]
        shaped = np.squeeze(shaped)

        for (p1, p2), color in edges.items():
            y1, x1, c1 = shaped[p1]
            y2, x2, c2 = shaped[p2]

            if c1 > confidence_threshold and c2 > confidence_threshold:
                cv2.line(
                    frame,
                    (int(x1), int(y1)), (int(x2), int(y2)),
                    (0, 0, 255), 2
                )

    @staticmethod
    def draw_key_points(frame, key_points, confidence_threshold):
        y, x, channel = frame.shape
        shaped = key_points * [y, x, 1]
        shaped = np.squeeze(shaped)

        for key_point in shaped:
            key_y, key_x, keypoint_conf = key_point
            if keypoint_conf > confidence_threshold:
                cv2.circle(frame, (int(key_x), int(key_y)), 4, (0, 255, 0), -1)