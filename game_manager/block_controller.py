#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime
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
        self.MYDEBUG=isshy.MYDEBUG
 
        t1 = datetime.now()
        # print GameStatus
        print("=================================================>")
        del GameStatus["field_info"]["withblock"]
        # pprint.pprint(GameStatus, width = 61, compact = True)
        if self.MYDEBUG: print('[board] index =',GameStatus["block_info"]["currentShape"]["index"])
        if self.MYDEBUG: pprint.pprint(GameStatus["field_info"]["backboard"], width = 31, compact = True)

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

        EvalValue,x0,direction0 = isshy.calcEvaluationValue(GameStatus)
        strategy = (direction0,x0,1,1)
        if (self.MYDEBUG) : print("<<< isshy-you:(EvalValue,shape,strategy(dir,x,y_ope,y_mov))=(",EvalValue,GameStatus["block_info"]["currentShape"]["index"],strategy,")")

        processtime = datetime.now()-t1
        print("=== processing time ===(", processtime,")")
        nextMove["strategy"]["direction"] = strategy[0]
        nextMove["strategy"]["x"] = strategy[1]
        nextMove["strategy"]["y_operation"] = strategy[2]
        nextMove["strategy"]["y_moveblocknum"] = strategy[3]
        print("=== nextMove:",nextMove)
        return nextMove

BLOCK_CONTROLLER = Block_Controller()
isshy=lib_tetris_isshy.lib_tetris()

