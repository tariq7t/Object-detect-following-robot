# Extraterrestrial Life Evaluator- Earth Class ELE-E (Fall 2019) – Autonomous Object Detecting & Following Robot

## Used OpenCV Library in Python to implement algorithms for the movement of robot. The robot detects an object pre-specified and proceeds to continuously follow it while remaining at a distance.

- Implemented object recognition though OpenCV
- Operated robot on a Raspberry PI powered with portable charger as power source. Used a Logitech webcam for video input.
- Motor controllers were separately powered with lithium batteries
- The code is executed by SSH-ing from an external device into the Pi.
- After object recognition is done, my algorithm measures the area of the object and proceeds to follow it if area is smaller than a specified amount.
- The object is kept at the center of camera with a simple centroid algorithm. If object moves past center of frame, my robot will turn so object comes back at center.
