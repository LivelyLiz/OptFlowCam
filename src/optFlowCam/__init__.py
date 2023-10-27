bl_info = {
    "name": 'OptFlowCam',
    "author": "Lisa Piotrowski",
    "version": (0, 0, 1),
    "blender": (3, 50, 0),
    "location": "View3D > N-Panel > OptFlowCam",
    "description": "An add-on for interpolating smooth camera paths.",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Animation",
}

modules = ['utility', 'math', 'interpolation', 'ui', 'properties', 
           'objects', 'operators']

from . import register_modules

def register():
    full_names = register_modules.get_full_module_names(modules, __name__)
    register_modules.register(full_names)

def unregister():
    full_names = register_modules.get_full_module_names(modules, __name__)
    register_modules.unregister(full_names)

if __name__ == "__main__":
    register()