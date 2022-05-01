import uuid
from typing import Dict, Any, Callable, List, Optional

from pydantic import BaseModel

from status import state

import numpy as np
import cv2 as cv

SubscriberFunc = Callable[[np.ndarray], Any]

# key is printer id
# val is a dict. key is subscription id, val is a function that get called when a new frame is added for that printer
_subscribers: Dict[int, Dict[str, SubscriberFunc]] = {}


class Camera(BaseModel):
    addr: str
    """`addr` is a video source supported by OpenCV for capturing video, such as a local camera ID, or MJPEG stream URL."""
    video_capture: Any
    """`cv.VideoCapture` instance - wish there was a better type but that seems it'll come eventually(tm) -> https://github.com/opencv/opencv-python/issues/656 and https://github.com/opencv/opencv/pull/20370"""
    ok: bool
    """`True` if frames are being successfully read, `False` otherwise."""
    frame: Any
    """`np.ndarray` from OpenCV with the latest frame data."""



# key is printer id,
_cameras: Dict[int, Camera] = {}


def on_state_update():
    # TODO: Test performance of streaming with SSE vs WS vs MJPEG (this'll be in the api route)
    # WebRTC is too much effort imo. If we need to do that (ie all the above transports are genuinely awful/unusable)
    # we can go the WebRTC route but i don't want to deal with STUN/TURN servers
    # If we do want to go this route check out https://webrtc.org/getting-started/peer-connections
    # and https://github.com/abhiTronix/vidgear/blob/master/vidgear/gears/asyncio/webgear_rtc.py
    # ^ uses https://github.com/aiortc/aiortc
    # apparently google has free turn servers we can use so idk. we'll see
    seen: List[int] = []
    # If a printer id is in seen it is in subscribers
    for pid in _subscribers.keys():
        seen.append(pid)
        try:
            # make sure the printer still exists
            printer = state[pid]
        except KeyError:
            del _subscribers[pid]
            del _cameras[pid]
            continue
        new = True
        for i in _cameras.values():
            current_cam = i.addr
            if current_cam == printer.printer.camera:
                new = False
                break
        if new:
            if printer.printer.camera is not None and printer.printer.camera == "":
                c = _cameras[printer.printer_id]
                _cameras[printer.printer_id] = c.copy(update={"video_capture": cv.VideoCapture(
                    printer.printer.camera)})
        elif printer.printer.camera != _cameras[printer.printer_id].addr:
            # TODO: delete cams from _cameras that have been removed from db
            c = _cameras[printer.printer_id]
            c.video_capture.release()
            _cameras[printer.printer_id] = c.copy(update={"addr": printer.printer.camera, "video_capture": cv.VideoCapture(
                    printer.printer.camera)})
    for p in state:
        if p not in seen:
            _subscribers[p] = {}
            _cameras[p] = Camera(addr=state[p].printer.camera, video_capture=cv.VideoCapture(
                state[p].printer.camera), ok=True, frame=None)


def loop():
    for cam in _cameras:
        c = _cameras[cam]
        if not c.ok:
            continue
        try:
            ret, frame = c.video_capture.read()
            if not ret:
                _cameras[cam] = c.copy(update={"ok": False})
                continue
        except Exception as e:
            print(e)
            _cameras[cam] = c.copy(update={"ok": False})
            continue
        _cameras[cam] = c.copy(update={"ok": True, "frame": frame})
        p = _subscribers[cam]
        for func in p.values():
            try:
                func(frame)
            except Exception as e:
                print(e)


def subscribe(printer_id: int, on_frame: SubscriberFunc) -> Optional[str]:
    sub_id = str(uuid.uuid4())
    try:
        subscriber = _subscribers[printer_id]
    except KeyError:
        # printer doesn't exist, try again after `config.printerCheckFrequency`.
        return None
    subscriber[sub_id] = on_frame
    return sub_id


def unsubscribe(printer_id: int, sub_id: str):
    try:
        subscriber = _subscribers[printer_id]
        del subscriber[sub_id]
    except KeyError:
        # For one of many reasons (printer has been deleted, or you already unsubscribed)
        # you're not currently subscribed, so we don't need to do anything if there is a KeyError
        pass

def get_frame(printer_id: int) -> np.ndarray:
    return _cameras[printer_id].frame