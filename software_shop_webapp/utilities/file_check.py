from software_shop_webapp import ALLOWED_FILE_EXTENSIONS
from software_shop_webapp import ALLOWED_IMAGE_EXTENSIONS
from software_shop_webapp import ALLOWED_VIDEO_EXTENSIONS


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_FILE_EXTENSIONS
        
        
def allowed_image(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS
        
        
def allowed_video(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_VIDEO_EXTENSIONS