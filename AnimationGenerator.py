import pygame as pg
from Utils import *
from ActionHistory import *
from Mouse import Mouse
from EventManager import EventManager
from UIButton import UIButton
from Geometry import *
from DataManager import DataManager
from ToolModes import *
import time



pg.init()

screen = pg.display.set_mode((1280,960))
pg.display.set_caption("Animation Tool")


em = EventManager()
dm = DataManager()
ah = ActionHistory()
mi = ModeIndicator()
mo = SelectMode(em,dm,ah,screen)

nearest = None
while em.running:
  # time.sleep(0.1) # slow loop for debugging
  screen.fill((20,0,50))
  em.update()

  # Choose Tool Mode #
  if   em.keyboard[pg.K_s].checkFall():
    mi.select("select")
    mo = SelectMode(em,dm,ah,screen)
  elif em.keyboard[pg.K_v].checkFall():
    mi.select("vertex")
    mo = VertexMode(em,dm,ah,screen)
  elif em.keyboard[pg.K_l].checkFall():
    mi.select("line")
    mo = LineMode(em,dm,ah,screen)
  elif em.keyboard[pg.K_c].checkFall():
    mi.select("circle")
    mo = CircleMode(em,dm,ah,screen)
  ####################

  # if not em.keyboard[pg.K_LSHIFT].checkHeld():
  mo.onHover()
  if em.mouse.left.checkFall():
    mo.onLeftFall()
  if em.mouse.left.checkHeld():
    mo.onLeftHeld()
  if em.mouse.left.checkRise():
    mo.onLeftRise()
  if em.mouse.middle.checkFall():
    mo.onMiddleFall()
  if em.mouse.middle.checkHeld():
    mo.onMiddleHeld()
  if em.mouse.middle.checkRise():
    mo.onMiddleRise()
  if em.mouse.right.checkFall():
    mo.onRightFall()
  if em.mouse.right.checkHeld():
    mo.onRightHeld()
  if em.mouse.right.checkRise():
    mo.onRightRise()


  # Undo/Redo #
  if em.keyboard[pg.K_LCTRL].checkHeld():
    if em.keyboard[pg.K_z].checkFall():
      if em.keyboard[pg.K_LSHIFT].checkHeld():
        ah.redo()
      else:
        ah.undo()
  #############

  mi.draw(screen)
  dm.draw(screen)
  pg.display.update()

pg.quit()