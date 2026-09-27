import math


class GestureController:

    def __init__(self):

        # Previous index-finger position
        self.previous_position = None

        # Previous wrist rotation
        self.previous_angle = None

        # Previous distance between two hands
        self.previous_two_hand_distance = None

    # ========================================================
    # DISTANCE
    # ========================================================

    def distance(self, p1, p2):

        return math.sqrt(
            (p1[0] - p2[0]) ** 2 +
            (p1[1] - p2[1]) ** 2
        )

    # ========================================================
    # PINCH
    # ========================================================

    def is_pinch(self, hand):

        thumb = hand.landmark[4]
        index = hand.landmark[8]

        d = math.sqrt(
            (thumb.x - index.x) ** 2 +
            (thumb.y - index.y) ** 2
        )

        return d < 0.055

    # ========================================================
    # OPEN PALM
    # ========================================================

    def is_open_palm(self, hand):

        fingers = [
            (8, 6),
            (12, 10),
            (16, 14),
            (20, 18)
        ]

        extended = 0

        for tip, joint in fingers:

            if hand.landmark[tip].y < hand.landmark[joint].y:

                extended += 1

        return extended >= 3

    # ========================================================
    # FIST
    # ========================================================

    def is_fist(self, hand):

        fingers = [
            (8, 6),
            (12, 10),
            (16, 14),
            (20, 18)
        ]

        closed = 0

        for tip, joint in fingers:

            if hand.landmark[tip].y > hand.landmark[joint].y:

                closed += 1

        return closed >= 3

    # ========================================================
    # UPDATE
    # ========================================================

    def update(self, hands):

        gesture = "IDLE"

        movement = (0.0, 0.0)

        rotation = (0.0, 0.0, 0.0)

        zoom = 0.0

        hide = False

        # ====================================================
        # TWO HAND ZOOM
        # ====================================================

        if len(hands) == 2:

            hand1 = hands[0]
            hand2 = hands[1]

            p1 = (
                hand1.landmark[8].x,
                hand1.landmark[8].y
            )

            p2 = (
                hand2.landmark[8].x,
                hand2.landmark[8].y
            )

            current_distance = self.distance(
                p1,
                p2
            )

            if self.previous_two_hand_distance is not None:

                delta = (
                    current_distance
                    - self.previous_two_hand_distance
                )

                zoom = delta * 4.0

            self.previous_two_hand_distance = current_distance

            gesture = "TWO HAND ZOOM"

        else:

            self.previous_two_hand_distance = None

        # ====================================================
        # SINGLE HAND
        # ====================================================

        if len(hands) >= 1:

            hand = hands[0]

            index = hand.landmark[8]

            current_position = (
                index.x,
                index.y
            )

            # =================================================
            # PINCH = MOVE OBJECT
            # =================================================

            if self.is_pinch(hand):

                gesture = "PINCH / GRAB"

                if self.previous_position is not None:

                    old_x, old_y = self.previous_position

                    dx = (
                        current_position[0]
                        - old_x
                    )

                    dy = (
                        current_position[1]
                        - old_y
                    )

                    movement = (
                        dx * 900,
                        dy * 650
                    )

                self.previous_position = current_position

                # Don't calculate rotation while pinching
                self.previous_angle = None

            # =================================================
            # OPEN PALM = 3 AXIS ROTATION
            # =================================================

            elif self.is_open_palm(hand):

                gesture = "3D ROTATE"

                # ---------------------------------------------
                # HAND MOVEMENT
                # ---------------------------------------------

                if self.previous_position is not None:

                    old_x, old_y = self.previous_position

                    dx = (
                        current_position[0]
                        - old_x
                    )

                    dy = (
                        current_position[1]
                        - old_y
                    )

                    # Horizontal hand movement
                    # → Y axis rotation
                    ry = dx * 700

                    # Vertical hand movement
                    # → X axis rotation
                    rx = dy * 700

                else:

                    rx = 0.0
                    ry = 0.0

                self.previous_position = current_position

                # ---------------------------------------------
                # WRIST ROTATION
                # ---------------------------------------------

                wrist = hand.landmark[0]

                middle = hand.landmark[9]

                wrist_dx = (
                    middle.x - wrist.x
                )

                wrist_dy = (
                    middle.y - wrist.y
                )

                current_angle = math.degrees(
                    math.atan2(
                        wrist_dy,
                        wrist_dx
                    )
                )

                rz = 0.0

                if self.previous_angle is not None:

                    delta_angle = (
                        current_angle
                        - self.previous_angle
                    )

                    # Prevent 360 degree jumps

                    if delta_angle > 180:

                        delta_angle -= 360

                    elif delta_angle < -180:

                        delta_angle += 360

                    rz = delta_angle * 1.5

                self.previous_angle = current_angle

                rotation = (
                    rx,
                    ry,
                    rz
                )

            # =================================================
            # FIST
            # =================================================

            elif self.is_fist(hand):

                gesture = "FIST"

                hide = True

                self.previous_position = None
                self.previous_angle = None

            # =================================================
            # NO SPECIAL GESTURE
            # =================================================

            else:

                self.previous_position = None
                self.previous_angle = None

        else:

            self.previous_position = None
            self.previous_angle = None

        return {
            "gesture": gesture,
            "movement": movement,
            "rotation": rotation,
            "zoom": zoom,
            "hide": hide
        }