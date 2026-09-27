import cv2
import numpy as np
import math
import time


class HoloObject:
    """
    Advanced Hologram Object Engine.
    Supports:
    1. Dynamic 3D Image Holograms (searched/generated from Google/Web/AI)
       with perspective 3D warping, multi-layer depth, glow halo,
       hologram scanlines, particle field, and cybernetic bounding box.
    2. Procedural 3D Models:
       - Cyber Supercar (High-detail wireframe & glass canopy)
       - Earth / Holographic Globe (Latitude/Longitude sphere & glowing equator)
       - Iron Man Arc Reactor (Concentric rotating energy coils & core)
       - Sci-Fi Drone / Fighter (Aerodynamic chassis, rotors, thrusters)
       - 4D Tesseract / Cyber Cube (Outer & inner hypercube)
    """

    MODEL_SUPERCAR = "SUPERCAR"
    MODEL_GLOBE = "GLOBE"
    MODEL_ARC_REACTOR = "ARC_REACTOR"
    MODEL_DRONE = "DRONE"
    MODEL_TESSERACT = "TESSERACT"
    MODEL_IMAGE_HOLOGRAM = "IMAGE_HOLOGRAM"

    def __init__(self):
        # --------------------------------------------------------
        # Transform
        # --------------------------------------------------------
        self.x = 0.0
        self.y = 0.0

        self.rotation_x = 0.0
        self.rotation_y = 0.0
        self.rotation_z = 0.0

        self.scale = 1.0
        self.visible = True

        # --------------------------------------------------------
        # Geometry for 3D meshes
        # --------------------------------------------------------
        self.vertices = []
        self.edges = []
        self.faces = []
        self.body_faces = []
        self.glass_faces = []
        self.light_edges = []

        # --------------------------------------------------------
        # Active Model & Dynamic Hologram State
        # --------------------------------------------------------
        self.current_model = self.MODEL_SUPERCAR
        self.model_name = "CYBER SUPERCAR"

        # Dynamic Image Hologram
        self.hologram_texture = None
        self.hologram_name = ""

        # Particle field for hologram ambience
        self.particles = []
        self._init_particles()

        # Build initial model
        self._build_car()

    # ================================================================
    # PARTICLE AMBIENCE
    # ================================================================

    def _init_particles(self, count=30):
        np.random.seed(42)
        self.particles = []
        for _ in range(count):
            self.particles.append({
                "pos": [
                    np.random.uniform(-3.5, 3.5),
                    np.random.uniform(-3.0, 3.0),
                    np.random.uniform(-2.0, 2.0)
                ],
                "speed": np.random.uniform(0.01, 0.035),
                "phase": np.random.uniform(0, math.pi * 2),
                "size": np.random.randint(1, 3)
            })

    # ================================================================
    # MODEL SELECTION
    # ================================================================

    def set_model(self, model_type):
        """Switches between procedural 3D models or custom image hologram."""
        self.current_model = model_type
        self.vertices = []
        self.edges = []
        self.faces = []
        self.body_faces = []
        self.glass_faces = []
        self.light_edges = []

        if model_type == self.MODEL_SUPERCAR:
            self.model_name = "CYBER SUPERCAR"
            self._build_car()
        elif model_type == self.MODEL_GLOBE:
            self.model_name = "PLANET EARTH GLOBE"
            self._build_globe()
        elif model_type == self.MODEL_ARC_REACTOR:
            self.model_name = "IRON MAN ARC REACTOR"
            self._build_arc_reactor()
        elif model_type == self.MODEL_DRONE:
            self.model_name = "CYBER DRONE FIGHTER"
            self._build_drone()
        elif model_type == self.MODEL_TESSERACT:
            self.model_name = "4D TESSERACT HYPERCUBE"
            self._build_tesseract()
        elif model_type == self.MODEL_IMAGE_HOLOGRAM:
            self.model_name = self.hologram_name if self.hologram_name else "CUSTOM HOLOGRAM"

    def set_hologram_image(self, bgra_texture, name="CUSTOM OBJECT"):
        """Sets a dynamic image texture as the active 3D hologram."""
        self.hologram_texture = bgra_texture
        self.hologram_name = name.upper()
        self.model_name = self.hologram_name
        self.current_model = self.MODEL_IMAGE_HOLOGRAM
        self.reset()

    # ================================================================
    # MESH HELPERS
    # ================================================================

    def _add_mesh(self, vertices, faces, edge_mode=True):
        start = len(self.vertices)
        for v in vertices:
            self.vertices.append(list(v))
        for face in faces:
            self.faces.append(tuple(start + i for i in face))
        if edge_mode:
            for face in faces:
                for i in range(len(face)):
                    a = start + face[i]
                    b = start + face[(i + 1) % len(face)]
                    edge = (a, b)
                    rev = (b, a)
                    if edge not in self.edges and rev not in self.edges:
                        self.edges.append(edge)
        return start

    def _add_box(self, center, size, edge_mode=True):
        cx, cy, cz = center
        sx, sy, sz = size
        x, y, z = sx / 2, sy / 2, sz / 2
        verts = [
            (-x + cx, -y + cy, -z + cz),
            ( x + cx, -y + cy, -z + cz),
            ( x + cx,  y + cy, -z + cz),
            (-x + cx,  y + cy, -z + cz),
            (-x + cx, -y + cy,  z + cz),
            ( x + cx, -y + cy,  z + cz),
            ( x + cx,  y + cy,  z + cz),
            (-x + cx,  y + cy,  z + cz)
        ]
        faces = [
            (0, 1, 2, 3), (4, 7, 6, 5),
            (0, 4, 5, 1), (1, 5, 6, 2),
            (2, 6, 7, 3), (3, 7, 4, 0)
        ]
        return self._add_mesh(verts, faces, edge_mode)

    # ================================================================
    # 3D MODEL 1: PROCEDURAL CYBER SUPERCAR
    # ================================================================

    def _build_car(self):
        self._add_body_shell()
        self._add_canopy()
        self._add_side_blades()
        # Wheels
        self._add_wheel(( 1.75, -1.27, -0.72), 0.65, 0.38)
        self._add_wheel(( 1.75,  1.27, -0.72), 0.65, 0.38)
        self._add_wheel((-1.75, -1.27, -0.72), 0.68, 0.44)
        self._add_wheel((-1.75,  1.27, -0.72), 0.68, 0.44)
        # Front Splitter & Diffuser
        self._add_box((2.85, 0.0, -0.58), (0.75, 2.25, 0.08), edge_mode=True)
        self._add_box((-2.85, 0.0, -0.52), (0.75, 2.15, 0.12), edge_mode=True)
        # Rear Wing
        self._add_box((-2.75, 0.0, 0.65), (0.42, 2.30, 0.06), edge_mode=True)
        # Headlights
        start_v = len(self.vertices)
        self.vertices.extend([
            [2.85, -0.92, -0.05], [3.10, -0.68, -0.12],
            [2.85,  0.92, -0.05], [3.10,  0.68, -0.12]
        ])
        self.light_edges.extend([
            (start_v, start_v + 1),
            (start_v + 2, start_v + 3)
        ])

    def _add_body_shell(self):
        sections = [
            ( 3.20, 0.62, -0.28, 0.25, 0.05),
            ( 2.75, 1.05, -0.40, 0.38, 0.12),
            ( 2.10, 1.18, -0.48, 0.50, 0.20),
            ( 1.25, 1.28, -0.52, 0.60, 0.32),
            ( 0.30, 1.32, -0.55, 0.67, 0.40),
            (-0.75, 1.34, -0.55, 0.68, 0.42),
            (-1.65, 1.27, -0.52, 0.60, 0.32),
            (-2.40, 1.12, -0.45, 0.50, 0.20),
            (-3.00, 0.88, -0.32, 0.38, 0.08)
        ]
        verts = []
        for x, w, bottom, shoulder, roof in sections:
            verts.extend([
                (x, -w, bottom), (x, w, bottom),
                (x, -w * 0.96, shoulder), (x, w * 0.96, shoulder),
                (x, -w * 0.68, roof), (x, w * 0.68, roof)
            ])
        faces = []
        for i in range(len(sections) - 1):
            a, b = i * 6, (i + 1) * 6
            faces.append((a + 0, b + 0, b + 2, a + 2))
            faces.append((a + 1, a + 3, b + 3, b + 1))
            faces.append((a + 2, b + 2, b + 4, a + 4))
            faces.append((a + 3, a + 5, b + 5, b + 3))
            faces.append((a + 4, b + 4, b + 5, a + 5))
            faces.append((a + 0, a + 1, b + 1, b + 0))
        start = self._add_mesh(verts, faces, edge_mode=False)
        for f in faces:
            self.body_faces.append(tuple(start + i for i in f))
        for i in range(len(sections) - 1):
            a, b = start + i * 6, start + (i + 1) * 6
            self.edges.extend([
                (a + 0, b + 0), (a + 1, b + 1),
                (a + 2, b + 2), (a + 3, b + 3),
                (a + 4, b + 4), (a + 5, b + 5)
            ])

    def _add_canopy(self):
        verts = [
            ( 1.15, -0.72, 0.42), ( 1.15,  0.72, 0.42),
            ( 0.55, -0.58, 1.10), ( 0.55,  0.58, 1.10),
            (-0.55, -0.52, 1.28), (-0.55,  0.52, 1.28),
            (-1.45, -0.72, 0.72), (-1.45,  0.72, 0.72)
        ]
        faces = [
            (0, 2, 4, 6), (1, 7, 5, 3),
            (2, 3, 5, 4), (4, 5, 7, 6)
        ]
        start = self._add_mesh(verts, faces, edge_mode=False)
        for f in faces:
            self.glass_faces.append(tuple(start + i for i in f))
        glass_edges = [
            (0, 2), (2, 4), (4, 6), (1, 3), (3, 5), (5, 7), (2, 3), (4, 5), (6, 7)
        ]
        self.edges.extend([(start + a, start + b) for a, b in glass_edges])

    def _add_side_blades(self):
        for side in [-1, 1]:
            verts = [
                ( 1.15, side * 1.20, -0.05), ( 0.25, side * 1.34, -0.18),
                (-0.95, side * 1.30, -0.18), (-1.60, side * 1.15,  0.02),
                (-0.55, side * 1.12,  0.15), ( 0.70, side * 1.05,  0.18)
            ]
            faces = [(0, 1, 4, 5), (1, 2, 3, 4)]
            start = self._add_mesh(verts, faces, edge_mode=False)
            for f in faces:
                self.body_faces.append(tuple(start + i for i in f))
            self.edges.extend([
                (start + 0, start + 1), (start + 1, start + 2), (start + 2, start + 3),
                (start + 3, start + 4), (start + 4, start + 5), (start + 5, start + 0)
            ])

    def _add_wheel(self, center, radius, depth, segments=24):
        cx, cy, cz = center
        start = len(self.vertices)
        for i in range(segments):
            angle = 2 * math.pi * i / segments
            x = math.cos(angle) * radius
            z = math.sin(angle) * radius
            self.vertices.append([cx + x, cy - depth / 2, cz + z])
            self.vertices.append([cx + x, cy + depth / 2, cz + z])
        for i in range(segments):
            j = (i + 1) % segments
            a = start + i * 2
            b = start + j * 2
            self.edges.extend([(a, b), (a + 1, b + 1), (a, a + 1)])

    # ================================================================
    # 3D MODEL 2: EARTH / HOLOGRAPHIC GLOBE
    # ================================================================

    def _build_globe(self, radius=2.2, lat_bands=8, lon_bands=12):
        start = len(self.vertices)
        # Latitude rings
        for lat in range(1, lat_bands):
            theta = math.pi * lat / lat_bands
            z = math.cos(theta) * radius
            ring_r = math.sin(theta) * radius
            ring_start = len(self.vertices)
            for lon in range(lon_bands):
                phi = 2 * math.pi * lon / lon_bands
                x = math.cos(phi) * ring_r
                y = math.sin(phi) * ring_r
                self.vertices.append([x, y, z])
            for lon in range(lon_bands):
                next_lon = (lon + 1) % lon_bands
                self.edges.append((ring_start + lon, ring_start + next_lon))

        # Longitude meridian arcs
        for lon in range(lon_bands):
            phi = 2 * math.pi * lon / lon_bands
            meridian_pts = []
            for lat in range(1, lat_bands):
                idx = start + (lat - 1) * lon_bands + lon
                meridian_pts.append(idx)
            for k in range(len(meridian_pts) - 1):
                self.edges.append((meridian_pts[k], meridian_pts[k + 1]))

        # Poles
        north_idx = len(self.vertices)
        self.vertices.append([0.0, 0.0, radius])
        south_idx = len(self.vertices)
        self.vertices.append([0.0, 0.0, -radius])
        for lon in range(lon_bands):
            self.edges.append((north_idx, start + lon))
            self.edges.append((south_idx, start + (lat_bands - 2) * lon_bands + lon))

        # Glowing Equator
        eq_lat = lat_bands // 2
        eq_start = start + (eq_lat - 1) * lon_bands
        for lon in range(lon_bands):
            self.light_edges.append((eq_start + lon, eq_start + ((lon + 1) % lon_bands)))

    # ================================================================
    # 3D MODEL 3: IRON MAN ARC REACTOR
    # ================================================================

    def _build_arc_reactor(self):
        radii = [0.6, 1.2, 1.8, 2.3]
        for r_idx, r in enumerate(radii):
            start = len(self.vertices)
            segs = 24
            for i in range(segs):
                angle = 2 * math.pi * i / segs
                x = math.cos(angle) * r
                y = math.sin(angle) * r
                self.vertices.append([x, y, 0.0])
            for i in range(segs):
                j = (i + 1) % segs
                edge = (start + i, start + j)
                if r_idx in [1, 3]:
                    self.light_edges.append(edge)
                else:
                    self.edges.append(edge)

        # 10 Power coils around ring
        for c in range(10):
            ang = 2 * math.pi * c / 10
            x1 = math.cos(ang) * 1.2
            y1 = math.sin(ang) * 1.2
            x2 = math.cos(ang) * 2.3
            y2 = math.sin(ang) * 2.3
            st = len(self.vertices)
            self.vertices.extend([[x1, y1, -0.2], [x2, y2, -0.2], [x1, y1, 0.2], [x2, y2, 0.2]])
            self.edges.extend([(st, st + 1), (st + 2, st + 3), (st, st + 2), (st + 1, st + 3)])

        # Center energy triangle
        tri_start = len(self.vertices)
        for i in range(3):
            ang = (2 * math.pi * i / 3) + math.pi / 2
            self.vertices.append([math.cos(ang) * 0.55, math.sin(ang) * 0.55, 0.0])
        self.light_edges.extend([
            (tri_start, tri_start + 1),
            (tri_start + 1, tri_start + 2),
            (tri_start + 2, tri_start)
        ])

    # ================================================================
    # 3D MODEL 4: SCI-FI DRONE FIGHTER
    # ================================================================

    def _build_drone(self):
        # Fuselage
        self._add_box((0.0, 0.0, 0.0), (3.0, 1.0, 0.6), edge_mode=True)
        # Cockpit canopy
        canopy_verts = [
            ( 0.8, -0.35, 0.3), ( 0.8,  0.35, 0.3),
            (-0.3, -0.25, 0.7), (-0.3,  0.25, 0.7),
            (-1.0, -0.30, 0.3), (-1.0,  0.30, 0.3)
        ]
        canopy_faces = [(0, 1, 3, 2), (2, 3, 5, 4)]
        st = self._add_mesh(canopy_verts, canopy_faces, edge_mode=True)
        for f in canopy_faces:
            self.glass_faces.append(tuple(st + i for i in f))

        # Quad Rotor Arms
        arm_coords = [
            ( 1.3, -1.8, 0.1), ( 1.3,  1.8, 0.1),
            (-1.3, -1.8, 0.1), (-1.3,  1.8, 0.1)
        ]
        for ax, ay, az in arm_coords:
            # Arm strut
            s = len(self.vertices)
            self.vertices.extend([[ax * 0.3, ay * 0.3, 0.0], [ax, ay, az]])
            self.edges.append((s, s + 1))
            # Rotor ring
            ring_start = len(self.vertices)
            for i in range(16):
                ang = 2 * math.pi * i / 16
                self.vertices.append([ax + math.cos(ang) * 0.55, ay + math.sin(ang) * 0.55, az])
            for i in range(16):
                self.light_edges.append((ring_start + i, ring_start + ((i + 1) % 16)))

    # ================================================================
    # 3D MODEL 5: 4D TESSERACT HYPERCUBE
    # ================================================================

    def _build_tesseract(self):
        # Outer cube (size 2.6)
        s1 = 1.3
        outer_verts = [
            (-s1, -s1, -s1), ( s1, -s1, -s1), ( s1,  s1, -s1), (-s1,  s1, -s1),
            (-s1, -s1,  s1), ( s1, -s1,  s1), ( s1,  s1,  s1), (-s1,  s1,  s1)
        ]
        # Inner cube (size 1.2)
        s2 = 0.65
        inner_verts = [
            (-s2, -s2, -s2), ( s2, -s2, -s2), ( s2,  s2, -s2), (-s2,  s2, -s2),
            (-s2, -s2,  s2), ( s2, -s2,  s2), ( s2,  s2,  s2), (-s2,  s2,  s2)
        ]
        st1 = len(self.vertices)
        for v in outer_verts:
            self.vertices.append(list(v))
        st2 = len(self.vertices)
        for v in inner_verts:
            self.vertices.append(list(v))

        cube_edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]
        # Outer cube edges
        for a, b in cube_edges:
            self.edges.append((st1 + a, st1 + b))
        # Inner cube edges (glowing)
        for a, b in cube_edges:
            self.light_edges.append((st2 + a, st2 + b))
        # Hypercube 4D connecting struts
        for i in range(8):
            self.edges.append((st1 + i, st2 + i))

    # ================================================================
    # TRANSFORMATION METHODS
    # ================================================================

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def rotate(self, rx, ry, rz):
        self.rotation_x += rx
        self.rotation_y += ry
        self.rotation_z += rz

    def zoom(self, amount):
        self.scale += amount
        self.scale = float(np.clip(self.scale, 0.25, 4.0))

    def reset(self):
        self.x = 0.0
        self.y = 0.0
        self.rotation_x = 0.0
        self.rotation_y = 0.0
        self.rotation_z = 0.0
        self.scale = 1.0
        self.visible = True

    def _rotate_points(self, points, rx, ry, rz):
        rx_rad = math.radians(rx)
        ry_rad = math.radians(ry)
        rz_rad = math.radians(rz)
        cx, sx = math.cos(rx_rad), math.sin(rx_rad)
        cy, sy = math.cos(ry_rad), math.sin(ry_rad)
        cz, sz = math.cos(rz_rad), math.sin(rz_rad)
        Rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]], dtype=np.float32)
        Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]], dtype=np.float32)
        Rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]], dtype=np.float32)
        return points @ (Rz @ Ry @ Rx).T

    # ================================================================
    # RENDER PIPELINE
    # ================================================================

    def render(self, frame):
        if not self.visible:
            return frame

        # Render holographic floating particles in background
        frame = self._render_particles(frame)

        # If active model is Dynamic Image Hologram
        if self.current_model == self.MODEL_IMAGE_HOLOGRAM and self.hologram_texture is not None:
            return self._render_image_hologram(frame)

        # Otherwise render procedural 3D Wireframe Object
        return self._render_mesh_object(frame)

    # ================================================================
    # DYNAMIC 3D IMAGE HOLOGRAM RENDERER
    # ================================================================

    def _render_image_hologram(self, frame):
        """
        Projects any image as a true 3D hologram with perspective warp,
        multi-layer parallax depth, glowing cyber bounding box,
        base energy rings, and holographic scanlines.
        """
        h_frame, w_frame = frame.shape[:2]
        hw, hh = 2.4, 2.4

        # 3D corners of the hologram plane
        corners_3d = np.array([
            [-hw, -hh, 0.0],
            [ hw, -hh, 0.0],
            [ hw,  hh, 0.0],
            [-hw,  hh, 0.0]
        ], dtype=np.float32)

        # Rotate and Scale
        front_3d = self._rotate_points(corners_3d * self.scale, self.rotation_x, self.rotation_y, self.rotation_z)
        front_3d[:, 2] += 8.0

        # Project front corners
        front_2d = []
        for x, y, z in front_3d:
            z_safe = max(z, 0.2)
            px = int((x / z_safe) * 780 + w_frame / 2 + self.x)
            py = int((y / z_safe) * 780 + h_frame / 2 + self.y)
            front_2d.append([px, py])
        front_2d = np.float32(front_2d)

        # Back depth layer for 3D parallax depth effect
        back_corners_3d = np.array([
            [-hw, -hh, -0.45],
            [ hw, -hh, -0.45],
            [ hw,  hh, -0.45],
            [-hw,  hh, -0.45]
        ], dtype=np.float32)
        back_3d = self._rotate_points(back_corners_3d * self.scale, self.rotation_x, self.rotation_y, self.rotation_z)
        back_3d[:, 2] += 8.0
        back_2d = []
        for x, y, z in back_3d:
            z_safe = max(z, 0.2)
            px = int((x / z_safe) * 780 + w_frame / 2 + self.x)
            py = int((y / z_safe) * 780 + h_frame / 2 + self.y)
            back_2d.append([px, py])
        back_2d = np.float32(back_2d)

        tex_h, tex_w = self.hologram_texture.shape[:2]
        src_pts = np.float32([[0, 0], [tex_w, 0], [tex_w, tex_h], [0, tex_h]])

        # 1. Warp Back Parallax Layer (subtle deep-blue glow shadow)
        try:
            M_back = cv2.getPerspectiveTransform(src_pts, back_2d)
            warped_back = cv2.warpPerspective(
                self.hologram_texture, M_back, (w_frame, h_frame),
                borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0)
            )
            back_alpha = (warped_back[:, :, 3].astype(np.float32) / 255.0) * 0.28
            back_bgr = warped_back[:, :, :3]
            # Deep blue tint for back shadow
            back_bgr[:, :, 0] = np.clip(back_bgr[:, :, 0] * 1.2, 0, 255)
            back_bgr[:, :, 2] = (back_bgr[:, :, 2] * 0.4).astype(np.uint8)
            for c in range(3):
                frame[:, :, c] = np.clip(
                    frame[:, :, c] * (1.0 - back_alpha) + back_bgr[:, :, c] * back_alpha, 0, 255
                ).astype(np.uint8)
        except Exception:
            pass

        # 2. Warp Front Hologram Layer
        try:
            M_front = cv2.getPerspectiveTransform(src_pts, front_2d)
            warped_front = cv2.warpPerspective(
                self.hologram_texture, M_front, (w_frame, h_frame),
                borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0)
            )
            front_alpha = (warped_front[:, :, 3].astype(np.float32) / 255.0) * 0.85
            front_bgr = warped_front[:, :, :3]

            # Additive glow blend
            for c in range(3):
                frame[:, :, c] = np.clip(
                    frame[:, :, c] * (1.0 - front_alpha * 0.65) + front_bgr[:, :, c] * front_alpha, 0, 255
                ).astype(np.uint8)
        except Exception:
            pass

        # 3. 3D Bounding Box & Cybernetic Corner Brackets
        box_pts_3d = np.array([
            [-hw, -hh, -0.4], [ hw, -hh, -0.4], [ hw,  hh, -0.4], [-hw,  hh, -0.4],
            [-hw, -hh,  0.4], [ hw, -hh,  0.4], [ hw,  hh,  0.4], [-hw,  hh,  0.4]
        ], dtype=np.float32)
        trans_box = self._rotate_points(box_pts_3d * self.scale, self.rotation_x, self.rotation_y, self.rotation_z)
        trans_box[:, 2] += 8.0
        box_2d = []
        for x, y, z in trans_box:
            zs = max(z, 0.2)
            bx = int((x / zs) * 780 + w_frame / 2 + self.x)
            by = int((y / zs) * 780 + h_frame / 2 + self.y)
            box_2d.append((bx, by))

        # Box wireframe lines
        box_edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]
        box_overlay = frame.copy()
        for a, b in box_edges:
            cv2.line(box_overlay, box_2d[a], box_2d[b], (255, 180, 50), 1, cv2.LINE_AA)

        # Corner brackets on front face
        for idx in range(4):
            pt = box_2d[idx + 4]
            cv2.circle(box_overlay, pt, 4, (255, 255, 200), -1, cv2.LINE_AA)

        frame = cv2.addWeighted(box_overlay, 0.35, frame, 0.65, 0)

        # 4. 3D Base Holographic Projector Rings
        base_center_3d = np.array([[0.0, hh * 1.15, 0.0]], dtype=np.float32)
        trans_base = self._rotate_points(base_center_3d * self.scale, self.rotation_x, self.rotation_y, self.rotation_z)
        trans_base[:, 2] += 8.0
        bx = int((trans_base[0, 0] / max(trans_base[0, 2], 0.2)) * 780 + w_frame / 2 + self.x)
        by = int((trans_base[0, 1] / max(trans_base[0, 2], 0.2)) * 780 + h_frame / 2 + self.y)
        ring_r1 = int(140 * self.scale)
        ring_r2 = int(32 * self.scale)
        if ring_r1 > 5 and ring_r2 > 2:
            ring_layer = frame.copy()
            cv2.ellipse(ring_layer, (bx, by), (ring_r1, ring_r2), 0, 0, 360, (255, 200, 30), 2, cv2.LINE_AA)
            cv2.ellipse(ring_layer, (bx, by), (int(ring_r1 * 1.2), int(ring_r2 * 1.2)), 0, 0, 360, (255, 120, 0), 1, cv2.LINE_AA)
            frame = cv2.addWeighted(ring_layer, 0.45, frame, 0.55, 0)

        # 5. Hologram HUD Header above object
        top_pt = box_2d[4]
        tag_text = f"// HOLOGRAM: {self.model_name} [3D PROJECTION ACTIVE]"
        cv2.putText(frame, tag_text, (max(20, top_pt[0] - 160), max(40, top_pt[1] - 15)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.48, (255, 240, 120), 1, cv2.LINE_AA)

        return frame

    # ================================================================
    # 3D WIREFRAME MESH OBJECT RENDERER
    # ================================================================

    def _render_mesh_object(self, frame):
        h_frame, w_frame = frame.shape[:2]
        if not self.vertices:
            return frame

        # Transform all vertices
        pts = np.array(self.vertices, dtype=np.float32) * self.scale
        pts = self._rotate_points(pts, self.rotation_x, self.rotation_y, self.rotation_z)
        pts[:, 2] += 8.0

        # Project vertices
        projected = []
        for x, y, z in pts:
            zs = max(z, 0.2)
            px = int((x / zs) * 780 + w_frame / 2 + self.x)
            py = int((y / zs) * 780 + h_frame / 2 + self.y)
            projected.append((px, py))

        # Depth sort faces
        if self.faces:
            face_depths = []
            for face in self.faces:
                depth = sum(pts[i][2] for i in face) / len(face)
                face_depths.append((depth, face))
            face_depths.sort(reverse=True, key=lambda x: x[0])

            # Semi-transparent body polygons
            body_overlay = frame.copy()
            for _, face in face_depths:
                poly = np.array([projected[i] for i in face], dtype=np.int32)
                cv2.fillPoly(body_overlay, [poly], (190, 75, 15))
            frame = cv2.addWeighted(body_overlay, 0.32, frame, 0.68, 0)

        # Glass faces (if any)
        if self.glass_faces:
            glass_overlay = frame.copy()
            for face in self.glass_faces:
                poly = np.array([projected[i] for i in face], dtype=np.int32)
                cv2.fillPoly(glass_overlay, [poly], (240, 160, 40))
            frame = cv2.addWeighted(glass_overlay, 0.45, frame, 0.55, 0)

        # Structural wireframe edges
        edge_overlay = frame.copy()
        for a, b in self.edges:
            cv2.line(edge_overlay, projected[a], projected[b], (255, 180, 40), 1, cv2.LINE_AA)
        frame = cv2.addWeighted(edge_overlay, 0.75, frame, 0.25, 0)

        # Glowing Neon Light Edges
        if self.light_edges:
            glow = np.zeros_like(frame)
            for a, b in self.light_edges:
                cv2.line(glow, projected[a], projected[b], (255, 255, 160), 6, cv2.LINE_AA)
            glow = cv2.GaussianBlur(glow, (0, 0), 6)
            frame = cv2.addWeighted(frame, 1.0, glow, 0.55, 0)
            for a, b in self.light_edges:
                cv2.line(frame, projected[a], projected[b], (255, 255, 240), 2, cv2.LINE_AA)

        # Base Scanner Ring
        xs = [p[0] for p in projected]
        ys = [p[1] for p in projected]
        if xs and ys:
            cx = int(sum(xs) / len(xs))
            cy = int(sum(ys) / len(ys)) + int(120 * self.scale)
            ring_w = int(180 * self.scale)
            ring_h = int(36 * self.scale)
            if ring_w > 5 and ring_h > 2:
                ring_layer = frame.copy()
                cv2.ellipse(ring_layer, (cx, cy), (ring_w, ring_h), 0, 0, 360, (255, 120, 0), 1, cv2.LINE_AA)
                cv2.ellipse(ring_layer, (cx, cy), (int(ring_w * 1.2), int(ring_h * 1.2)), 0, 0, 360, (255, 70, 0), 1, cv2.LINE_AA)
                frame = cv2.addWeighted(ring_layer, 0.35, frame, 0.65, 0)

        return frame

    # ================================================================
    # FLOATING PARTICLES
    # ================================================================

    def _render_particles(self, frame):
        h_frame, w_frame = frame.shape[:2]
        t = time.time()
        for p in self.particles:
            px3 = p["pos"][0] + math.sin(t * 0.8 + p["phase"]) * 0.25
            py3 = p["pos"][1] + math.cos(t * 0.7 + p["phase"]) * 0.25
            pz3 = p["pos"][2] + 8.0

            zs = max(pz3, 0.2)
            scr_x = int((px3 / zs) * 780 + w_frame / 2 + self.x)
            scr_y = int((py3 / zs) * 780 + h_frame / 2 + self.y)

            if 0 <= scr_x < w_frame and 0 <= scr_y < h_frame:
                alpha = 0.5 + 0.5 * math.sin(t * 2.0 + p["phase"])
                color = (int(255 * alpha), int(190 * alpha), int(60 * alpha))
                cv2.circle(frame, (scr_x, scr_y), p["size"], color, -1, cv2.LINE_AA)
        return frame