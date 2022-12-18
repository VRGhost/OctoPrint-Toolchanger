"""Opencv code to do XY aligment of tolls"""

import argparse
import sys
from typing import Iterator
import pyudev
import numpy
import cv2
import time


def list_devices():
    # XXX: Linux-specific!
    ctx = pyudev.Context()
    for dev in ctx.list_devices(ID_TYPE="video"):
        capabilities = dev.properties.get("ID_V4L_CAPABILITIES") or ""
        if ":capture:" in capabilities.lower():
            yield {
                "model": dev.get("ID_MODEL") or "UNKNOWN",
                "devname": dev.get("DEVNAME"),
            }


def iter_frames(dev: cv2.VideoCapture) -> Iterator[numpy.ndarray]:
    MAX_HEATUP_TIME = 5  # seconds
    start_t = time.time()
    while True:
        (success, frame) = dev.read()
        if not success:
            if (start_t + MAX_HEATUP_TIME) >= time.time():
                # Still in the heatup time window
                print("wait...")
                time.sleep(1)
                # re-open
                continue
            else:
                raise Exception("Can't receive frame (stream end?). Exiting ...")
        assert success
        yield frame


def detect_circle(image: numpy.ndarray) -> tuple[int, int, int] | None:  # (x, y, size)
    circles = cv2.HoughCircles(
        image,
        cv2.HOUGH_GRADIENT,
        dp=4,
        minDist=400,
        param1=200,
        param2=120,
        minRadius=0,
        maxRadius=150,
    )
    if (circles is not None) and circles.any():
        return numpy.uint16(numpy.around(circles))[0, :]
    else:
        return None


def draw_crosshair(image: numpy.ndarray) -> numpy.ndarray:
    (width, height, _) = image.shape
    mid_h = height // 2
    mid_w = width // 2
    red = (0, 0, 255)  # bgr colour
    # vertical image
    cv2.line(image, (mid_h, 0), (mid_h, width), red, 1)
    # horizontal line
    cv2.line(image, (0, mid_w), (height, mid_w), red, 1)
    cv2.circle(image, (mid_h, mid_w), 100, red, 1)
    return image


def draw_detected_circle(circle: tuple, image: numpy.ndarray):
    (width, height, _) = image.shape
    img_mid_h = height // 2
    img_mid_w = width // 2

    (cx, cy, r, *_) = circle
    cyan = (0, 255, 255)
    cv2.circle(image, (cx, cy), r, cyan, 2)
    cv2.line(image, (img_mid_h, img_mid_w), (cx, cy), cyan)


def main_capture(devname: str):
    cap = cv2.VideoCapture(devname)
    # cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MPG4'))
    if not cap.isOpened():
        raise Exception("Cannot open camera")
    try:
        for colour_frame in iter_frames(cap):
            # Our operations on the frame come here
            gray = cv2.cvtColor(colour_frame, cv2.COLOR_BGR2GRAY)
            detected_circles = detect_circle(gray)
            # Display the resulting frame
            draw_crosshair(colour_frame)
            if (detected_circles is not None) and detected_circles.any():
                draw_detected_circle(detected_circles[0], colour_frame)
            cv2.imshow("frame", colour_frame)
            if cv2.waitKey(1) == ord("q"):
                break
    finally:
        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()


def get_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser("OpenCV circle detection.")
    parser.add_argument("--device", default=None, help="Camera to capture video with.")
    return parser


if __name__ == "__main__":
    args = get_argument_parser().parse_args()
    if not args.device:
        print("Available cameras: ")
        print(list(list_devices()))
        sys.exit(1)
    main_capture(args.device)
