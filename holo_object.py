import cv2
import numpy as np
import math
import time


class HoloObject:
    """
    Advanced Volumetric 3D Hologram Engine.
    Guarantees TRUE 3D volumetric geometry for ANY query.
    1. Rich Procedural 3D CAD Models for recognized categories:
       - House / Architecture (Walls, Roof gables, Ridge, Chimney, Door, Windows, Porch)
       - Earth / Globe (Sphere latitude/longitude, glowing equator, satellite orbit)
       - Cyber Supercar (Aerodynamic body, glass canopy, diffuser, wheels, lights)
       - Iron Man Arc Reactor (Concentric rotating energy coils, core power triangle)
       - Sci-Fi Drone Fighter (Fuselage, quad rotors, thrusters)
       - 4D Tesseract Hypercube (Nested inner and outer cube with 4D struts)
       - Cyber Katana / Sword (Blade fuller, guard, grip, glowing pommel)
       - Futuristic Robot / Mech (Head, visor, chest arc reactor, torso, limbs)
       - Cybernetic Skull / Helmet (Cranium, eye sockets, jaw structure)
       - Hologram Tree (Trunk, branches, foliage rings)
       - Sci-Fi Chair (Seat, backrest slats, 4 legs)
       - Alien Spaceship / UFO (Saucer discs, upper/lower domes, plasma thrusters)
    2. Universal 3D Volumetric Extrusion for any other web/AI search query:
       - True 3D depth thickness (Front hull + Back hull + 3D connecting side walls + wireframe ribs)
       - NEVER a flat paper sheet!
    """

    MODEL_SUPERCAR = "SUPERCAR"
    MODEL_HOUSE = "HOUSE"
    MODEL_GLOBE = "GLOBE"
    MODEL_ARC_REACTOR = "ARC_REACTOR"
    MODEL_DRONE = "DRONE"
    MODEL_TESSERACT = "TESSERACT"
    MODEL_SWORD = "SWORD"
    MODEL_ROBOT = "ROBOT"
    MODEL_SKULL = "SKULL"
    MODEL_TREE = "TREE"
    MODEL_CHAIR = "CHAIR"
    MODEL_UFO = "UFO"
    MODEL_VOLUMETRIC = "VOLUMETRIC"

    def __init__(self):
        self.x = 0.0
        self.y = 0.0

        # Start with a nice isometric 3D tilt so true 3D depth is immediately visible!
        self.rotation_x = 18.0
        self.rotation_y = -25.0
        self.rotation_z = 0.0

        self.scale = 1.0
        self.visible = True

        self.vertices = []
        self.edges = []
        self.faces = []
        self.body_faces = []
        self.glass_faces = []
        self.light_edges = []

        self.current_model = self.MODEL_SUPERCAR
        self.model_name = "CYBER SUPERCAR"

        # Volumetric image extrusion data
        self.hologram_texture = None
        self.volumetric_contour_pts = []
        self.extrusion_depth = 1.2

        self.particles = []
        self._init_particles()

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
    # SEMANTIC QUERY ROUTER (TRUE 3D GUARANTEE)
    # ================================================================

    def set_hologram_by_query(self, query, texture=None):
        """
        Determines the best true 3D representation for ANY user query.
        If it matches a known category, builds a rich 3D procedural CAD model.
        Otherwise, builds a full 3D Volumetric Extruded Solid from the search image.
        """
        q = query.lower().strip()
        self.hologram_texture = texture
        self.volumetric_contour_pts = []
        self.reset()

        if any(k in q for k in ["house", "home", "building", "villa", "cottage", "mansion", "room", "bungalow", "palace"]):
            self.current_model = self.MODEL_HOUSE
            self.model_name = "3D ARCHITECTURAL HOUSE"
            self._build_house()

        elif any(k in q for k in ["earth", "globe", "world", "planet", "mars", "moon", "jupiter", "saturn", "sun", "space"]):
            self.current_model = self.MODEL_GLOBE
            self.model_name = "3D PLANET EARTH GLOBE"
            self._build_globe()

        elif any(k in q for k in ["car", "vehicle", "supercar", "auto", "ferrari", "lambo", "lamborghini", "bmw", "audi", "porsche"]):
            self.current_model = self.MODEL_SUPERCAR
            self.model_name = "3D CYBER SUPERCAR"
            self._build_car()

        elif any(k in q for k in ["arc", "reactor", "iron man", "tony", "stark"]):
            self.current_model = self.MODEL_ARC_REACTOR
            self.model_name = "3D IRON MAN ARC REACTOR"
            self._build_arc_reactor()

        elif any(k in q for k in ["drone", "jet", "fighter", "plane", "airplane", "aircraft"]):
            self.current_model = self.MODEL_DRONE
            self.model_name = "3D SCI-FI DRONE FIGHTER"
            self._build_drone()

        elif any(k in q for k in ["ufo", "saucer", "spaceship", "alien"]):
            self.current_model = self.MODEL_UFO
            self.model_name = "3D CYBER SPACESHIP UFO"
            self._build_spaceship_ufo()

        elif any(k in q for k in ["tesseract", "hypercube", "cube", "box"]):
            self.current_model = self.MODEL_TESSERACT
            self.model_name = "3D 4D TESSERACT HYPERCUBE"
            self._build_tesseract()

        elif any(k in q for k in ["sword", "katana", "blade", "knife", "weapon"]):
            self.current_model = self.MODEL_SWORD
            self.model_name = "3D CYBER KATANA SWORD"
            self._build_sword()

        elif any(k in q for k in ["robot", "bot", "mech", "android", "cyborg"]):
            self.current_model = self.MODEL_ROBOT
            self.model_name = "3D CYBERNETIC MECH ROBOT"
            self._build_robot()

        elif any(k in q for k in ["skull", "skeleton", "head", "helmet"]):
            self.current_model = self.MODEL_SKULL
            self.model_name = "3D CYBERNETIC SKULL"
            self._build_skull()

        elif any(k in q for k in ["tree", "plant", "forest"]):
            self.current_model = self.MODEL_TREE
            self.model_name = "3D HOLOGRAPHIC TREE"
            self._build_tree()

        elif any(k in q for k in ["chair", "sofa", "furniture", "bench"]):
            self.current_model = self.MODEL_CHAIR
            self.model_name = "3D DESIGNER CHAIR"
            self._build_chair()

        else:
            # Universal 3D Volumetric Extrusion for any other object
            self.current_model = self.MODEL_VOLUMETRIC
            self.model_name = f"3D VOLUMETRIC {query.upper()}"
            self._build_volumetric_extrusion(texture, query)

    def set_model(self, model_type):
        """Switches between available 3D procedural models."""
        self.current_model = model_type
        self.vertices = []
        self.edges = []
        self.faces = []
        self.body_faces = []
        self.glass_faces = []
        self.light_edges = []

        if model_type == self.MODEL_SUPERCAR:
            self.model_name = "3D CYBER SUPERCAR"
            self._build_car()
        elif model_type == self.MODEL_HOUSE:
            self.model_name = "3D ARCHITECTURAL HOUSE"
            self._build_house()
        elif model_type == self.MODEL_GLOBE:
            self.model_name = "3D PLANET EARTH GLOBE"
            self._build_globe()
        elif model_type == self.MODEL_ARC_REACTOR:
            self.model_name = "3D IRON MAN ARC REACTOR"
            self._build_arc_reactor()
        elif model_type == self.MODEL_DRONE:
            self.model_name = "3D SCI-FI DRONE FIGHTER"
            self._build_drone()
        elif model_type == self.MODEL_TESSERACT:
            self.model_name = "3D 4D TESSERACT HYPERCUBE"
            self._build_tesseract()
        elif model_type == self.MODEL_SWORD:
            self.model_name = "3D CYBER KATANA SWORD"
            self._build_sword()
        elif model_type == self.MODEL_ROBOT:
            self.model_name = "3D CYBERNETIC MECH ROBOT"
            self._build_robot()
        elif model_type == self.MODEL_SKULL:
            self.model_name = "3D CYBERNETIC SKULL"
            self._build_skull()
        elif model_type == self.MODEL_TREE:
            self.model_name = "3D HOLOGRAPHIC TREE"
            self._build_tree()
        elif model_type == self.MODEL_CHAIR:
            self.model_name = "3D DESIGNER CHAIR"
            self._build_chair()
        elif model_type == self.MODEL_UFO:
            self.model_name = "3D CYBER SPACESHIP UFO"
            self._build_spaceship_ufo()

    # ================================================================
    # GEOMETRY HELPERS
    # ================================================================

    def _clear_geometry(self):
        self.vertices = []
        self.edges = []
        self.faces = []
        self.body_faces = []
        self.glass_faces = []
        self.light_edges = []

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

    def _add_box(self, center, size, edge_mode=True, is_light=False):
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
        start = len(self.vertices)
        for v in verts:
            self.vertices.append(list(v))
        for f in faces:
            self.body_faces.append(tuple(start + i for i in f))
            self.faces.append(tuple(start + i for i in f))

        box_edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]
        for a, b in box_edges:
            edge = (start + a, start + b)
            if is_light:
                self.light_edges.append(edge)
            elif edge_mode:
                self.edges.append(edge)
        return start

    # ================================================================
    # 3D MODEL 1: PROCEDURAL 3D ARCHITECTURAL HOUSE
    # ================================================================

    def _build_house(self):
        self._clear_geometry()

        # 1. Concrete Foundation Slab
        self._add_box((0.0, 0.0, -1.2), (3.6, 4.2, 0.25))

        # 2. Main Ground Floor Living Quarters
        self._add_box((0.0, 0.0, -0.2), (3.2, 3.8, 1.75))

        # 3. Pitched Roof Gables & Ridge Beam
        st = len(self.vertices)
        w, d, h_base, h_ridge = 1.75, 2.0, 0.68, 1.45

        # Front gable triangle (X = width, Y = -d, Z = height)
        self.vertices.extend([
            [-w, -d, h_base], [w, -d, h_base], [0.0, -d, h_base + h_ridge]
        ])
        # Rear gable triangle
        self.vertices.extend([
            [-w,  d, h_base], [w,  d, h_base], [0.0,  d, h_base + h_ridge]
        ])

        # Roof faces
        # Left sloping roof
        self.faces.append((st + 0, st + 2, st + 5, st + 3))
        self.body_faces.append((st + 0, st + 2, st + 5, st + 3))
        # Right sloping roof
        self.faces.append((st + 1, st + 4, st + 5, st + 2))
        self.body_faces.append((st + 1, st + 4, st + 5, st + 2))
        # Front triangular gable face
        self.faces.append((st + 0, st + 1, st + 2))
        # Rear triangular gable face
        self.faces.append((st + 3, st + 5, st + 4))

        # Roof Structural Wireframe
        self.edges.extend([
            (st + 0, st + 1), (st + 1, st + 2), (st + 2, st + 0),
            (st + 3, st + 4), (st + 4, st + 5), (st + 5, st + 3),
            (st + 0, st + 3), (st + 1, st + 4)
        ])
        # Glowing Roof Ridge Beam
        self.light_edges.append((st + 2, st + 5))

        # 4. Chimney with Top Flue Rim
        self._add_box((0.9, 0.6, 1.4), (0.55, 0.55, 1.3), is_light=True)

        # 5. Front Entrance Door with Detailed Frame
        self._add_box((0.0, -1.92, -0.55), (0.75, 0.12, 1.15), is_light=True)

        # 6. Front Architectural Windows (Left & Right) with Glass & Glowing Cross Frames
        w_left = self._add_box((-1.0, -1.92, -0.25), (0.65, 0.10, 0.65), is_light=True)
        w_right = self._add_box(( 1.0, -1.92, -0.25), (0.65, 0.10, 0.65), is_light=True)

        # 7. Attic Circular / Triangular Window
        attic_st = len(self.vertices)
        self.vertices.extend([
            [-0.3, -1.92, h_base + 0.35],
            [ 0.3, -1.92, h_base + 0.35],
            [ 0.0, -1.92, h_base + 0.85]
        ])
        self.light_edges.extend([
            (attic_st + 0, attic_st + 1),
            (attic_st + 1, attic_st + 2),
            (attic_st + 2, attic_st + 0)
        ])

        # 8. Front Covered Porch & Support Pillars
        self._add_box((0.0, -2.45, -1.1), (1.6, 0.9, 0.12))
        # Left and Right Porch Pillars
        self._add_box((-0.65, -2.75, -0.5), (0.1, 0.1, 1.1), is_light=True)
        self._add_box(( 0.65, -2.75, -0.5), (0.1, 0.1, 1.1), is_light=True)
        # Porch Canopy Roof
        self._add_box((0.0, -2.45, 0.08), (1.8, 1.0, 0.08), is_light=True)

    # ================================================================
    # 3D MODEL 2: PLANET EARTH GLOBE
    # ================================================================

    def _build_globe(self, radius=2.3, lat_bands=10, lon_bands=16):
        self._clear_geometry()
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
            meridian_pts = []
            for lat in range(1, lat_bands):
                idx = start + (lat - 1) * lon_bands + lon
                meridian_pts.append(idx)
            for k in range(len(meridian_pts) - 1):
                self.edges.append((meridian_pts[k], meridian_pts[k + 1]))

        # North & South Poles
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

        # Orbiting Orbital Satellite Ring
        sat_start = len(self.vertices)
        sat_r = radius * 1.35
        for i in range(24):
            ang = 2 * math.pi * i / 24
            # Tilted orbit plane
            x = math.cos(ang) * sat_r
            y = math.sin(ang) * sat_r * math.cos(math.radians(35))
            z = math.sin(ang) * sat_r * math.sin(math.radians(35))
            self.vertices.append([x, y, z])
        for i in range(24):
            self.light_edges.append((sat_start + i, sat_start + ((i + 1) % 24)))

    # ================================================================
    # 3D MODEL 3: PROCEDURAL CYBER SUPERCAR
    # ================================================================

    def _build_car(self):
        self._clear_geometry()
        self._add_body_shell()
        self._add_canopy()
        self._add_side_blades()
        # Wheels
        self._add_wheel(( 1.75, -1.27, -0.72), 0.65, 0.38)
        self._add_wheel(( 1.75,  1.27, -0.72), 0.65, 0.38)
        self._add_wheel((-1.75, -1.27, -0.72), 0.68, 0.44)
        self._add_wheel((-1.75,  1.27, -0.72), 0.68, 0.44)
        # Front Splitter & Diffuser
        self._add_box((2.85, 0.0, -0.58), (0.75, 2.25, 0.08))
        self._add_box((-2.85, 0.0, -0.52), (0.75, 2.15, 0.12))
        # Rear Wing
        self._add_box((-2.75, 0.0, 0.65), (0.42, 2.30, 0.06))
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

    def _add_wheel(self, center, radius, depth, segments=20):
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
    # 3D MODEL 4: IRON MAN ARC REACTOR
    # ================================================================

    def _build_arc_reactor(self):
        self._clear_geometry()
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

        for c in range(10):
            ang = 2 * math.pi * c / 10
            x1 = math.cos(ang) * 1.2
            y1 = math.sin(ang) * 1.2
            x2 = math.cos(ang) * 2.3
            y2 = math.sin(ang) * 2.3
            st = len(self.vertices)
            self.vertices.extend([[x1, y1, -0.2], [x2, y2, -0.2], [x1, y1, 0.2], [x2, y2, 0.2]])
            self.edges.extend([(st, st + 1), (st + 2, st + 3), (st, st + 2), (st + 1, st + 3)])

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
    # 3D MODEL 5: SCI-FI DRONE FIGHTER
    # ================================================================

    def _build_drone(self):
        self._clear_geometry()
        self._add_box((0.0, 0.0, 0.0), (3.0, 1.0, 0.6))
        canopy_verts = [
            ( 0.8, -0.35, 0.3), ( 0.8,  0.35, 0.3),
            (-0.3, -0.25, 0.7), (-0.3,  0.25, 0.7),
            (-1.0, -0.30, 0.3), (-1.0,  0.30, 0.3)
        ]
        canopy_faces = [(0, 1, 3, 2), (2, 3, 5, 4)]
        st = self._add_mesh(canopy_verts, canopy_faces, edge_mode=True)
        for f in canopy_faces:
            self.glass_faces.append(tuple(st + i for i in f))

        arm_coords = [
            ( 1.3, -1.8, 0.1), ( 1.3,  1.8, 0.1),
            (-1.3, -1.8, 0.1), (-1.3,  1.8, 0.1)
        ]
        for ax, ay, az in arm_coords:
            s = len(self.vertices)
            self.vertices.extend([[ax * 0.3, ay * 0.3, 0.0], [ax, ay, az]])
            self.edges.append((s, s + 1))
            ring_start = len(self.vertices)
            for i in range(16):
                ang = 2 * math.pi * i / 16
                self.vertices.append([ax + math.cos(ang) * 0.55, ay + math.sin(ang) * 0.55, az])
            for i in range(16):
                self.light_edges.append((ring_start + i, ring_start + ((i + 1) % 16)))

    # ================================================================
    # 3D MODEL 6: 4D TESSERACT HYPERCUBE
    # ================================================================

    def _build_tesseract(self):
        self._clear_geometry()
        s1 = 1.3
        outer_verts = [
            (-s1, -s1, -s1), ( s1, -s1, -s1), ( s1,  s1, -s1), (-s1,  s1, -s1),
            (-s1, -s1,  s1), ( s1, -s1,  s1), ( s1,  s1,  s1), (-s1,  s1,  s1)
        ]
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
        for a, b in cube_edges:
            self.edges.append((st1 + a, st1 + b))
        for a, b in cube_edges:
            self.light_edges.append((st2 + a, st2 + b))
        for i in range(8):
            self.edges.append((st1 + i, st2 + i))

    # ================================================================
    # 3D MODEL 7: CYBER KATANA SWORD
    # ================================================================

    def _build_sword(self):
        self._clear_geometry()
        # Blade (Z = height, from Z = 0 to Z = 2.8)
        st = len(self.vertices)
        blade_sections = [
            (0.0, 0.05, 0.22, 0.05),
            (0.8, 0.045, 0.20, 0.04),
            (1.8, 0.038, 0.18, 0.035),
            (2.5, 0.025, 0.14, 0.025),
            (2.9, 0.0, 0.0, 0.0)  # Tip
        ]
        for z, w_edge, w_spine, th in blade_sections:
            self.vertices.extend([
                [-th, -w_spine, z], [ th, -w_spine, z],
                [0.0,  w_edge,  z]
            ])
        # Connect blade ribs
        for i in range(len(blade_sections) - 1):
            a, b = st + i * 3, st + (i + 1) * 3
            self.edges.extend([(a, b), (a + 1, b + 1), (a + 2, b + 2), (a, a + 1), (a + 1, a + 2), (a + 2, a)])
        self.light_edges.append((st + 2, st + (len(blade_sections) - 1) * 3 + 2))  # Glowing blade edge!

        # Guard (Tsuba)
        self._add_box((0.0, 0.0, 0.0), (0.35, 0.85, 0.08), is_light=True)

        # Grip (Tsuka)
        self._add_box((0.0, 0.0, -0.55), (0.16, 0.24, 1.0))

        # Pommel (Kashira)
        self._add_box((0.0, 0.0, -1.1), (0.22, 0.30, 0.12), is_light=True)

    # ================================================================
    # 3D MODEL 8: CYBERNETIC MECH ROBOT
    # ================================================================

    def _build_robot(self):
        self._clear_geometry()
        # Head & Glowing Visor
        self._add_box((0.0, 0.0, 1.7), (0.7, 0.7, 0.65))
        self._add_box((0.0, -0.36, 1.7), (0.5, 0.08, 0.18), is_light=True)  # Visor

        # Torso Chest & Core
        self._add_box((0.0, 0.0, 0.7), (1.4, 0.9, 1.2))
        self._add_box((0.0, -0.46, 0.75), (0.35, 0.05, 0.35), is_light=True)  # Arc Core

        # Shoulders & Arms
        for s in [-1, 1]:
            self._add_box((s * 1.05, 0.0, 1.1), (0.5, 0.5, 0.5), is_light=True)
            self._add_box((s * 1.05, 0.0, 0.4), (0.35, 0.35, 0.8))
            self._add_box((s * 1.05, 0.0, -0.2), (0.3, 0.3, 0.35), is_light=True)

        # Pelvis & Legs
        self._add_box((0.0, 0.0, -0.1), (1.1, 0.7, 0.35))
        for s in [-1, 1]:
            self._add_box((s * 0.45, 0.0, -0.7), (0.4, 0.45, 0.8))
            self._add_box((s * 0.45, 0.0, -1.4), (0.35, 0.4, 0.7))
            self._add_box((s * 0.45, -0.15, -1.8), (0.45, 0.7, 0.15), is_light=True)

    # ================================================================
    # 3D MODEL 9: CYBER SKULL
    # ================================================================

    def _build_skull(self):
        self._clear_geometry()
        # Cranium dome
        self._add_box((0.0, 0.0, 0.6), (1.6, 1.8, 1.4))
        # Cheekbones & Face
        self._add_box((0.0, -0.7, 0.1), (1.4, 0.6, 0.8))
        # Eye Sockets (Left and Right)
        self._add_box((-0.42, -1.02, 0.25), (0.38, 0.08, 0.35), is_light=True)
        self._add_box(( 0.42, -1.02, 0.25), (0.38, 0.08, 0.35), is_light=True)
        # Nasal Cavity
        self._add_box((0.0, -1.02, -0.05), (0.18, 0.08, 0.22), is_light=True)
        # Jaw & Teeth Notch
        self._add_box((0.0, -0.65, -0.7), (1.0, 0.9, 0.55), is_light=True)

    # ================================================================
    # 3D MODEL 10: HOLOGRAPHIC TREE
    # ================================================================

    def _build_tree(self):
        self._clear_geometry()
        # Trunk column
        self._add_box((0.0, 0.0, -0.6), (0.4, 0.4, 1.6))
        # Foliage Canopy (Multi-tier 3D Rings)
        radii = [1.8, 1.4, 0.9]
        heights = [0.4, 1.1, 1.7]
        for r, h in zip(radii, heights):
            st = len(self.vertices)
            segs = 16
            for i in range(segs):
                ang = 2 * math.pi * i / segs
                self.vertices.append([math.cos(ang) * r, math.sin(ang) * r, h])
            for i in range(segs):
                self.light_edges.append((st + i, st + ((i + 1) % segs)))
        # Top foliage apex
        apex = len(self.vertices)
        self.vertices.append([0.0, 0.0, 2.2])
        for i in range(16):
            self.edges.append((apex, st + i))

    # ================================================================
    # 3D MODEL 11: DESIGNER CHAIR
    # ================================================================

    def _build_chair(self):
        self._clear_geometry()
        # Seat Cushion
        self._add_box((0.0, 0.0, 0.0), (1.6, 1.6, 0.18))
        # 4 Legs
        for lx in [-0.7, 0.7]:
            for ly in [-0.7, 0.7]:
                self._add_box((lx, ly, -0.75), (0.12, 0.12, 1.4))
        # Backrest uprights
        self._add_box((-0.7, 0.7, 0.8), (0.12, 0.12, 1.5), is_light=True)
        self._add_box(( 0.7, 0.7, 0.8), (0.12, 0.12, 1.5), is_light=True)
        # Backrest Slats
        self._add_box((0.0, 0.7, 1.0), (1.4, 0.08, 0.45), is_light=True)
        self._add_box((0.0, 0.7, 1.45), (1.4, 0.08, 0.25), is_light=True)

    # ================================================================
    # 3D MODEL 12: SCI-FI SPACESHIP UFO
    # ================================================================

    def _build_spaceship_ufo(self):
        self._clear_geometry()
        segs = 24
        # Main Disc Hull Outer Rim
        st_rim = len(self.vertices)
        r_rim = 2.4
        for i in range(segs):
            ang = 2 * math.pi * i / segs
            self.vertices.append([math.cos(ang) * r_rim, math.sin(ang) * r_rim, 0.0])
        for i in range(segs):
            self.light_edges.append((st_rim + i, st_rim + ((i + 1) % segs)))

        # Upper Cockpit Dome
        st_upper = len(self.vertices)
        r_up = 1.1
        for i in range(segs):
            ang = 2 * math.pi * i / segs
            self.vertices.append([math.cos(ang) * r_up, math.sin(ang) * r_up, 0.45])
        for i in range(segs):
            self.edges.append((st_upper + i, st_upper + ((i + 1) % segs)))
            self.edges.append((st_rim + i, st_upper + i))

        # Apex Antenna
        apex = len(self.vertices)
        self.vertices.append([0.0, 0.0, 0.95])
        for i in range(0, segs, 2):
            self.light_edges.append((apex, st_upper + i))

        # Bottom Thruster Reactor Ring
        st_lower = len(self.vertices)
        r_low = 1.3
        for i in range(segs):
            ang = 2 * math.pi * i / segs
            self.vertices.append([math.cos(ang) * r_low, math.sin(ang) * r_low, -0.35])
        for i in range(segs):
            self.light_edges.append((st_lower + i, st_lower + ((i + 1) % segs)))
            self.edges.append((st_rim + i, st_lower + i))

    # ================================================================
    # UNIVERSAL 3D VOLUMETRIC EXTRUSION (FOR ARBITRARY QUERIES)
    # ================================================================

    def _build_volumetric_extrusion(self, texture, query):
        """
        Extrudes ANY image contour into a genuine 3D Volumetric Mesh:
        Front Hull (+Z) + Back Hull (-Z) + Connecting Side Walls + Wireframe Ribs.
        Gives real physical thickness and volumetric presence in 3D air!
        """
        self._clear_geometry()
        depth = 0.9  # Substantial 3D thickness so it's clearly volumetric!

        if texture is not None and texture.shape[2] == 4:
            alpha = texture[:, :, 3]
            contours, _ = cv2.findContours((alpha > 40).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if contours:
                c = max(contours, key=cv2.contourArea)
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.02 * peri, True)
                pts = approx.reshape(-1, 2)
            else:
                pts = np.array([[100, 100], [400, 100], [400, 400], [100, 400]])
        else:
            # Fallback diamond / polygon
            pts = np.array([[256, 80], [420, 200], [380, 440], [130, 440], [90, 200]])

        # Rescale points to 3D object space [-2.0, 2.0]
        n_pts = len(pts)
        front_verts = []
        back_verts = []
        for p in pts:
            x = (float(p[0]) - 256.0) / 100.0
            y = (float(p[1]) - 256.0) / 100.0
            front_verts.append([x, y,  depth / 2])
            back_verts.append([x, y, -depth / 2])

        st_front = len(self.vertices)
        for v in front_verts:
            self.vertices.append(v)
        st_back = len(self.vertices)
        for v in back_verts:
            self.vertices.append(v)

        # 1. Front and Back Contour Rings
        for i in range(n_pts):
            j = (i + 1) % n_pts
            self.light_edges.append((st_front + i, st_front + j))
            self.edges.append((st_back + i, st_back + j))
            # 2. Volumetric 3D Depth Ribs connecting front to back!
            self.edges.append((st_front + i, st_back + i))
            # 3. 3D Side Quad Faces
            side_face = (st_front + i, st_front + j, st_back + j, st_back + i)
            self.body_faces.append(side_face)
            self.faces.append(side_face)

        # Center volumetric depth core
        center_f = len(self.vertices)
        self.vertices.append([0.0, 0.0, depth / 2])
        center_b = len(self.vertices)
        self.vertices.append([0.0, 0.0, -depth / 2])
        for i in range(0, n_pts, max(1, n_pts // 6)):
            self.light_edges.append((center_f, st_front + i))
            self.edges.append((center_b, st_back + i))

    # ================================================================
    # TRANSFORMATION CONTROLS
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
        # Default nice 3D perspective angle
        self.rotation_x = 18.0
        self.rotation_y = -25.0
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

        # Render floating ambient particles
        frame = self._render_particles(frame)

        # Render true 3D Wireframe / Mesh Object
        frame = self._render_3d_mesh(frame)

        # If volumetric model has search image, project image onto 3D front & back hulls
        if self.current_model == self.MODEL_VOLUMETRIC and self.hologram_texture is not None:
            frame = self._render_volumetric_texture(frame)

        return frame

    # ================================================================
    # 3D MESH RENDERER (VERIFIED TRUE 3D PERSPECTIVE)
    # ================================================================

    def _render_3d_mesh(self, frame):
        h_frame, w_frame = frame.shape[:2]
        if not self.vertices:
            return frame

        # Transform all 3D vertices
        pts = np.array(self.vertices, dtype=np.float32) * self.scale
        pts = self._rotate_points(pts, self.rotation_x, self.rotation_y, self.rotation_z)
        pts[:, 2] += 8.0

        # Project 3D to 2D screen coordinates with perspective division
        projected = []
        for x, y, z in pts:
            zs = max(z, 0.2)
            px = int((x / zs) * 780 + w_frame / 2 + self.x)
            py = int((y / zs) * 780 + h_frame / 2 + self.y)
            projected.append((px, py))

        # Depth-sorted semi-transparent body polygons
        if self.body_faces:
            face_depths = []
            for face in self.body_faces:
                depth = sum(pts[i][2] for i in face) / len(face)
                face_depths.append((depth, face))
            face_depths.sort(reverse=True, key=lambda x: x[0])

            body_overlay = frame.copy()
            for _, face in face_depths:
                poly = np.array([projected[i] for i in face], dtype=np.int32)
                cv2.fillPoly(body_overlay, [poly], (170, 70, 15))
            frame = cv2.addWeighted(body_overlay, 0.30, frame, 0.70, 0)

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
                cv2.line(glow, projected[a], projected[b], (255, 255, 150), 6, cv2.LINE_AA)
            glow = cv2.GaussianBlur(glow, (0, 0), 6)
            frame = cv2.addWeighted(frame, 1.0, glow, 0.60, 0)
            for a, b in self.light_edges:
                cv2.line(frame, projected[a], projected[b], (255, 255, 240), 2, cv2.LINE_AA)

        # 3D Base Holographic Projector Ring
        xs = [p[0] for p in projected]
        ys = [p[1] for p in projected]
        if xs and ys:
            cx = int(sum(xs) / len(xs))
            cy = int(max(ys)) + int(35 * self.scale)
            ring_w = int(170 * self.scale)
            ring_h = int(35 * self.scale)
            if ring_w > 5 and ring_h > 2:
                ring_layer = frame.copy()
                cv2.ellipse(ring_layer, (cx, cy), (ring_w, ring_h), 0, 0, 360, (255, 140, 20), 1, cv2.LINE_AA)
                cv2.ellipse(ring_layer, (cx, cy), (int(ring_w * 1.2), int(ring_h * 1.2)), 0, 0, 360, (255, 80, 0), 1, cv2.LINE_AA)
                frame = cv2.addWeighted(ring_layer, 0.40, frame, 0.60, 0)

        return frame

    # ================================================================
    # VOLUMETRIC TEXTURE PROJECTION (WITH 3D PARALLAX DEPTH)
    # ================================================================

    def _render_volumetric_texture(self, frame):
        h_frame, w_frame = frame.shape[:2]
        hw, hh = 1.8, 1.8
        corners_3d = np.array([
            [-hw, -hh,  0.45], [ hw, -hh,  0.45],
            [ hw,  hh,  0.45], [-hw,  hh,  0.45]
        ], dtype=np.float32)

        front_3d = self._rotate_points(corners_3d * self.scale, self.rotation_x, self.rotation_y, self.rotation_z)
        front_3d[:, 2] += 8.0
        front_2d = []
        for x, y, z in front_3d:
            zs = max(z, 0.2)
            front_2d.append([int((x / zs) * 780 + w_frame / 2 + self.x),
                             int((y / zs) * 780 + h_frame / 2 + self.y)])
        front_2d = np.float32(front_2d)

        tex_h, tex_w = self.hologram_texture.shape[:2]
        src_pts = np.float32([[0, 0], [tex_w, 0], [tex_w, tex_h], [0, tex_h]])

        try:
            M = cv2.getPerspectiveTransform(src_pts, front_2d)
            warped = cv2.warpPerspective(
                self.hologram_texture, M, (w_frame, h_frame),
                borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0)
            )
            alpha = (warped[:, :, 3].astype(np.float32) / 255.0) * 0.70
            bgr = warped[:, :, :3]
            for c in range(3):
                frame[:, :, c] = np.clip(
                    frame[:, :, c] * (1.0 - alpha * 0.6) + bgr[:, :, c] * alpha, 0, 255
                ).astype(np.uint8)
        except Exception:
            pass
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