#!/usr/bin/python3
# -*- coding: utf-8 -*-

# from datetime import datetime
import time
import pprint
import copy
import lib_tetris_isshy

class Block_Controller(object):

    # init parameter
    board_backboard = 0
    board_data_width = 0
    board_data_height = 0
    ShapeNone_index = 0
    CurrentShape_class = 0
    NextShape_class = 0

    # GetNextMove is main function.
    # input
    #    nextMove : nextMove structure which is empty.
    #    GameStatus : block/field/judge/debug information. 
    #                 in detail see the internal GameStatus data.
    # output
    #    nextMove : nextMove structure which includes next shape position and the other.
    def GetNextMove(self, nextMove, GameStatus):
        self.MYDEBUG = isshy.MYDEBUG
        self.HOLDMODE = isshy.HOLDMODE
        self.DEBUG = True
 
        t1 = time.time()
        # print GameStatus
        if self.DEBUG: print("=================================================>")
        del GameStatus["field_info"]["withblock"]
        # pprint.pprint(GameStatus, width = 61, compact = True)
        if self.MYDEBUG: print('[board] index =',GameStatus["block_info"]["currentShape"]["index"])
        # if self.MYDEBUG: pprint.pprint(GameStatus["field_info"]["backboard"], width = 31, compact = True)
        if self.MYDEBUG: 
            for jj in range(GameStatus["field_info"]["height"]):
                tmpstr=''
                for ii in range(GameStatus["field_info"]["width"]):
                    tmpstr = tmpstr + str(GameStatus["field_info"]["backboard"][jj*GameStatus["field_info"]["width"]+ii]) + ' '
                print(format(jj,'02d'),tmpstr)
            print('-- 0 1 2 3 4 5 6 7 8 9 0 --' )
        # # get data from GameStatus
        # # current shape info
        # CurrentShapeDirectionRange = GameStatus["block_info"]["currentShape"]["direction_range"]
        # self.CurrentShape_class = GameStatus["block_info"]["currentShape"]["class"]
        # self.CurrentShape_index = GameStatus["block_info"]["currentShape"]["index"]
        # # next shape info
        # NextShapeDirectionRange = GameStatus["block_info"]["nextShape"]["direction_range"]
        # self.NextShape_class = GameStatus["block_info"]["nextShape"]["class"]
        # self.NextShape_index = GameStatus["block_info"]["nextShape"]["index"]
        # # current board info
        # self.board_backboard = GameStatus["field_info"]["backboard"]
        # # default board definition
        # self.board_data_width = GameStatus["field_info"]["width"]
        # self.board_data_height = GameStatus["field_info"]["height"]
        # self.ShapeNone_index = GameStatus["debug_info"]["shape_info"]["shapeNone"]["index"]


        print(GameStatus["block_info"]["holdShape"]["index"])
        if self.HOLDMODE and GameStatus["block_info"]["holdShape"]["index"] == None:
            ### store hold and use next shape
            if self.DEBUG: print('store hold and use next shape')
            EvalValue,x0,direction0 = isshy.calcEvaluationValue(GameStatus,0)
            strategy = (direction0,x0,1,1,'y')
        else:
            ### use current shape
            EvalValue,x0,direction0 = isshy.calcEvaluationValue(GameStatus,0)
            if self.HOLDMODE:
                HoldShapeDirectionRange = GameStatus["block_info"]["holdShape"]["direction_range"]
                HoldShapeClass = GameStatus["block_info"]["holdShape"]["class"]
                if (self.MYDEBUG) : print("HoldShapeDirectionRange,HoldshapeCalss=",HoldShapeDirectionRange,HoldShapeClass)
                ### use hold shape 
                EvalValue_hold,x0_hold,direction0_hold = isshy.calcEvaluationValue(GameStatus,1)
                if (self.DEBUG) : print('Normal:',EvalValue,x0,direction0)
                if (self.DEBUG) : print('Hold  :',EvalValue_hold,x0_hold,direction0_hold)

            if self.HOLDMODE:
                if EvalValue < EvalValue_hold:
                    EvalValue = EvalValue_hold
                    strategy = (direction0_hold,x0_hold,1,1,'y')
                else:
                    strategy = (direction0,x0,1,1,'n')
            else:
                strategy = (direction0,x0,1,1,'n')

        if (self.MYDEBUG) : print("<<< isshy-you:(EvalValue,shape,strategy(dir,x,y_ope,y_mov))=(",EvalValue,GameStatus["block_info"]["currentShape"]["index"],strategy,")")
        processtime = time.time()-t1
        if self.DEBUG:
            print("=== block index(current) === (", GameStatus["block_info"]["currentShape"]["index"],")")
            print("=== block index(hold)    === (", GameStatus["block_info"]["holdShape"]["index"],")")
            if strategy[4] == 'n':
                print("=== use current          ===")
            else:
                print("=== use hold             ===")

        if self.DEBUG:  print("=== processing time === (", processtime,") under usec(",processtime<0.001,")")
        nextMove["strategy"]["direction"] = strategy[0]
        nextMove["strategy"]["x"] = strategy[1]
        nextMove["strategy"]["y_operation"] = strategy[2]
        nextMove["strategy"]["y_moveblocknum"] = strategy[3]
        nextMove["strategy"]["use_hold_function"] = strategy[4]
        # print("=== nextMove:",nextMove)
        if self.DEBUG:  print("=== nextMove        === dir(",strategy[0],") xpos(",strategy[1],")")
        return nextMove

BLOCK_CONTROLLER = Block_Controller()
isshy=lib_tetris_isshy.lib_tetris()

