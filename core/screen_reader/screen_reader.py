import ctypes

from python_imagesearch.imagesearch import imagesearcharea, region_grabber

from core.app_state import app_state, app_data
from core.json_reader.json_reader import get_profile_list, get_profile


def determine_profile():
    app_data.set_profile_list(get_profile_list())

    __screensize = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)

    x0 = int(__screensize[0] - __screensize[0] / 3)
    y0 = int(__screensize[1] - __screensize[1] / 3)
    x1 = int(__screensize[0])
    y1 = int(__screensize[1])

    region = region_grabber((x0, y0, x1, y1))

    for key in [element for element in app_data.get_profile_list() if
                element not in {'profile_1', 'profile_2', 'profile_3', 'default'}]:
        try:
            res = imagesearcharea(
                './settings/icons_to_search/' + key + '.png',
                x0,
                y0,
                x1,
                y1,
                0.9,
                region
            )

            if res[0] != -1:
                app_state.set_forces(get_profile(key))
                return
        except FileNotFoundError:
            print('[WARNING]:', key, 'image not found')

    print("nothing found, setting default")
    app_state.set_forces(get_profile("default"))
