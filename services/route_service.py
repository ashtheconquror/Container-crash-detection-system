import math
from typing import List, Dict

class RouteService:
    """
    Handles coordinate interpolation and route geometry.
    Uses strategic transit hubs to avoid landmasses for major international routes.
    """

    # Strategic Maritime Choke Points
    HUBS = {
        "SUEZ": {"lat": 29.97, "lng": 32.53, "name": "Suez Canal"},
        "PANAMA": {"lat": 9.08, "lng": -79.69, "name": "Panama Canal"},
        "MALACCA": {"lat": 2.22, "lng": 102.16, "name": "Strait of Malacca"},
        "GIBRALTAR": {"lat": 35.95, "lng": -5.31, "name": "Strait of Gibraltar"},
        "BAB_EL_MANDEB": {"lat": 12.58, "lng": 43.34, "name": "Bab el-Mandeb"},
        "CAPE_GOOD_HOPE": {"lat": -34.35, "lng": 18.47, "name": "Cape of Good Hope"},
        "CAPE_HORN": {"lat": -55.98, "lng": -67.27, "name": "Cape Horn"}
    }

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """Haversine formula to calculate distance in km."""
        R = 6371
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * \
            math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    def get_intermediate_points(self, start: Dict, end: Dict, num_points: int) -> List[Dict]:
        """Interpolates points on a single Great Circle segment."""
        lat1 = math.radians(start["lat"])
        lon1 = math.radians(start["lng"])
        lat2 = math.radians(end["lat"])
        lon2 = math.radians(end["lng"])

        # Handle crossing the International Date Line
        dlon = lon2 - lon1
        if dlon > math.pi:
            lon2 -= 2 * math.pi
        elif dlon < -math.pi:
            lon2 += 2 * math.pi
        
        d = 2 * math.asin(math.sqrt(math.sin((lat1 - lat2) / 2)**2 +
                                    math.cos(lat1) * math.cos(lat2) * math.sin((lon1 - lon2) / 2)**2))

        segment_points = []
        for i in range(num_points):
            f = i / (num_points - 1)
            if d == 0:
                segment_points.append({"lat": start["lat"], "lng": start["lng"]})
                continue

            a = math.sin((1 - f) * d) / math.sin(d)
            b = math.sin(f * d) / math.sin(d)
            
            x = a * math.cos(lat1) * math.cos(lon1) + b * math.cos(lat2) * math.cos(lon2)
            y = a * math.cos(lat1) * math.sin(lon1) + b * math.cos(lat2) * math.sin(lon2)
            z = a * math.sin(lat1) + b * math.sin(lat2)
            
            res_lat = math.atan2(z, math.sqrt(x**2 + y**2))
            res_lon = math.atan2(y, x)
            
            # Normalize longitude back to -180 to 180
            deg_lon = math.degrees(res_lon)
            if deg_lon > 180: deg_lon -= 360
            if deg_lon < -180: deg_lon += 360
            
            segment_points.append({
                "lat": math.degrees(res_lat),
                "lng": deg_lon,
                "name": start.get("name", "In Transit")
            })
        return segment_points

    def get_route_waypoints(self, start: Dict, end: Dict, num_points: int = 100) -> List[Dict]:
        """
        Determines the best path using hubs and generates combined waypoints.
        """
        path = [start]
        
        s_lng = start["lng"]
        e_lng = end["lng"]
        s_lat = start["lat"]
        e_lat = end["lat"]

        # Logic for major maritime transitions
        
        # 1. Europe/Atlantic to Indian/Far East (via Suez)
        is_europe_atlantic = (s_lng < 20 or s_lng > 340 or -100 < s_lng < 0)
        is_asia_india = (40 < e_lng < 150)
        
        if (is_europe_atlantic and is_asia_india) or (is_asia_india and is_europe_atlantic):
            # Check if one is North and one is East
            path.append(self.HUBS["GIBRALTAR"])
            path.append(self.HUBS["SUEZ"])
            path.append(self.HUBS["BAB_EL_MANDEB"])
            if e_lng > 90 or s_lng > 90: # Far East
                path.append(self.HUBS["MALACCA"])

        # 2. US East to US West/Pacific (via Panama)
        is_us_east_coast = -90 < s_lng < -60 and s_lat > 20
        is_pacific_coast = e_lng < -110 or e_lng > 110
        if (is_us_east_coast and is_pacific_coast) or (is_pacific_coast and is_us_east_coast):
            path.append(self.HUBS["PANAMA"])

        path.append(end)
        
        # Generate final interpolated waypoints
        all_waypoints = []
        # Ensure we have enough points for the curve
        target_total = max(num_points, len(path) * 20)
        points_per_segment = target_total // (len(path) - 1)
        
        for i in range(len(path) - 1):
            segment = self.get_intermediate_points(path[i], path[i+1], points_per_segment)
            if i > 0:
                all_waypoints.extend(segment[1:])
            else:
                all_waypoints.extend(segment)
                
        return all_waypoints

route_service = RouteService()
