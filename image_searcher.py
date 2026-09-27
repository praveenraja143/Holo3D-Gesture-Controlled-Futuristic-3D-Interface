import os
import re
import urllib.parse
import threading
import requests
import cv2
import numpy as np


class ImageSearcher:
    """
    Asynchronous web image fetcher and holographic texture generator.
    Fetches transparent PNGs or clean images for any object query,
    cleans background if needed, and applies futuristic holographic styling.
    """

    def __init__(self, cache_dir="hologram_cache"):
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)
        self.is_fetching = False
        self.last_query = ""
        self.last_error = ""

    def search_and_process_async(self, query, callback):
        """
        Runs search and processing in a background thread so the camera feed never stutters.
        Calls callback(hologram_rgba, query) when complete.
        """
        thread = threading.Thread(
            target=self._worker,
            args=(query, callback),
            daemon=True
        )
        thread.start()

    def _worker(self, query, callback):
        self.is_fetching = True
        self.last_query = query
        self.last_error = ""
        try:
            img = self.fetch_image(query)
            if img is not None:
                holo_img = self.create_holographic_texture(img)
                callback(holo_img, query)
            else:
                self.last_error = "No image found"
                callback(None, query)
        except Exception as e:
            self.last_error = str(e)
            callback(None, query)
        finally:
            self.is_fetching = False

    def fetch_image(self, query):
        """
        Searches web for query + transparent / cutout image.
        Tries multiple queries and search backends.
        """
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            )
        }

        search_variations = [
            f"{query} transparent png",
            f"{query} cutout isolated",
            f"{query} 3d render transparent",
            query
        ]

        found_urls = []
        for q in search_variations:
            try:
                # Bing image search
                url = f"https://www.bing.com/images/search?q={urllib.parse.quote(q)}&first=1"
                r = requests.get(url, headers=headers, timeout=6)
                matches = re.findall(r'murl&quot;:&quot;(http[^&]+)&quot;', r.text)
                if matches:
                    found_urls.extend(matches[:6])
                    break
            except Exception:
                continue

        # Try downloading images from results
        for img_url in found_urls:
            try:
                resp = requests.get(img_url, headers=headers, timeout=6)
                if resp.status_code == 200 and len(resp.content) > 5000:
                    arr = np.asarray(bytearray(resp.content), dtype=np.uint8)
                    # Try reading with alpha channel first
                    img = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)
                    if img is not None and img.shape[0] > 100 and img.shape[1] > 100:
                        return img
            except Exception:
                continue

        return None

    def create_holographic_texture(self, img, target_size=(512, 512)):
        """
        Converts any image into an ultra-futuristic holographic texture
        with alpha transparency, cyan/neon edge glow, and hologram scanlines.
        Returns BGRA image (shape: target_size x 4).
        """
        # Resize preserving aspect ratio into target_size square canvas
        h, w = img.shape[:2]
        scale = min(target_size[0] / h, target_size[1] / w)
        new_w, new_h = max(1, int(w * scale)), max(1, int(h * scale))
        resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

        # Create canvas with 4 channels (BGRA)
        canvas = np.zeros((target_size[0], target_size[1], 4), dtype=np.uint8)
        y_off = (target_size[0] - new_h) // 2
        x_off = (target_size[1] - new_w) // 2

        if resized.shape[2] == 4:
            # Already has alpha
            alpha = resized[:, :, 3]
            bgr = resized[:, :, :3]
        else:
            bgr = resized
            # Detect background: if background is pure white or very dark, create smart mask
            gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
            # Edge-based mask with floodFill from corners
            mask = np.zeros((new_h + 2, new_w + 2), np.uint8)
            corners = [(0, 0), (new_w - 1, 0), (0, new_h - 1), (new_w - 1, new_h - 1)]
            
            # Check corner colors to see if background is white or black
            corner_pixels = [gray[0, 0], gray[0, -1], gray[-1, 0], gray[-1, -1]]
            avg_corner = float(np.mean(corner_pixels))
            
            if avg_corner > 220:
                # White background removal
                _, thresh = cv2.threshold(gray, 235, 255, cv2.THRESH_BINARY_INV)
                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
                alpha = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            elif avg_corner < 35:
                # Black background removal
                _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
                alpha = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            else:
                # Center circular/soft fade mask
                alpha = np.full((new_h, new_w), 240, dtype=np.uint8)
                # Soft vignette edges
                cv2.rectangle(alpha, (0, 0), (new_w - 1, new_h - 1), 0, 15)
                alpha = cv2.GaussianBlur(alpha, (21, 21), 0)

        # Holographic tint: blend image colors with futuristic cyan/neon blue
        holo_bgr = bgr.copy().astype(np.float32)
        # Boost blue and cyan
        holo_bgr[:, :, 0] = np.clip(holo_bgr[:, :, 0] * 0.7 + 160, 0, 255)
        holo_bgr[:, :, 1] = np.clip(holo_bgr[:, :, 1] * 0.8 + 110, 0, 255)
        holo_bgr[:, :, 2] = np.clip(holo_bgr[:, :, 2] * 0.6 + 40, 0, 255)
        holo_bgr = holo_bgr.astype(np.uint8)

        # Edge glow detection
        edges = cv2.Canny(bgr, 60, 160)
        edges_dilated = cv2.dilate(edges, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
        glow_mask = (edges_dilated > 0)
        holo_bgr[glow_mask] = [255, 250, 180]  # Glowing bright cyan-white edges

        # Hologram scanlines effect
        scanline_pattern = np.ones((new_h, 1), dtype=np.float32)
        scanline_pattern[::3] = 0.55
        holo_bgr = (holo_bgr * scanline_pattern[:, :, None]).astype(np.uint8)

        canvas[y_off:y_off + new_h, x_off:x_off + new_w, :3] = holo_bgr
        canvas[y_off:y_off + new_h, x_off:x_off + new_w, 3] = alpha

        return canvas
