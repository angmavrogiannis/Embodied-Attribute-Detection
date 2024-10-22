import math

class ImagePatch:
    """A Python class containing a crop of an image centered around a particular object, as well as relevant information.
    Attributes
    ----------
    cropped_image : array_like
        An array-like of the cropped image taken from the original image.
    left, lower, right, upper : int
        An int describing the position of the (left/lower/right/upper) border of the crop's bounding box in the original image.

    Methods
    -------
    find(object_name: str)->List[ImagePatch]
        Returns a list of new ImagePatch objects containing crops of the image centered around any objects found in the
        image matching the object_name.
    visual_query(question: str=None)->str
        Returns the answer to a basic question asked about the image. If no question is provided, returns the answer to "What is this?".
    language_query(question: str)->str
        References a large language model (e.g., GPT) to produce a response to the given question.
    """

    def __init__(self, image, left: int = None, lower: int = None, right: int = None, upper: int = None):
        """Initializes an ImagePatch object by cropping the image at the given coordinates and stores the coordinates as
        attributes. If no coordinates are provided, the image is left unmodified, and the coordinates are set to the
        dimensions of the image.
        Parameters
        -------
        image : array_like
            An array-like of the original image.
        left, lower, right, upper : int
            An int describing the position of the (left/lower/right/upper) border of the crop's bounding box in the original image.
        """
        if left is None and right is None and upper is None and lower is None:
            self.cropped_image = image
            self.left = 0
            self.lower = 0
            self.right = image.shape[2]  # width
            self.upper = image.shape[1]  # height
        else:
            self.cropped_image = image[:, lower:upper, left:right]
            self.left = left
            self.upper = upper
            self.right = right
            self.lower = lower

        self.width = self.cropped_image.shape[2]
        self.height = self.cropped_image.shape[1]

        self.horizontal_center = (self.left + self.right) / 2
        self.vertical_center = (self.lower + self.upper) / 2

    def find(self, object_name: str) -> List[ImagePatch]:
        """Returns a list of ImagePatch objects matching object_name contained in the crop if any are found.
        Otherwise, returns an empty list.
        Parameters
        ----------
        object_name : str
            the name of the object to be found

        Returns
        -------
        List[ImagePatch]
            a list of ImagePatch objects matching object_name contained in the crop

        Examples
        --------
        >>> # return the foo
        >>> def execute_command(image) -> List[ImagePatch]:
        >>>     image_patch = ImagePatch(image)
        >>>     foo_patches = image_patch.find("foo")
        >>>     return foo_patches
        """
        return find_in_image(self.cropped_image, object_name)

    def visual_query(self, question: str = None) -> str:
        """Returns the answer to a basic question asked about the image. If no question is provided, returns the answer
        to "What is this?". The questions are about basic perception, and are not meant to be used for complex reasoning
        or external knowledge.
        Parameters
        -------
        question : str
            A string describing the question to be asked.

        Examples
        -------

        >>> # Which kind of baz is not fredding?
        >>> def execute_command(image) -> str:
        >>>     image_patch = ImagePatch(image)
        >>>     baz_patches = image_patch.find("baz")
        >>>     for baz_patch in baz_patches:
        >>>         is_fredding = True if baz_patch.visual_query("Is this baz fredding?") == "Yes" else False
        >>>         if not is_fredding:
        >>>             return baz_patch.visual_query("What is this baz?")

        >>> # What color is the foo?
        >>> def execute_command(image) -> str:
        >>>     image_patch = ImagePatch(image)
        >>>     foo_patches = image_patch.find("foo")
        >>>     foo_patch = foo_patches[0]
        >>>     return foo_patch.visual_query("What is the color?")

        >>> # Is the second bar from the left quuxy?
        >>> def execute_command(image) -> str:
        >>>     image_patch = ImagePatch(image)
        >>>     bar_patches = image_patch.find("bar")
        >>>     bar_patches.sort(key=lambda x: x.horizontal_center)
        >>>     bar_patch = bar_patches[1]
        >>>     return bar_patch.visual_query("Is the bar quuxy?")
        """
        return visual_query(self.cropped_image, question)

    def language_query(self, question: str) -> str:
        '''Answers a text question using GPT-3. The input question is always a formatted string with a variable in it.

        Parameters
        ----------
        question: str
            the text question to ask. Must not contain any reference to 'the image' or 'the photo', etc.

        Examples
        --------
        >>> # What is the city this building is in?
        >>> def execute_command(image) -> str:
        >>>     image_patch = ImagePatch(image)
        >>>     building_patches = image_patch.find("building")
        >>>     building_patch = building_patches[0]
        >>>     building_name = building_patch.visual_query("What is the name of the building?")
        >>>     return building_patch.language_query(f"What city is {building_name} in?")

        >>> # Who invented this object?
        >>> def execute_command(image) -> str:
        >>>     image_patch = ImagePatch(image)
        >>>     object_patches = image_patch.find("object")
        >>>     object_patch = object_patches[0]
        >>>     object_name = object_patch.visual_query("What is the name of the object?")
        >>>     return object_patch.language_query(f"Who invented {object_name}?")

        >>> # Explain the history behind this object.
        >>> def execute_command(image) -> str:
        >>>     image_patch = ImagePatch(image)
        >>>     object_patches = image_patch.find("object")
        >>>     object_patch = object_patches[0]
        >>>     object_name = object_patch.visual_query("What is the name of the object?")
        >>>     return object_patch.language_query(f"What is the history behind {object_name}?")
        '''
        return language_query(question, long_answer)

