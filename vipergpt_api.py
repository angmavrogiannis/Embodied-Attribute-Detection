import math

class Robot:
	"""
	A Python class describing the actions that a robot can make.
	"""
	def go_to(object_name: str):
		"""Move towards an object and stop once you are close to it."""

	def move_forward(distance: float):
		"""Move forward for a given distance"""

	def move_backwards(distance: float):
		"""Move backwards for a given distance"""

	def move_right(distance: float):
		"""Move right for a given distance"""

	def move_left(distance: float):
		"""Move left for a given distance"""

	def rotate(angle: float):
		"""Rotate counter-clockwise by the amount of radians given as input."""

	def stop():
		"""Stop in place and await for further instructions."""

	def look_around():
		"""Look around in case you cannot find an object."""

	def debug():
		"""objects"""

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
    exists(object_name: str)->bool
        Returns True if the object specified by object_name is found in the image, and False otherwise.
    verify_property(property: str)->bool
        Returns True if the property is met, and False otherwise.
    simple_query(question: str=None)->str
        Returns the answer to a basic question asked about the image. If no question is provided, returns the answer to "What is this?".
    llm_query(question: str, long_answer: bool)->str
        References a large language model (e.g., GPT) to produce a response to the given question. Default is short-form answers, can be made long-form responses with the long_answer flag.
    compute_depth()->float
        Returns the median depth of the image crop.
    crop(left: int, lower: int, right: int, upper: int)->ImagePatch
        Returns a new ImagePatch object containing a crop of the image at the given coordinates.
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

    def exists(self, object_name: str) -> bool:
        """Returns True if the object specified by object_name is found in the image, and False otherwise.
        Parameters
        -------
        object_name : str
            A string describing the name of the object to be found in the image.

        Examples
        -------
        >>> # Are there both foos and garply bars in the photo?
        >>> def execute_command(image)->str:
        >>>     image_patch = ImagePatch(image)
        >>>     is_foo = image_patch.exists("foo")
        >>>     is_garply_bar = image_patch.exists("garply bar")
        >>>     return bool_to_yesno(is_foo and is_garply_bar)
        """
        return len(self.find(object_name)) > 0

    def verify_property(self, object_name: str, visual_property: str) -> bool:
        """Returns True if the object possesses the visual property, and False otherwise.
        Differs from 'exists' in that it presupposes the existence of the object specified by object_name, instead checking whether the object possesses the property.
        Parameters
        -------
        object_name : str
            A string describing the name of the object to be found in the image.
        visual_property : str
            A string describing the simple visual property (e.g., color, shape, material) to be checked.

        Examples
        -------
        >>> # Do the letters have blue color?
        >>> def execute_command(image) -> str:
        >>>     image_patch = ImagePatch(image)
        >>>     letters_patches = image_patch.find("letters")
        >>>     # Question assumes only one letter patch
        >>>     return bool_to_yesno(letters_patches[0].verify_property("letters", "blue"))
        """
        return verify_property(self.cropped_image, object_name, property)

    def simple_query(self, question: str = None) -> str:
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
        >>>         if not baz_patch.verify_property("baz", "fredding"):
        >>>             return baz_patch.simple_query("What is this baz?")

        >>> # What color is the foo?
        >>> def execute_command(image) -> str:
        >>>     image_patch = ImagePatch(image)
        >>>     foo_patches = image_patch.find("foo")
        >>>     foo_patch = foo_patches[0]
        >>>     return foo_patch.simple_query("What is the color?")

        >>> # Is the second bar from the left quuxy?
        >>> def execute_command(image) -> str:
        >>>     image_patch = ImagePatch(image)
        >>>     bar_patches = image_patch.find("bar")
        >>>     bar_patches.sort(key=lambda x: x.horizontal_center)
        >>>     bar_patch = bar_patches[1]
        >>>     return bar_patch.simple_query("Is the bar quuxy?")
        """
        return simple_query(self.cropped_image, question)

    def compute_depth(self):
        """Returns the median depth of the image crop
        Parameters
        ----------
        Returns
        -------
        float
            the median depth of the image crop

        Examples
        --------
        >>> # the bar furthest away
        >>> def execute_command(image)->ImagePatch:
        >>>     image_patch = ImagePatch(image)
        >>>     bar_patches = image_patch.find("bar")
        >>>     bar_patches.sort(key=lambda bar: bar.compute_depth())
        >>>     return bar_patches[-1]
        """
        depth_map = compute_depth(self.cropped_image)
        return depth_map.median()

    def crop(self, left: int, lower: int, right: int, upper: int) -> ImagePatch:
        """Returns a new ImagePatch cropped from the current ImagePatch.
        Parameters
        -------
        left, lower, right, upper : int
            The (left/lower/right/upper)most pixel of the cropped image.
        -------
        """
        return ImagePatch(self.cropped_image, left, lower, right, upper)

    def llm_query(self, question: str, long_answer: bool = True) -> str:
        '''Answers a text question using GPT-3. The input question is always a formatted string with a variable in it.

        Parameters
        ----------
        question: str
            the text question to ask. Must not contain any reference to 'the image' or 'the photo', etc.
        long_answer: bool
            whether to return a short answer or a long answer. Short answers are one or at most two words, very concise.
            Long answers are longer, and may be paragraphs and explanations. Defalt is True (so long answer).

        Examples
        --------
        >>> # What is the city this building is in?
        >>> def execute_command(image) -> str:
        >>>     image_patch = ImagePatch(image)
        >>>     building_patches = image_patch.find("building")
        >>>     building_patch = building_patches[0]
        >>>     building_name = building_patch.simple_query("What is the name of the building?")
        >>>     return building_patch.llm_query(f"What city is {building_name} in?", long_answer=False)

        >>> # Who invented this object?
        >>> def execute_command(image) -> str:
        >>>     image_patch = ImagePatch(image)
        >>>     object_patches = image_patch.find("object")
        >>>     object_patch = object_patches[0]
        >>>     object_name = object_patch.simple_query("What is the name of the object?")
        >>>     return object_patch.llm_query(f"Who invented {object_name}?", long_answer=False)

        >>> # Explain the history behind this object.
        >>> def execute_command(image) -> str:
        >>>     image_patch = ImagePatch(image)
        >>>     object_patches = image_patch.find("object")
        >>>     object_patch = object_patches[0]
        >>>     object_name = object_patch.simple_query("What is the name of the object?")
        >>>     return object_patch.llm_query(f"What is the history behind {object_name}?", long_answer=True)
        '''
        return llm_query(question, long_answer)

def distance(patch_a: ImagePatch, patch_b: ImagePatch) -> float:
    """
    Returns the distance between the edges of two ImagePatches. If the patches overlap, it returns a negative distance
    corresponding to the negative intersection over union.

    Parameters
    ----------
    patch_a : ImagePatch
    patch_b : ImagePatch

    Examples
    --------
    # Return the qux that is closest to the foo
    >>> def execute_command(image):
    >>>     image_patch = ImagePatch(image)
    >>>     qux_patches = image_patch.find('qux')
    >>>     foo_patches = image_patch.find('foo')
    >>>     foo_patch = foo_patches[0]
    >>>     qux_patches.sort(key=lambda x: distance(x, foo_patch))
    >>>     return qux_patches[0]
    """
    return distance(patch_a, patch_b)


def bool_to_yesno(bool_answer: bool) -> str:
    return "yes" if bool_answer else "no"


def coerce_to_numeric(string):
    """
    This function takes a string as input and returns a float after removing any non-numeric characters.
    If the input string contains a range (e.g. "10-15"), it returns the first value in the range.
    """
    return coerce_to_numeric(string)

Write a function using Python and the Robot and ImagePatch classes (above) that could be executed to perform the given instruction.

Consider the following guidelines:
- Use base Python (comparison, sorting) for basic logical operations, left/right/up/down, math, etc.
- Use the llm_query function to access external information and answer informational questions not concerning the image.

Instruction: Tread towards the small door.