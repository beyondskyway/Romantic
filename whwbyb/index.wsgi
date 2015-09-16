import sys
import os

app_root = os.path.dirname(__file__) 
sys.path.insert(0, os.path.join(app_root, 'site-packages'))

import sae

from wechat import app

application = sae.create_wsgi_app(app)