class Robot:
    """
    A Python class describing the actions that a robot can take.
    Attributes
    ----------
    sensors : array_like
        An array-like of the available on-board robot sensors.

    Methods
    -------
    focus_on_patch(object_patch: ImagePatch)
        Uses low-level controls of the robot to adjust the robot's position and orientation to center the camera on the given object patch.
    measure_distance(object_name: str)->float
        Returns the distance between the robot and the object in the geometric center of the image assuming the robot has a distance sensor.
    measure_weight(object_name: str)->float
        Returns the weight of an object assuming that the robot has a force/torque sensor and is already holding the object.
    go_to_coords(object_x_center: int, object_y_center: int)
        Uses low-level controls of the robot to navigate to an object with the given (x_coord, y_coord) image coordinates.
    go_to_object(object_name: str)
        Computes the center coordinates of an image patch and calls go_to_coords to navigate to an object.
    pick_up(object_name: str)
        Uses low-level controls of the robot to pick up an object.
    put_on(receptacle: str)
        Uses low-level controls of the robot to put an object that has picked up on an target receptacle.
    push(object_name: str)
        Uses low-level controls of the robot to push an object forward.
    """
    def __init__(self, sensors: List[str]):
        """Initializes a Robot object that acquires sensing capabilities through the input sensors parameter.
        Parameters
        -------
        sensors : array_like
            An array-like of the available sensors on the robot.

        Examples
        -------
        >>> # The robot is equipped with a camera
        >>> robot = Robot(sensors=["camera"])

        >>> # The robot is equipped with a camera, an IMU, and a distance sensor
        >>> robot = Robot(sensors=["camera, "IMU", "distance sensor"])
        """

    def focus_on_patch(self, object_patch: ImagePatch):
        """Uses low-level controls of the robot to adjust the robot's position and orientation to center the camera on the given object patch.

        Examples
        -------
        >>> # Look at the couch.
        >>> def execute_command(image):
        >>>     image_patch = ImagePatch(image)
        >>>     couch_patch = image_patch.find("couch")
        >>>     couch_patch.focus_on_patch(couch_patch)
        """

    def measure_weight(self, object_name: str) -> float:
        """Only works if the robot has a force/torque sensor.
        Measures the weight of an object after the object has been picked up by the robot.

        Examples
        -------
        >>> # The robot has a camera and a force/torque sensor. How heavy is this book?
        >>> def execute_command(image):
        >>>     robot = Robot(sensors=["camera, "force/torque sensor"])
        >>>     image_patch = ImagePatch(image)
        >>>     book_patch = image_patch.find("book")
        >>>     go_to_object("book")
        >>>     pick_up("book")
        >>>     weight = book_patch.measure_weight("book")
        >>>     return weight["book"]
        """
        return weight[object_name]

    def measure_distance(self, object_name: str) -> float:
        """Only works if the robot has a distance sensor.
        Measures the distance between the robot and the object patch.
        To measure the distance to a patch, the camera must first focus on an object_patch.
        Returns the current reading of the distance sensor which is 
        the distance between the robot and that object.

        Examples
        -------
        >>> # The robot has a camera and a distance sensor. How far is that tv?
        >>> def execute_command(image):
        >>>     robot = Robot(sensors=["camera, "distance sensor"])
        >>>     image_patch = ImagePatch(image)
        >>>     tv_patch = image_patch.find("tv")
        >>>     focus_on_patch(tv_patch)
        >>>     distance = tv_patch.measure_distance("tv")
        >>>     return distance

        >>> # The robot has a camera and a distance sensor. How far is the apple from the desk?
        >>> def execute_command(image):
        >>>     robot = Robot(sensors=["camera, "distance sensor"])
        >>>     image_patch = ImagePatch(image)
        >>>     apple_patch = image_patch.find("apple")
        >>>     desk_patch = image_patch.find("desk")
        >>>     # The robot first has to navigate to the first object and then measure the distance to the second
        >>>     go_to_object(apple_patch)
        >>>     focus_on_patch(desk_patch)
        >>>     distance = apple_patch.measure_distance("desk")
        >>>     return distance
        """
        return measure_distance(object_name)

    def go_to_coords(self, object_x_center: int, object_y_center: int):
        """Auxiliary function that uses low-level controls of the robot 
        to navigate to an object with the given (x_coord, y_coord) image coordinates.

        Examples
        -------
        >>> # Move towards the desk that has center coords: desk_x_center, desk_y_center
        >>> def execute_command(desk_x_center, desk_y_center):
        >>>     go_to_coords(desk_x_center, desk_y_center)
        """

    def go_to_object(self, object_name: str):
        """Computes the center coordinates of an image patch and calls go_to_coords
        to navigate to an object.
        Examples
        -------
        >>> # The robot is equipped with a camera. Approach the red round object
        >>> def execute_command(image):
        >>>     robot = Robot(sensors=["camera"])
        >>>     image_patch = ImagePatch(image)
        >>>     object_patches = image_patch.find("object")
        >>>     for object_patch in object_patches:
        >>>         is_red = True if object_patch.visual_query("Is this object red?") == "Yes" else False
        >>>         if is_red:
        >>>             is_round = True if object_patch.visual_query("Is this object round?") == "Yes" else False
        >>>             if is_round:
        >>>                 go_to_object("object")
        >>>                 break
        """
        object_center_x = (object_patch.left + object_patch.right) / 2
        object_center_y = (object_patch.lower + object_patch.upper) / 2
        go_to_coords(object_center_x, object_center_y)

    def pick_up(object_name: str):
        """Uses low-level controls of the robot to pick up an object.

        Examples
        -------
        >>> # The robot is equipped with a camera. Grab the remote and put it on the green box
        >>> def execute_command(image):
        >>>     robot = Robot(sensors=["camera"])
        >>>     image_patch = ImagePatch(image)
        >>>     remote_patch = image_patch.find("remote")
        >>>     go_to_object(remote_patch)
        >>>     pick_up("remote")
        >>>     box_patches = image_patch.find("box")
        >>>     for box_patch in box_patches:
        >>>         is_green = True if box_patch.visual_query("Is this box green?") == "Yes" else False
        >>>         if is_green:
        >>>             go_to_object("box")
        >>>             put_on("box")
        >>>             break
        """

    def put_on(receptacle: str):
        """Uses low-level controls of the robot to put an object that has
        picked up on another object in the given object_patch.

        Examples
        -------
        >>> # The robot is equipped with a camera. Get the sweet snack and stack it onto the white stand.
        >>> def execute_command(image):
        >>>     robot = Robot(sensors=["camera"])
        >>>     image_patch = ImagePatch(image)
        >>>     snack_patches = image_patch.find("snack")
        >>>     snacks = []
        >>>     for snack_patch in snack_patches:
        >>>         is_sweet = True if snack_patch.visual_query("Is this snack sweet?") == "Yes" else False
        >>>         if is_sweet:
        >>>             go_to_object("snack")
        >>>             pick_up("snack")
        >>>             stand_patch = image_patch.find("stand")
        >>>             is_white = True if stand_patch.visual_query("Is this stand white?") == "Yes" else False
        >>>             if is_white:
        >>>                 go_to_object("stand")
        >>>                 put_on("stand")
        """

Write a function using Python and the Robot and ImagePatch classes (above) that could be executed to perform the given instruction.

Consider the following guidelines:
- Use base Python (comparison, sorting) for basic logical operations, left/right/up/down, math, etc.
- Use the find function to detect objects.
- Initialize the robot class based on the information about the available robot sensors.
- Use the visual_query function for simple visual queries.
- Use the language_query function to access external information.
- Use the robot class functions to deploy the robot and identify attributes that are not visually obvious

Instruction: The robot is equipped with {sensors}. {query}

























































