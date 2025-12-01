import importlib
backend_app = importlib.import_module('backend.app')
globals().update(backend_app.__dict__)
