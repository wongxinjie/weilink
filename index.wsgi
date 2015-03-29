import os
import sys
import sae
from weilink import wsgi

application = sae.create_wsgi_app(wsgi.application)
