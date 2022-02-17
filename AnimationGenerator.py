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
mi = ModeSelector(fm,em,screen) # Mode Indicator GUI


nearest = None
while em.running:
  # time.sleep(0.1) # slow loop for debugging
  screen.fill((20,0,50))

  em.update()
  fm.update(em)
  mi.update(em)

  # Undo/Redo #
  if em.keyboard[pg.K_z].checkFall():
    if em.keyboard[pg.K_LCTRL].checkHeld():
      if em.keyboard[pg.K_LSHIFT].checkHeld():
        fm.currFrame.ah.redo()
      else:
        fm.currFrame.ah.undo()
  #############

  fm.draw(screen)
  mi.draw(screen)

  pg.display.update()

pg.quit()