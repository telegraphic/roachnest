#!/usr/bin/env python
# encoding: utf-8
"""
config.py
============

This is the main configuration file for CASPER GUI. 

Change the variables below to modify the appearance of the GUI. 

"""
# Basic setup
title        = "roachnest"
version      = "v1"

# File paths
import os
dirroot  = os.getcwd()
database = 'hardware.db'
#database = 'test.db'

# Change logo and stylesheet
branding_css = '/files/branding.css'
branding_logo= '/files/logos/logo_roach.png'
favicon      = '/files/favicon.ico'


