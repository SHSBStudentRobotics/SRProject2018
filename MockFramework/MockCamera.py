import time, os, json, math

#A Mock Mamera object that reads in a json file made by JSONCameraTool
#When see() is called it returns the camera data , iterating through each
#image for each successive call of see(). Also replicates the delay caused 
# by image processing.

class MockCameraJSONReader():
    def __init__(self, filename):
        self.importCameraData(filename)
        self.imageCounter = 0
        self.CAMERADELAY = 0.2

    #Filename is relative to the MockFramework directory.
    def importCameraData(self, filename):
        #try:
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),filename)) as file:
            self.cameraData = json.load(file)
        #except:
        #    print("Error loading JSON file: " + str(filename))
        #    print("Proceeding without camera data")

    def see(self):
        self.imageCounter += 1
        time.sleep(self.CAMERADELAY)
        return self.seeImage(self.imageCounter -1)

    #Returns a particular image, rather than iterating through them, for consistent testing
    #In the unit testing framework.
    def seeImage(self, imageID):

        return list(map(lambda x: Marker(x["_raw_data"]), self.cameraData[imageID % len(self.cameraData)]))


#Previously code shamelessly stolen from www.github.com/sourcebots/robot-api

class CartCoord:
    """Represents a cartesian co-ordinate point."""

    def __init__(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z

    @property
    def x(self):
        """X co-ordinate of the cartesian position."""
        return self._x

    @property
    def y(self):
        """Y co-ordinate of the cartesian position."""
        return self._y

    @property
    def z(self):
        """Z co-ordinate of the cartesian position."""
        return self._z


class PolarCoord:
    """
    Represents a point expressed in polar co-ordinates.
    Strictly the space are spherical co-ordinates.
    """

    def __init__(self, rot, dist_m):
        self._rot_x_rad = rot[0]
        self._rot_y_rad = rot[1]
        self._distance_metres = dist_m

    # TODO add tests for all these
    @property
    def rot_x_rad(self):
        """
        Rotation of marker relative to camera in the #TODO axis.
        """
        return self._rot_x_rad

    @property
    def rot_y_rad(self):
        """
        Rotation of marker relative to camera in the #TODO axis.
        """
        return self._rot_y_rad

    @property
    def rot_x_deg(self):
        """
        Rotation of marker relative to camera in the #TODO axis.
        """
        # TODO describe which axis this is
        return math.degrees(self._rot_x_rad)

    @property
    def rot_y_deg(self):
        """
        Rotation of marker relative to camera in the #TODO axis.
        """
        # TODO describe which axis this is
        return math.degrees(self._rot_y_rad)

    @property
    def distance_metres(self):
        """Distance of marker from camera in metres."""
        # TODO describe which axis this is
        return self._distance_metres


class Marker:
    """A marker captured from a webcam image."""

    def __init__(self, data):
        self._raw_data = data

        # Go through all the data, add an _ at the start.
        data = {"_" + k: v for k, v in data.items()}

        self.__dict__.update(data)

    @property
    def id(self):
        """ID of the marker seen."""
        return self._id

    @property
    def size(self):
        """Marker size in metres."""
        return tuple(self._size)

    # Disabled because it's always 0.0
    # TODO fix the certainty being 0
    # @property
    # def certainty(self):
    #     return self._certainty

    @property
    def pixel_corners(self):
        """Pixel co-ordinates of the of the corners of the marker."""
        # TODO define what the order of these corners are
        return [tuple(x) for x in self._pixel_corners]

    @property
    def pixel_centre(self):
        """Pixel co-ordinates of the centre of the marker."""
        return tuple(self._pixel_centre)

    @property
    def distance_metres(self):
        """Distance of the marker from the camera in metres."""
        return self.polar.distance_metres

    # Helper functions, Might need to vary these per-game

    def is_wall_marker(self):
        """If the marker is a wall marker."""
        return self.id in WALL

    def is_token_marker(self):
        """If the marker is a token marker."""
        return self.id in TOKEN

    @property
    def polar(self):
        """
        The position of the marker in the polar co-ordinates.
        Strictly these are spherical co-ordinates. The camera's position is the
        origin of the co-ordinate space.
        """
        return PolarCoord((self._polar[0], self._polar[1]), self._polar[2])

    @property
    def cartesian(self):
        """
        The position of the marker in Cartesian co-ordinates.
        The camera's position is the origin of the co-ordinate space.
        """
        raise NotImplementedError("This is not implemented.")
        return CartCoord()


