from werkzeug.local import LocalProxy
from flask import current_app
import warnings
import os
from ghost import Ghost
from multiprocessing import Process
haunted = LocalProxy(lambda: current_app.ghost_manager)


class GhostManager(object):
    def __init__(self, app=None):
        self._debug = False
        if app is not None:
            self.init_app(app)

    def _create_ghost(self):
        return Ghost(wait_timeout=20)

    def _inner_take_picture(self, url, full_path):
        """
        needed by the take_picture to be spawned byt multi_process
        """
        ghost = self._create_ghost()
        ghost.open('http://' + url)
        ghost.capture_to(full_path)

    def take_picture(self, url, save_path):
        url = url.replace('http://', '')
        if not url:
            return ''
        clean_url = ''.join(ch for ch in url if ch.isalnum())
        file_name = '%s.png' % clean_url
        full_path = os.path.join(save_path, file_name)  # includes the filename
        p = Process(target=self._inner_take_picture, args=(url, full_path))
        p.start()
        return file_name  # returns the name of the saved image
    
    def setup_app(self, app):  # pragma: no cover
        '''
        This method has been deprecated. Please use
        :meth:`GhostManager.init_app` instead.
        '''
        warnings.warn('Warning setup_app is deprecated. Please use init_app.',
                      DeprecationWarning)
        self.init_app(app)

    def init_app(self, app):
        '''
        Configures an application. This registers a `before_request` and an
        `after_request` call, and attaches this `LoginManager` to it as
        `app.login_manager`.

        :param app: The :class:`flask.Flask` object to configure.
        :type app: :class:`flask.Flask`
        '''
        app.ghost_manager = self
        try:
            if app.config['DEBUG'] is True:
                self._debug = True
        except KeyError:
            self._debug = False