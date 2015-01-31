'''
OpenCV Camera: Implement CameraBase with OpenCV 2
'''

#
# TODO: make usage of thread or multiprocess
#

__all__ = ('CameraOpenCV2')

from kivy.logger import Logger
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.core.camera import CameraBase

import cv2
from cv2 import cv

class CameraOpenCV2(CameraBase):
    '''Implementation of CameraBase using OpenCV 2
    '''

    def __init__(self, **kwargs):
        self._device = None
        super(CameraOpenCV2, self).__init__(**kwargs)

    def init_camera(self):
        # create the device
        self._device = cv2.VideoCapture(self._index)

        # Set preferred resolution
        self._device.set(cv.CV_CAP_PROP_FRAME_WIDTH, self.resolution[0])
        self._device.set(cv.CV_CAP_PROP_FRAME_HEIGHT, self.resolution[1])

        # and get frame to check if it's ok
        ret, frame = self._device.read()
        # Just set the resolution to the frame we just got, but don't use
        # self.resolution for that as that would cause an infinite recursion
        # with self.init_camera (but slowly as we'd have to always get a
        # frame).
        h, w, c = frame.shape
        self._resolution = (int(w), int(h))

        #get fps
        self.fps = self._device.get(cv.CV_CAP_PROP_FPS)
        if self.fps <= 0:
            self.fps = 1 / 30.

        if not self.stopped:
            self.start()

    def _update(self, dt):
        if self.stopped:
            return
        if self._texture is None:
            # Create the texture
            self._texture = Texture.create(self._resolution)
            self._texture.flip_vertical()
            self.dispatch('on_load')
        try:
            ret, frame = self._device.read()
            self._format = 'bgr'
            self._buffer = frame.tostring()
            self._copy_to_gpu()
        except:
            Logger.exception('OpenCV: Couldn\'t get image from Camera')

    def start(self):
        super(CameraOpenCV2, self).start()
        Clock.unschedule(self._update)
        Clock.schedule_interval(self._update, self.fps)

    def stop(self):
        super(CameraOpenCV2, self).stop()
        Clock.unschedule(self._update)
