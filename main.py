import cv2
import time
import numpy as np

from hand_tracker import HandTracker
from gesture_controller import GestureController
from holo_object import HoloObject
from image_searcher import ImageSearcher


def main():
    # --------------------------------------------------------
    # Components
    # --------------------------------------------------------
    tracker = HandTracker()
    controller = GestureController()
    holo_object = HoloObject()
    searcher = ImageSearcher()

    # --------------------------------------------------------
    # Interactive Search & Notification State
    # --------------------------------------------------------
    search_active = False
    search_query = ""
    status_notification = "WELCOME TO HOLO3D! PRESS 'S' TO SEARCH ANY 3D OBJECT"
    status_timer = time.time() + 6.0

    def on_image_fetched(hologram_texture, query):
        nonlocal status_notification, status_timer
        if hologram_texture is not None:
            # Update texture on current volumetric or procedural model
            holo_object.hologram_texture = hologram_texture
            status_notification = f"TEXTURE APPLIED FOR '{query.upper()}' IN 3D SPACE!"
        status_timer = time.time() + 4.0

    # --------------------------------------------------------
    # Camera Initialization
    # --------------------------------------------------------
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    if not camera.isOpened():
        print("ERROR: Could not open webcam.")
        return

    print()
    print("=======================================================")
    print("      HOLO3D — FUTURISTIC 3D AUGMENTED INTERFACE       ")
    print("=======================================================")
    print()
    print("  GESTURE CONTROLS:")
    print("    PINCH & DRAG -> Move 3D Object in Space")
    print("    OPEN PALM    -> 3D Pitch / Yaw / Roll Rotation")
    print("    TWO HANDS    -> Dynamic Pinch to Zoom / Scale")
    print("    FIST         -> Stealth Cloak / Hide Object")
    print()
    print("  KEYBOARD CONTROLS:")
    print("    S or SPACE   -> Search ANY Object (House, Earth, Car, Robot, etc.)")
    print("    1            -> 3D Cyber Supercar")
    print("    2            -> 3D Planet Earth Globe")
    print("    3            -> 3D Architectural House")
    print("    4            -> 3D Iron Man Arc Reactor")
    print("    5            -> 3D Sci-Fi Drone Fighter")
    print("    6            -> 3D Cyber Katana Sword")
    print("    7            -> 3D Cybernetic Mech Robot")
    print("    8            -> 3D Cybernetic Skull")
    print("    9            -> 3D Spaceship UFO")
    print("    + / -        -> Manual Zoom In / Zoom Out")
    print("    R            -> Reset Transform (Position & Rotation)")
    print("    V            -> Toggle Hologram Visibility")
    print("    Q            -> Quit")
    print("=======================================================")
    print()

    prev_time = time.time()
    fps = 30.0

    # --------------------------------------------------------
    # Main Application Loop
    # --------------------------------------------------------
    while True:
        success, frame = camera.read()
        if not success:
            break

        # Mirror camera feed for natural interaction
        frame = cv2.flip(frame, 1)
        height, width = frame.shape[:2]

        curr_time = time.time()
        fps = 0.9 * fps + 0.1 * (1.0 / max(0.001, curr_time - prev_time))
        prev_time = curr_time

        # ----------------------------------------------------
        # Hand Tracking & Gesture Recognition
        # ----------------------------------------------------
        result = tracker.process(frame)
        detected_hands = []
        if result.multi_hand_landmarks:
            detected_hands = result.multi_hand_landmarks

        state = controller.update(detected_hands)
        gesture = state["gesture"]
        movement = state["movement"]
        rotation = state["rotation"]
        zoom = state["zoom"]
        hide = state["hide"]

        # Only apply gestures when search modal is not active
        if not search_active:
            holo_object.move(movement[0], movement[1])
            holo_object.rotate(rotation[0], rotation[1], rotation[2])
            holo_object.zoom(zoom)

            if hide:
                holo_object.visible = False
            elif gesture != "FIST":
                holo_object.visible = True

        # Draw hand skeleton landmarks
        frame = tracker.draw_landmarks(frame, result)

        # Render 3D virtual hologram
        frame = holo_object.render(frame)

        # ----------------------------------------------------
        # Futuristic HUD Header & Info Cards
        # ----------------------------------------------------
        overlay = frame.copy()

        # Top Bar
        cv2.rectangle(overlay, (0, 0), (width, 50), (12, 16, 24), -1)
        # Left HUD Panel
        cv2.rectangle(overlay, (20, 65), (360, 240), (10, 15, 25), -1)
        # Right HUD Panel
        cv2.rectangle(overlay, (width - 330, 65), (width - 20, 200), (10, 15, 25), -1)
        # Bottom Controls Bar
        cv2.rectangle(overlay, (20, height - 60), (width - 20, height - 15), (10, 15, 25), -1)

        frame = cv2.addWeighted(overlay, 0.78, frame, 0.22, 0)

        # Top Bar Content
        cv2.putText(frame, "HOLO3D // VOLUMETRIC 3D AR INTERFACE", (30, 32),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.70, (255, 255, 255), 2, cv2.LINE_AA)

        active_label = f"3D MESH: {holo_object.model_name}"
        cv2.putText(frame, active_label, (width - 530, 32),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.58, (255, 220, 80), 2, cv2.LINE_AA)

        cv2.putText(frame, f"FPS: {fps:.0f}", (width - 100, 32),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (100, 255, 100), 1, cv2.LINE_AA)

        # Left HUD Content
        cv2.putText(frame, "// GESTURE TRACKING", (35, 92),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 200, 50), 1, cv2.LINE_AA)

        tracking_status = "ACTIVE [HAND DETECTED]" if detected_hands else "WAITING FOR HANDS..."
        track_color = (80, 255, 80) if detected_hands else (100, 150, 255)
        cv2.putText(frame, f"STATUS:  {tracking_status}", (35, 122),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.48, track_color, 1, cv2.LINE_AA)

        cv2.putText(frame, f"GESTURE: {gesture}", (35, 152),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.52, (255, 255, 255), 1, cv2.LINE_AA)

        cv2.putText(frame, f"SCALE:   {holo_object.scale:.2f}x", (35, 182),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.50, (255, 255, 255), 1, cv2.LINE_AA)

        vis_str = "VISIBLE" if holo_object.visible else "CLOAKED (HIDDEN)"
        cv2.putText(frame, f"RENDER:  {vis_str}", (35, 212),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.48, (255, 255, 255), 1, cv2.LINE_AA)

        # Right HUD Content (3D Spatial Telemetry)
        cv2.putText(frame, "// 3D SPATIAL TELEMETRY", (width - 315, 92),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.52, (255, 200, 50), 1, cv2.LINE_AA)

        cv2.putText(frame, f"X, Y OFFSET: {holo_object.x:+.0f}, {holo_object.y:+.0f}",
                    (width - 315, 122), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (255, 255, 255), 1, cv2.LINE_AA)

        cv2.putText(frame, f"ROTATION X:  {holo_object.rotation_x % 360:.0f} deg",
                    (width - 315, 147), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (255, 255, 255), 1, cv2.LINE_AA)

        cv2.putText(frame, f"ROTATION Y:  {holo_object.rotation_y % 360:.0f} deg",
                    (width - 315, 172), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (255, 255, 255), 1, cv2.LINE_AA)

        # Bottom Bar Controls
        controls_text = (
            "PRESS [S]: SEARCH ANY 3D OBJECT (House, Earth, Car, etc.) | [1-9]: 3D MODELS | "
            "PINCH: MOVE | PALM: ROTATE | 2 HANDS: ZOOM | R: RESET | Q: QUIT"
        )
        cv2.putText(frame, controls_text, (35, height - 32),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (230, 240, 255), 1, cv2.LINE_AA)

        # ----------------------------------------------------
        # Notification Toast
        # ----------------------------------------------------
        if searcher.is_fetching:
            fetch_box = frame.copy()
            cv2.rectangle(fetch_box, (width // 2 - 300, 65), (width // 2 + 300, 115), (20, 25, 45), -1)
            frame = cv2.addWeighted(fetch_box, 0.85, frame, 0.15, 0)
            dot_count = int(time.time() * 3) % 4
            cv2.putText(frame, f"ENHANCING 3D TEXTURE FOR '{searcher.last_query.upper()}'{'.' * dot_count}",
                        (width // 2 - 270, 97), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (80, 240, 255), 2, cv2.LINE_AA)
        elif time.time() < status_timer:
            toast_box = frame.copy()
            tw = min(720, len(status_notification) * 13 + 60)
            cv2.rectangle(toast_box, (width // 2 - tw // 2, 65), (width // 2 + tw // 2, 115), (15, 20, 35), -1)
            frame = cv2.addWeighted(toast_box, 0.85, frame, 0.15, 0)
            cv2.putText(frame, status_notification, (width // 2 - tw // 2 + 25, 97),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.52, (255, 240, 140), 1, cv2.LINE_AA)

        # ----------------------------------------------------
        # Interactive Search Modal
        # ----------------------------------------------------
        if search_active:
            modal = frame.copy()
            mw, mh = 660, 180
            mx = (width - mw) // 2
            my = (height - mh) // 2
            cv2.rectangle(modal, (mx, my), (mx + mw, my + mh), (15, 18, 30), -1)
            cv2.rectangle(modal, (mx, my), (mx + mw, my + mh), (255, 200, 40), 2)
            cv2.rectangle(modal, (mx + 30, my + 75), (mx + mw - 30, my + 125), (30, 35, 50), -1)
            cv2.rectangle(modal, (mx + 30, my + 75), (mx + mw - 30, my + 125), (100, 220, 255), 1)

            frame = cv2.addWeighted(modal, 0.90, frame, 0.10, 0)

            cv2.putText(frame, "JARVIS 3D OBJECT SEARCH & MATERIALIZER", (mx + 35, my + 45),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 220, 50), 2, cv2.LINE_AA)

            cursor = "_" if int(time.time() * 2) % 2 == 0 else ""
            display_text = f"> {search_query}{cursor}"
            cv2.putText(frame, display_text, (mx + 45, my + 110),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.70, (255, 255, 255), 2, cv2.LINE_AA)

            cv2.putText(frame, "TYPE ANY 3D OBJECT (House, Earth, Car, Robot, etc.) | ENTER: MATERIALIZE | ESC: CANCEL",
                        (mx + 35, my + 155), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (180, 200, 220), 1, cv2.LINE_AA)

        # ----------------------------------------------------
        # Display Window & Key Handling
        # ----------------------------------------------------
        cv2.imshow("Holo3D - Free Air Augmented Interface", frame)
        key = cv2.waitKey(1) & 0xFF

        if search_active:
            if key == 27:  # ESC to cancel
                search_active = False
            elif key in [10, 13]:  # ENTER to submit search
                search_active = False
                query_clean = search_query.strip()
                if query_clean:
                    # Instantly materialize true 3D model!
                    holo_object.set_hologram_by_query(query_clean)
                    status_notification = f"MATERIALIZED: '{holo_object.model_name}' IN TRUE 3D SPACE!"
                    status_timer = time.time() + 6.0
                    searcher.search_and_process_async(query_clean, on_image_fetched)
            elif key == 8:  # BACKSPACE
                search_query = search_query[:-1]
            elif 32 <= key <= 126:  # Printable character
                search_query += chr(key)
        else:
            if key == ord("q"):
                break
            elif key == ord("s") or key == 32:  # 's' or space opens search
                search_active = True
                search_query = ""
            elif key == ord("1"):
                holo_object.set_model(HoloObject.MODEL_SUPERCAR)
                status_notification = "LOADED: 3D CYBER SUPERCAR"
                status_timer = time.time() + 3.0
            elif key == ord("2"):
                holo_object.set_model(HoloObject.MODEL_GLOBE)
                status_notification = "LOADED: 3D PLANET EARTH GLOBE"
                status_timer = time.time() + 3.0
            elif key == ord("3"):
                holo_object.set_model(HoloObject.MODEL_HOUSE)
                status_notification = "LOADED: 3D ARCHITECTURAL HOUSE"
                status_timer = time.time() + 3.0
            elif key == ord("4"):
                holo_object.set_model(HoloObject.MODEL_ARC_REACTOR)
                status_notification = "LOADED: 3D IRON MAN ARC REACTOR"
                status_timer = time.time() + 3.0
            elif key == ord("5"):
                holo_object.set_model(HoloObject.MODEL_DRONE)
                status_notification = "LOADED: 3D SCI-FI DRONE FIGHTER"
                status_timer = time.time() + 3.0
            elif key == ord("6"):
                holo_object.set_model(HoloObject.MODEL_SWORD)
                status_notification = "LOADED: 3D CYBER KATANA SWORD"
                status_timer = time.time() + 3.0
            elif key == ord("7"):
                holo_object.set_model(HoloObject.MODEL_ROBOT)
                status_notification = "LOADED: 3D CYBERNETIC MECH ROBOT"
                status_timer = time.time() + 3.0
            elif key == ord("8"):
                holo_object.set_model(HoloObject.MODEL_SKULL)
                status_notification = "LOADED: 3D CYBERNETIC SKULL"
                status_timer = time.time() + 3.0
            elif key == ord("9"):
                holo_object.set_model(HoloObject.MODEL_UFO)
                status_notification = "LOADED: 3D CYBER SPACESHIP UFO"
                status_timer = time.time() + 3.0
            elif key in [ord("+"), ord("=")]:
                holo_object.zoom(0.1)
            elif key in [ord("-"), ord("_")]:
                holo_object.zoom(-0.1)
            elif key == ord("r"):
                holo_object.reset()
                status_notification = "HOLOGRAM TRANSFORM RESET TO DEFAULT"
                status_timer = time.time() + 3.0
            elif key == ord("v"):
                holo_object.visible = not holo_object.visible
                status_notification = f"HOLOGRAM VISIBILITY: {'ON' if holo_object.visible else 'OFF'}"
                status_timer = time.time() + 3.0

    # --------------------------------------------------------
    # Cleanup
    # --------------------------------------------------------
    camera.release()
    cv2.destroyAllWindows()
    tracker.close()


if __name__ == "__main__":
    main()