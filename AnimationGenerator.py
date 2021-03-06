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
from Text import *
import FileSaver
import time

def main():
  screen = pg.display.set_mode(SCREEN_SIZE)
  pg.display.set_caption("Animation Tool")

  em = EventManager()
  fm = FrameManager()
  ms = ModeSelector(fm,em,screen) # Mode Indicator GUI

  while em.running:
    # time.sleep(0.1) # slow loop for debugging
    screen.fill((20,0,50))

    em.update()

    try:
      if em.keyboard[pg.K_s].checkFall() and em.keyboard[pg.K_LCTRL].checkHeld():
          FileSaver.saveToFile("saveFiles", "saveFile", fm)
      if em.keyboard[pg.K_o].checkFall() and em.keyboard[pg.K_LCTRL].checkHeld():
          fm = FileSaver.loadFromFile("saveFiles", "saveFile.sav")
          ms = ModeSelector(fm,em,screen)
    except Exception as exp:
      print(str(exp))

    fm.update(em)
    ms.update(em)

    # Undo/Redo #
    if em.keyboard[pg.K_z].checkFall() and em.keyboard[pg.K_LCTRL].checkHeld():
      if em.keyboard[pg.K_LSHIFT].checkHeld():
        fm.currFrame.ah.redo()
      else:
        fm.currFrame.ah.undo()
    #############

    if (em.console.isActive()):
      em.console.draw(screen)

    fm.draw(screen)
    ms.draw(screen)

    pg.display.update()


if __name__ == "__main__":
  pg.init()
  main()
  pg.quit()
