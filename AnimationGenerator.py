import pygame as pg
from Utils import *
from ActionHistory import *
from Mouse import Mouse
from EventManager import EventManager
from UIButton import UIButton
from Geometry     import *
from DataManager  import DataManager
from ToolModes    import *
from FrameManager import *
import time

pg.init()

screen = pg.display.set_mode((1280,960))
pg.display.set_caption("Animation Tool")

em = EventManager()

fm = FrameManager()
mi = ModeIndicator(fm.currFrame.dm)     # Mode Indicator GUI
mo = SelectMode(fm.currFrame,em,screen) # Current Tool Mode

font = pg.font.SysFont("monospace", 20)

nearest = None
while em.running:
  # time.sleep(0.1) # slow loop for debugging
  screen.fill((20,0,50))
  em.update()

  # Frame Control #
  if em.keyboard[pg.K_RIGHT].checkFall():
    fm.next()
    mi.dm = fm.currFrame.dm
    mo.dm = fm.currFrame.dm
    mo.ah = fm.currFrame.ah
  if em.keyboard[pg.K_LEFT].checkFall():
    fm.prev()
    mi.dm = fm.currFrame.dm
    mo.dm = fm.currFrame.dm
    mo.ah = fm.currFrame.ah
  if em.keyboard[pg.K_d].checkFall():
    if em.keyboard[pg.K_LCTRL].checkHeld():
      fm.delete()
      mi.dm = fm.currFrame.dm
      mo.dm = fm.currFrame.dm
      mo.ah = fm.currFrame.ah

  #################

  # Choose Tool Mode #
  if   em.keyboard[pg.K_s].checkFall():
    mi.select("select")
    mo.reset()
    mo = SelectMode(fm.currFrame,em,screen)
  elif em.keyboard[pg.K_v].checkFall():
    mi.select("vertex")
    mo.reset()
    mo = VertexMode(fm.currFrame,em,screen)
  elif em.keyboard[pg.K_l].checkFall():
    mi.select("line")
    mo.reset()
    mo = LineMode(fm.currFrame,em,screen)
  elif em.keyboard[pg.K_c].checkFall():
    mi.select("circle")
    mo.reset()
    mo = CircleMode(fm.currFrame,em,screen)
  elif em.keyboard[pg.K_p].checkFall():
    mi.select("pill")
    mo.reset()
    mo = PillMode(fm.currFrame,em,screen)

  if em.keyboard[pg.K_ESCAPE].checkFall():
    mo.reset()
  ####################

  fm.draw(screen)

  # Mode Actions #
  if not em.keyboard[pg.K_LSHIFT].checkHeld():
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
  ################

  # Undo/Redo #
  if em.keyboard[pg.K_z].checkFall():
    if em.keyboard[pg.K_LCTRL].checkHeld():
      if em.keyboard[pg.K_LSHIFT].checkHeld():
        fm.currFrame.ah.redo()
      else:
        fm.currFrame.ah.undo()
  #############

  mi.draw(screen)

  pg.display.update()

pg.quit()