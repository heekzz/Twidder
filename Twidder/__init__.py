# coding=utf-8
from flask import Flask, request, json
import database_helper
import json, hashlib, string, random


__author__ = 'Fredrik Håkansson (freha309)'

app = Flask(__name__, static_url_path='')

import Twidder.views
