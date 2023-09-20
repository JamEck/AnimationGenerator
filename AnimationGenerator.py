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
          FileSaver.saveToJson("saveFiles", "saveFile", fm)
          FileSaver.saveToBinary("saveFiles", "saveFile", fm)
      if em.keyboard[pg.K_o].checkFall() and em.keyboard[pg.K_LCTRL].checkHeld():
          fm = FrameManager.genFromJson("saveFiles", "saveFile.json")
          ms = ModeSelector(fm,em,screen)
    except Exception as exp:
      print(str(exp))
      print(tb.format_exc())

    fm.update(em)

    if em.console.checkExecute():
      cmdLine = em.console.getTextEntry()
      if cmdLine:
        try:
          if cmdLine.startswith('>'):
            cmd = cmdLine[1:]
            print("Execute: " + cmd)
            exec(cmd)
          else:
            ms.currMode.runFromConsole(cmdLine)
        except IndexError as ie:
          print("No Data To Operate On: {}: {}".format(str(ie), tb.format_exc()))
        except KeyError as ke:
          print("Command not found: {}: {}".format(str(ke), tb.format_exc()))
        except Exception as exp:
          print("{}: {}: {}".format(type(exp).__name__, str(exp), tb.format_exc()))

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
