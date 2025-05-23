import collections

class ObservableDict(collections.UserDict):
    """
    A dictionary that notifies a callback on any value change.
    """
    def __init__(self, *args, callback=None, **kwargs):
        self._callback = callback  # Set this first!
        super().__init__(*args, **kwargs)

    def set_callback(self, callback):
        self._callback = callback

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        if self._callback:
            self._callback(key, value)
