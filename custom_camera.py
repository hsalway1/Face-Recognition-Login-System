from kivy.uix.image import Image
from kivy.core.camera import Camera as CoreCamera
from kivy.properties import NumericProperty, ListProperty, BooleanProperty

# access to camera
core_camera = CoreCamera(index=0, resolution=(1280, 720), stopped=True, dimension = (1280, 720))

# Widget to display camera
class CameraCv(Image):
    '''Camera class. See module documentation for more information.
    '''

    play = BooleanProperty(True)
    '''Boolean indicating whether the camera is playing or not.
    You can start/stop the camera by setting this property::
        # start the camera playing at creation (default)
        cam = Camera(play=True)
        # create the camera, and start later
        cam = Camera(play=False)
        # and later
        cam.play = True
    :attr:`play` is a :class:`~kivy.properties.BooleanProperty` and defaults to
    True.
    '''

    index = NumericProperty(-1)
    '''Index of the used camera, starting from 0.
    :attr:`index` is a :class:`~kivy.properties.NumericProperty` and defaults
    to -1 to allow auto selection.
    '''

    resolution = ListProperty([-1, -1])
    '''Preferred resolution to use when invoking the camera. If you are using
    [-1, -1], the resolution will be the default one::
        # create a camera object with the best image available
        cam = Camera()
        # create a camera object with an image of 320x240 if possible
        cam = Camera(resolution=(320, 240))
    .. warning::
        Depending on the implementation, the camera may not respect this
        property.
    :attr:`resolution` is a :class:`~kivy.properties.ListProperty` and defaults
    to [-1, -1].
    '''

    def __init__(self, **kwargs):
        self._camera = None
        super().__init__(**kwargs)  # `MyCamera` instead of `Camera`
        if self.index == -1:
            self.index = 0
        on_index = self._on_index
        fbind = self.fbind
        fbind('index', on_index)
        fbind('resolution', on_index)
        on_index()

    def on_tex(self, *l):
        self.canvas.ask_update()

    def _on_index(self, *largs):
        self._camera = None
        if self.index < 0:
            return
        if self.resolution[0] < 0 or self.resolution[1] < 0:
            return

        self._camera = core_camera # `core_camera` instead of `CoreCamera(index=self.index, resolution=self.resolution, stopped=True)`

        self._camera.bind(on_load=self._camera_loaded)
        if self.play:
            self._camera.start()
            self._camera.bind(on_texture=self.on_tex)

    def _camera_loaded(self, *largs):
        self.texture = self._camera.texture
        self.texture_size = list(self.texture.size)

    def on_play(self, instance, value):
        if not self._camera:
            return
        if value:
            self._camera.start()
        else:
            self._camera.stop()