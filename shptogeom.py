import math
from euclid import *
import shapefile

from seidel import Triangulator


class _MetaObj:
        
        def __init__(self, v3Origin, lstPoints):
                self.origin = v3Origin
                self.points = lstPoints



class ShapeToGeom:
        
        _FIPS = 0
        _ISO2 = 1
        _ISO3 = 2
        _UN = 3
        _NAME = 4
        _AREA = 5
        _POP = 7
        
        _LON = 9
        _LAT = 10
        
        def __init__(self, pathToShpRec, pathToShp):
                
                self._sf = shapefile.Reader(pathToShpRec)
                self._sf2 = shapefile.Reader(pathToShp)
                self._shpRecs = self._sf.shapeRecords()

                shps = self._sf2.shapes()
                shps.reverse()
                print(self._sf2.bbox)
                self._lstBorders = []
                #print(len(list(self._itShpRecs)))
                
                #for shp, rec in self._itShpRecs:
                for idx, sr in enumerate(self._shpRecs):
                        #shp = self._sf.shape(0)
                        #rec = self._sf.record(0)
                        # indent
                        shp = shps[idx]
                        rec = sr.record

                        lat = rec[ShapeToGeom._LAT]
                        lon = rec[ShapeToGeom._LON]
                        origin = ShapeToGeom._sphToEuc(lat, lon)

                        lstPoints = ShapeToGeom._shapeToPoints(shp, origin)
                        self._lstBorders.append(lstPoints)

                        #print(lstPoints)

        def Borders(self):
            return self._lstBorders



                
        
        # to unit sphere
        @staticmethod
        def _sphToEuc(degLat, degLon):
                degLat = math.radians(degLat);
                degLon = math.radians(degLon);
                x = math.cos(degLat) * math.sin(degLon)
                y = math.sin(degLat)
                z = math.cos(degLat) * math.cos(degLon)
                point = Vector3(x, y, z)
                return point
                
        
        # bounding box center of weight
        @staticmethod
        def _bboxCenter(bbox):
                point = Vector2((bbox[2] - bbox[0]) * 0.5 + bbox[0],
                                (bbox[3] - bbox[1]) * 0.5 + bbox[1])
                return point
                
        
        @staticmethod
        def _shapeToPoints(shape, v3Dest):

                lstPoints = []

                target = v3Dest.normalized()
                normal = Vector3(0, 1, 0)
                rotAxis = normal.cross(target)
                angle = math.acos(target.dot(normal))



                t = Matrix4()
                t.translate(target.x, target.y, target.z)
                t.rotate_axis(angle, rotAxis)
                t.scale(1.0/180.0, 1, -1.0/90.0)


                massCenter = ShapeToGeom._bboxCenter(shape.bbox)

                for point in shape.points:
                        #v = Vector2(point[0], point[1])
                        #v = v - massCenter
                        #v3d = Vector3(v.x, 0, v.y)
                        #v3d = t.transform(v3d)
                        v3d = ShapeToGeom._sphToEuc(point[1], point[0])
                        lstPoints.append(v3d)

                #lstPoints.reverse()
                return lstPoints

                        
