
def find(object_name: str) -> list(ImagePatch):
      """
      Calls the GLIP model and returns a list of image patches 
      containing crops of the image centered around any objects
      found in the image matching the object_name. 
      """

def verify_property(property: str) -> bool:
      """
      Calls the X-VLM model and returns True if the property is met,
      and False otherwise.
      """

def simple_visual_query(question: str) -> str:
      """
      Calls the BLIP-2 model and returns the answer to a basic question
      asked about the image. If no question is provided, returns 
      the answer to "What is this?
      """

def llm_query(question: str) -> str:
      """
      Answers a textual question by calling an LLM (GPT).
      """

def move_forward(distance, speed)

def move_backwards(distance, speed)

def move_left(distance, speed)

def move_right(distance, speed)

def rotate(angle, speed)

def move_arm_forward(distance)

def move_arm_backwards(distance)

def move_arm_up(distance)

def move_arm_down(distance)

def open_gripper(power)

def close_gripper(power)

