import os
import sys


def get_current_directory():
    p = os.path.dirname(sys.argv[0])
    plat = sys.platform
    if ("win" in plat):
        p = p[0].upper() + p[1:]
        # print(os.pathsep)
        p = p.replace("/", "\\")
    return p