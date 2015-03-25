from flask.ext.uploads import UploadSet, IMAGES, UploadNotAllowed  # the UploadNotAllowed is needed here
from random import randrange
import settings
import os

class UploadSet(UploadSet):
    """
    overrides some stuff to meet my requirements
    """
    def file_allowed(self, storage, basename):
        """
        dont allow too long filenames!
        """
        if super(UploadSet, self).file_allowed(storage, basename) is False:
            return False
        if len(basename) > settings.max_picture_name_len:
            return False
        return True
    
    def save(self, storage, name):
        """
        [I FORCE FOLDER=NONE]
        cause save to always return an extended path
        instead of just basename or folder + basename
        (it will now return something like: /static/uploads/webphotos/mypic.jpg
        """
        #the return value is only basename without a folder
        #the real constructor uses a folder so i just pass None
        folder = None
        #if its not str the module crashes
        name = str(name)
        if '.' not in name:
            name += '.jpg'

        path = super(UploadSet, self).save(storage, folder, name)
        before_path = settings.uploads_dir
        #self.name is the folder inside uploads (e.g webphotos)
        result = os.path.join(before_path, self.name, path)
        #fix windows-linux
        return result.replace('\\', '/')
    
    def save_random(self, storage, ext='.jpg'):
        """
        saves the file with a random name
        and appends the ext to it
        e.g: 123883.jpg
        """
        return self.save(storage, str(randrange(1, 10 ** 6)) + ext)
        
webphotos = UploadSet('webphotos', IMAGES)
logophotos = UploadSet('logophotos', IMAGES)
staticphotos = UploadSet('staticphotos', IMAGES)
tabphotos = UploadSet('tabphotos', IMAGES)
all_sets = [webphotos, logophotos, staticphotos, tabphotos]