#!/usr/bin/python3
"""
File: currently_running_loop.py
Author: Asyncio recipes a problem-solution approach
Email: 
Github: 
Description: 

    Tells if an event loop is currently running and which one it is
"""
import asyncio

print("Method one")
try:
    loop = asyncio.get_event_loop()
    print(loop)
except RuntimeError:
    print("No loop running")

print("Method two")
try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    print("No loop running")
