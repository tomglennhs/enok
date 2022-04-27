import uuid
from typing import Dict, Any, Callable, NewType, Type, List, Optional

from pydantic import BaseModel

from status import state

import numpy as np
import cv2 as cv

SubscriberFunc: Type = NewType("SubscriberFunc", Callable[[np.ndarray], Any])

# key is printer id
# val is a dict. key is subscription id, val is a function that get called when a new frame is added for that printer
_subscribers: Dict[int, Dict[str, SubscriberFunc]] = {}


class Camera(BaseModel):
    addr: str
    video_capture: Any
    ok: bool
    # frame: np.ndarray
    frame: Any


# key is printer id,
# val is a list. item one is a local camera id, or mjpg stream - as long as opencv supports it, we're chilling
# item 2 is a cv.VideoCapture instance - wish there was a better type but that
# seems it'll come eventually(tm) -> https://github.com/opencv/opencv-python/issues/656
# item 3 is a bool indicating whether frames are being read succesfully. false if there are errors
# item 4 is the latest frame
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
            current_cam = i[0]
            if current_cam == printer.printer.camera:
                new = False
                break
        if new:
            # TODO: Init the cv.VideoCapture unless there's no camera in which case do nothing
            pass
        elif printer.printer.camera != _cameras[printer.printer_id][0]:
            # TODO: the currently stored db value for a camera is not the one we've been using, so it's changed
            # stop the original videocapture, make sure to vid.release()
            # then replace with new cv.VideoCapture using new cam addr
            # also be sure to delete cams from _cameras that have been removed from db
            pass
    for p in state:
        if p not in seen:
            # TODO: set up the new printer in subscribers and cameras
            _subscribers[p] = {}
            cam_addr = state[p].printer.camera
            _cameras[p] = Camera(cam_addr=state[p].printer.camera, video_capture=cv.VideoCapture(cam_addr), ok=True,
                                 frame=None)


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
        # you're already unsubscribed, so we don't need to do anything if there is a KeyError
        pass
