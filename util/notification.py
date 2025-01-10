import time
from threading import Lock, Thread

import blf
import bpy
import gpu
from gpu_extras.batch import batch_for_shader

# vertices = (
#     (100, 100), (300, 100),
#     (100, 200), (300, 200))

indices = (
    (0, 1, 2), (2, 1, 3))

if bpy.app.version < (4, 0, 0):
    shader_name = '2D_UNIFORM_COLOR'
else:
    shader_name = 'UNIFORM_COLOR'

shader = gpu.shader.from_builtin(shader_name)
# shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
# shader = gpu.shader.from_builtin('POLYLINE_UNIFORM_COLOR')

GENERAL = 0
ERROR = 1
ALERT = 2
OK = 3
SUCCESS = 4

GENERAL_COL = (.3, .3, .3, 1)
ERROR_COL = (.7, .1, .1, 1)
ALERT_COL = (.6, .4, .1, 1)
OK_COL = (0, .6, .1, 1)
SUCCESS_COL = (.1, .2, .7, 1)

class Notification:
    def __init__(self, message, duration=None, status = GENERAL):
        self.__message = message
        self.__duration = duration
        self.__status = status

    def __str__(self):
        return self.__message

    @property
    def duration(self):
        return self.__duration

    @property
    def status(self):
        return self.__status

def get_color(notif):
    st = notif.status
    if st == GENERAL:
        return GENERAL_COL
    if st == ERROR:
        return ERROR_COL
    if st == ALERT:
        return ALERT_COL
    if st == OK:
        return OK_COL
    if st == SUCCESS:
        return SUCCESS_COL
    return GENERAL_COL

_notifications = None
_notifications_lock = None


def _draw():
    font_id = 0
    font_size = 13
    margin = 10
    padding = 8
    offset_underline = 3

    blf.color(font_id, 1, 1, 1, 1)
    y = margin

    if bpy.app.version < (4, 0, 0):
        blf.size(font_id, font_size, 72)  # 3.6以前の場合
    else:
        blf.size(font_id, font_size)  # 4.0以降の場合
    # blf.size(font_id, font_size, 72)
    with _notifications_lock:
        for notification in _notifications:
            dim = blf.dimensions(font_id, str(notification))

            vertices = (
            (margin, y), (dim[0]+margin+padding*4, y),
            (margin, y+dim[1]+offset_underline+padding*2), (dim[0]+margin+padding*4, y+dim[1]+offset_underline+padding*2))

            batch = batch_for_shader(shader, 'TRIS', {"pos": vertices}, indices=indices)
            blf.position(font_id, margin+padding*2, y+offset_underline+padding, 0)
            shader.bind()
            shader.uniform_float("color", get_color(notification))
            batch.draw(shader)
            blf.draw(font_id, str(notification))
            y += dim[1] + margin + padding * 2 + offset_underline


def add(notification):
    global _notifications
    global _notifications_lock
    with _notifications_lock:
        _notifications.append(notification)

    if notification.duration is not None:
        def _run_thread_wait_and_remove_notification():
            time.sleep(notification.duration)
            remove(notification)

        thread = Thread(target=_run_thread_wait_and_remove_notification)
        thread.start()


def remove(notification):
    global _notifications
    global _notifications_lock
    with _notifications_lock:
        _notifications.remove(notification)

_draw_handler = None

def register():
    global _notifications
    global _notifications_lock
    global _draw_handler

    _notifications = []
    _notifications_lock = Lock()

    _draw_handler = bpy.types.SpaceView3D.draw_handler_add(_draw, (), 'WINDOW', 'POST_PIXEL')


def unregister():
    global _draw_handler
    bpy.types.SpaceView3D.draw_handler_remove(_draw_handler, 'WINDOW')
