#!/usr/bin/env python

__author__ = 'John Wilkinson, python docu, stack overflow, the internet at large, and Amanda Y for some help debugging'

import requests
import turtle
import time 

indy = [39.76838, -86.15804]

def astronauts_roster():
    """ this funtion hit an API and retireves a list of astronauts on the ISS.
        Then it pulls out each astronauts full name and their craft and finally 
        displays how many total astronauts are on board
    """
    r = requests.get('http://api.open-notify.org/astros.json').json()
    astro = ''
    for astronauts in r['people']:
        astro += astronauts['name'] + ' is on ' + astronauts['craft'] + '\n'
    astro += f'There are a total of {len(r["people"])} on the {r["people"][0]["craft"]}'
    print(astro)
    return astro

def iss_locale():
    """returns the current locations of the ISS in long and lat"""
    r = requests.get('http://api.open-notify.org/iss-now.json').json()
    res = f'@ {r["timestamp"]} the ISS is at the longitude {r["iss_position"]["longitude"]} / latitude {r["iss_position"]["latitude"]}'
    print(res)
    print(r)
    return r

def map(iss_location, indy_pass):
    """sets up and generates a map of the globe with Indy and the current location of the ISS"""
    # sets up the screen with the backgroung image
    screen = turtle.Screen()
    screen.bgcolor('black')
    screen.setup(width=720, height=360, startx=None, starty=None)
    screen.setworldcoordinates(-180, -90, 180, 90)
    screen.bgpic('map.gif')
    screen.register_shape('iss.gif')
    # sets up the ISS icon
    iss = turtle.Turtle()
    iss.shape('iss.gif')
    iss.setheading(90)
    longitude = round(float(iss_location['iss_position']['longitude']))
    latitude = round(float(iss_location['iss_position']['latitude']))
    iss.penup()
    iss.goto(longitude, latitude)
    # Indy
    indy = turtle.Turtle()
    indy.shape('triangle')
    indy.color('white')
    indy.setheading(90)
    indy.penup()
    indy.goto(-86.1, 39.8 )
    indy.write(indy_pass)
    turtle.done()



def next_passover():
    api = 'http://api.open-notify.org/iss-pass.json'
    next_indy_passover = requests.get(f'{api}?lat={indy[0]}&lon=\
        {indy[1]}').json()
    nip_ctime = time.ctime(next_indy_passover['response'][0]['risetime'])
    print(nip_ctime)
    return nip_ctime
    

next_passover()

def main():

    loc_iss = iss_locale()
    next_time_passover = next_passover()
    map(loc_iss, next_time_passover)


if __name__ == '__main__':
    main()
