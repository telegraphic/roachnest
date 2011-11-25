#!/usr/bin/env python
# encoding: utf-8
"""
config.py
============

This is the main configuration file for CASPER GUI. 

Change the variables below to modify the appearance of the GUI. 

"""
# Basic setup
backend_name = 'level 3'
title        = "%s roachnest"%backend_name
version      = "v1"

# File paths
import os
dirroot  = os.getcwd()
database = 'hardware.db'

# Change logo and stylesheet
branding_css = '/files/branding.css'
branding_logo= '/files/logos/dancing-hamsters-1.gif'
favicon      = '/files/favicon.ico'


