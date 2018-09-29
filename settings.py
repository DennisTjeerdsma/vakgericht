# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 13:54:27 2018

@author: Dennis Tjeerdsma
"""

import os
from redis import Redis

redis = Redis.from_url(os.environ.get("REDIS_URL"))
