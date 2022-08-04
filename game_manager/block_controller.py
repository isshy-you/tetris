#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime
import pprint
import copy
import lib_tetris_isshy

class Block_Controller(object):

    MYDEBUG = 0
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

        t1 = datetime.now()
        DEBUG = 0 #OFF
        # print GameStatus
        print("=================================================>")
        del GameStatus["field_info"]["withblock"]
        pprint.pprint(GameStatus, width = 61, compact = True)

        # get data from GameStatus
        # current shape info
        CurrentShapeDirectionRange = GameStatus["block_info"]["currentShape"]["direction_range"]
        self.CurrentShape_class = GameStatus["block_info"]["currentShape"]["class"]
        self.CurrentShape_index = GameStatus["block_info"]["currentShape"]["index"]
        # next shape info
        NextShapeDirectionRange = GameStatus["block_info"]["nextShape"]["direction_range"]
        self.NextShape_class = GameStatus["block_info"]["nextShape"]["class"]
        self.NextShape_index = GameStatus["block_info"]["nextShape"]["index"]
        # current board info
        self.board_backboard = GameStatus["field_info"]["backboard"]
        # default board definition
        self.board_data_width = GameStatus["field_info"]["width"]
        self.board_data_height = GameStatus["field_info"]["height"]
        self.ShapeNone_index = GameStatus["debug_info"]["shape_info"]["shapeNone"]["index"]

        # search best nextMove -->
        strategy = None
        LatestEvalValue = -100000

        # isshy=lib_tetris_isshy()
        # add additional code by isshy-you
        self.MYDEBUG=True
        if self.CurrentShape_index==1:
            EvalValue,x0,direction0 = isshy.calcEvaluationValueIndex1(GameStatus,self.board_backboard, self.NextShape_index)
        elif self.CurrentShape_index==2:
            EvalValue,x0,direction0 = isshy.calcEvaluationValueIndex2(GameStatus,self.board_backboard, self.NextShape_index)
        elif self.CurrentShape_index==3:
            EvalValue,x0,direction0 = isshy.calcEvaluationValueIndex3(GameStatus,self.board_backboard, self.NextShape_index)
        elif self.CurrentShape_index==4:
            EvalValue,x0,direction0 = isshy.calcEvaluationValueIndex4(GameStatus,self.board_backboard, self.NextShape_index)
        elif self.CurrentShape_index==5:
            EvalValue,x0,direction0 = isshy.calcEvaluationValueIndex5(GameStatus,self.board_backboard, self.NextShape_index)
        elif self.CurrentShape_index==6:
            EvalValue,x0,direction0 = isshy.calcEvaluationValueIndex6(GameStatus,self.board_backboard, self.NextShape_index)
        elif self.CurrentShape_index==7:
            EvalValue,x0,direction0 = isshy.calcEvaluationValueIndex7(GameStatus,self.board_backboard, self.NextShape_index)
        if EvalValue > 0 :
            #strategy = (direction0,x0,1,self.board_data_height-1)
            strategy = (direction0,x0,1,1)
            if (self.MYDEBUG) : print("<<< isshy-you:(EvalValue,shape,strategy(dir,x,y_ope,y_mov))=(",EvalValue,self.CurrentShape_index,strategy,")")
            #LatestEvalValue = EvalValue
            LatestEvalValue = 19
        else:
            if (self.MYDEBUG) : print("<<< isshy-you:GiveUp")

        if LatestEvalValue < 19:
            # sample code
            # search with current block Shape
            for direction0 in CurrentShapeDirectionRange:
                # search with x range
                x0Min, x0Max = self.getSearchXRange(self.CurrentShape_class, direction0)
                for x0 in range(x0Min, x0Max):
                    # get board data, as if dropdown block
                    board = self.getBoard(self.board_backboard, self.CurrentShape_class, direction0, x0)

                    # evaluate board
                    EvalValue = self.calcEvaluationValueSample(board)
                    # update best move
                    if EvalValue > LatestEvalValue:
                        if (self.MYDEBUG) : print(">>> SAMPLE   :(EvalValue,index,strategy(dir,x,y_ope,y_mov))=(",EvalValue,self.CurrentShape_index,(direction0, x0, 1, 1),")")
                        strategy = (direction0, x0, 1, 1)
                        LatestEvalValue = EvalValue

        # search best nextMove <--

        #print("!!! debug    :(EvalValue,index,strategy(dir,x,y_ope,y_mov))=( ",LatestEvalValue,self.CurrentShape_index,strategy,")")
        processtime = datetime.now()-t1
        print("=== processing time ===(", processtime,")")
        nextMove["strategy"]["direction"] = strategy[0]
        nextMove["strategy"]["x"] = strategy[1]
        nextMove["strategy"]["y_operation"] = strategy[2]
        nextMove["strategy"]["y_moveblocknum"] = strategy[3]
        print("=== nextMove:",nextMove)
        return nextMove

        
    def getSearchXRange(self, Shape_class, direction):
        #
        # get x range from shape direction.
        #
        minX, maxX, _, _ = Shape_class.getBoundingOffsets(direction) # get shape x offsets[minX,maxX] as relative value.
        xMin = -1 * minX
        xMax = self.board_data_width - maxX
        return xMin, xMax

    def getShapeCoordArray(self, Shape_class, direction, x, y):
        #
        # get coordinate array by given shape.
        #
        coordArray = Shape_class.getCoords(direction, x, y) # get array from shape direction, x, y.
        return coordArray

    def getBoard(self, board_backboard, Shape_class, direction, x):
        # 
        # get new board.
        #
        # copy backboard data to make new board.
        # if not, original backboard data will be updated later.
        board = copy.deepcopy(board_backboard)
        _board = self.dropDown(board, Shape_class, direction, x)
        return _board

    def dropDown(self, board, Shape_class, direction, x):
        # 
        # internal function of getBoard.
        # -- drop down the shape on the board.
        # 
        dy = self.board_data_height - 1
        coordArray = self.getShapeCoordArray(Shape_class, direction, x, 0)
        # update dy
        for _x, _y in coordArray:
            _yy = 0
            while _yy + _y < self.board_data_height and (_yy + _y < 0 or board[(_y + _yy) * self.board_data_width + _x] == self.ShapeNone_index):
                _yy += 1
            _yy -= 1
            if _yy < dy:
                dy = _yy
        # get new board
        _board = self.dropDownWithDy(board, Shape_class, direction, x, dy)
        return _board

    def dropDownWithDy(self, board, Shape_class, direction, x, dy):
        #
        # internal function of dropDown.
        #
        _board = board
        coordArray = self.getShapeCoordArray(Shape_class, direction, x, 0)
        for _x, _y in coordArray:
            _board[(_y + dy) * self.board_data_width + _x] = Shape_class.shape
        return _board

    def calcEvaluationValueSample(self, board):
        #
        # sample function of evaluate board.
        #
        width = self.board_data_width
        height = self.board_data_height

        # evaluation paramters
        ## lines to be removed
        fullLines = 0
        ## number of holes or blocks in the line.
        nHoles, nIsolatedBlocks = 0, 0
        ## absolute differencial value of MaxY
        absDy = 0
        ## how blocks are accumlated
        BlockMaxY = [0] * width
        holeCandidates = [0] * width
        holeConfirm = [0] * width

        ### check board
        # each y line
        for y in range(height - 1, 0, -1):
            hasHole = False
            hasBlock = False
            # each x line
            for x in range(width):
                ## check if hole or block..
                if board[y * self.board_data_width + x] == self.ShapeNone_index:
                    # hole
                    hasHole = True
                    holeCandidates[x] += 1  # just candidates in each column..
                else:
                    # block
                    hasBlock = True
                    BlockMaxY[x] = height - y                # update blockMaxY
                    if holeCandidates[x] > 0:
                        holeConfirm[x] += holeCandidates[x]  # update number of holes in target column..
                        holeCandidates[x] = 0                # reset
                    if holeConfirm[x] > 0:
                        nIsolatedBlocks += 1                 # update number of isolated blocks

            if hasBlock == True and hasHole == False:
                # filled with block
                fullLines += 1
            elif hasBlock == True and hasHole == True:
                # do nothing
                pass
            elif hasBlock == False:
                # no block line (and ofcourse no hole)
                pass

        # nHoles
        for x in holeConfirm:
            nHoles += abs(x)

        ### absolute differencial value of MaxY
        BlockMaxDy = []
        for i in range(len(BlockMaxY) - 1):
            val = BlockMaxY[i] - BlockMaxY[i+1]
            BlockMaxDy += [val]
        for x in BlockMaxDy:
            absDy += abs(x)

        #### maxDy
        #maxDy = max(BlockMaxY) - min(BlockMaxY)
        #### maxHeight
        #maxHeight = max(BlockMaxY) - fullLines

        ## statistical data
        #### stdY
        #if len(BlockMaxY) <= 0:
        #    stdY = 0
        #else:
        #    stdY = math.sqrt(sum([y ** 2 for y in BlockMaxY]) / len(BlockMaxY) - (sum(BlockMaxY) / len(BlockMaxY)) ** 2)
        #### stdDY
        #if len(BlockMaxDy) <= 0:
        #    stdDY = 0
        #else:
        #    stdDY = math.sqrt(sum([y ** 2 for y in BlockMaxDy]) / len(BlockMaxDy) - (sum(BlockMaxDy) / len(BlockMaxDy)) ** 2)


        # calc Evaluation Value
        score = 0
        score = score + fullLines * 10.0           # try to delete line 
        score = score - nHoles * 1.0               # try not to make hole
        #score = score - nHoles * 0.0               # try not to make hole
        score = score - nIsolatedBlocks * 1.0      # try not to make isolated block
        score = score - absDy * 1.0                # try to put block smoothly
        #score = score - maxDy * 0.3                # maxDy
        #score = score - maxHeight * 5              # maxHeight
        #score = score - stdY * 1.0                 # statistical data
        #score = score - stdDY * 0.01               # statistical data

        #print(score, fullLines, nHoles, nIsolatedBlocks, maxHeight, stdY, stdDY, absDy, BlockMaxY)
        #print(">>>>>>>>>>(score,fullLines,nHoles,nIsoLateBlocks,absDy,BlockMaxY)=(",score, fullLines, nHoles, nIsolatedBlocks, absDy, BlockMaxY,")")
        return score

BLOCK_CONTROLLER = Block_Controller()
isshy=lib_tetris_isshy.lib_tetris()

