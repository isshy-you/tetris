#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime
import pprint
import copy
import random

from numpy import iinfo

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

        t1 = datetime.now()
        DEBUG = 1
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

        # add additional code by isshy-you
        if self.CurrentShape_index==1:
            EvalValue,x0,direction0 = self.calcEvaluationValueIndex1(self.board_backboard, self.NextShape_index)
        elif self.CurrentShape_index==2:
            EvalValue,x0,direction0 = self.calcEvaluationValueIndex2(self.board_backboard, self.NextShape_index)
        elif self.CurrentShape_index==3:
            EvalValue,x0,direction0 = self.calcEvaluationValueIndex3(self.board_backboard, self.NextShape_index)
        elif self.CurrentShape_index==4:
            EvalValue,x0,direction0 = self.calcEvaluationValueIndex4(self.board_backboard, self.NextShape_index)
        elif self.CurrentShape_index==5:
            EvalValue,x0,direction0 = self.calcEvaluationValueIndex5(self.board_backboard, self.NextShape_index)
        elif self.CurrentShape_index==6:
            EvalValue,x0,direction0 = self.calcEvaluationValueIndex6(self.board_backboard, self.NextShape_index)
        elif self.CurrentShape_index==7:
            EvalValue,x0,direction0 = self.calcEvaluationValueIndex7(self.board_backboard, self.NextShape_index)
        if EvalValue > 0 :
            strategy = (direction0,x0,1,1)
            if DEBUG == 1 : print("<<< isshy-you:(EvalValue,shape,strategy(dir,x,y_ope,y_mov))=(",EvalValue,self.CurrentShape_index,strategy,")")
            #LatestEvalValue = EvalValue
            LatestEvalValue = 19
        else:
            if DEBUG == 1 : print("<<< isshy-you:GiveUp")

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
                    if DEBUG == 1 : print(">>> SAMPLE   :(EvalValue,index,strategy(dir,x,y_ope,y_mov))=(",EvalValue,self.CurrentShape_index,(direction0, x0, 1, 1),")")
                    strategy = (direction0, x0, 1, 1)
                    LatestEvalValue = EvalValue

        # search best nextMove <--

        #print("!!! debug    :(EvalValue,index,strategy(dir,x,y_ope,y_mov))=( ",LatestEvalValue,self.CurrentShape_index,strategy,")")
        print("=== processing time ===(", datetime.now() - t1,")")
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

    def makehorizontalorder(self):
        width = self.board_data_width #width=10
        height = self.board_data_height #height=22
        order = list(range(width))
        for ii in range(0,width,1):
            if (int(ii/2))==(ii/2) :
                order[ii] = int(ii/2)
            else:
                order[ii] = width-1-int(ii/2)
        return(order)


    def checkupper(self,board,xpos,ypos):
        width = self.board_data_width #width=10
        height = self.board_data_height #height=22
        block=0
        for yy in range(ypos,0,-1):
            if board[(yy) * width + (xpos)] != 0:
                block = 1
                break
        return(block)

    def counthole(self,board,xpos,ypos):
        width = self.board_data_width #width=10
        height = self.board_data_height #height=22
        hole=0
        if (height-1<ypos+1): return(0)
        for yy in range(height-1,ypos,-1):
            #if (yy < height):
            if board[(yy) * width + (xpos)] == 0:
                hole += 1
            else:
                hole = 0
        return(hole)

    def maxblockheight(self,board):
        width = self.board_data_width #width=10
        height = self.board_data_height #height=22
        for yy in range(height-1,0,-1):
            for xx in range(0,width,1):
                if board[yy*width+xx]!=0:
                    height = yy
        return(height)

    #type-I
    def calcEvaluationValueIndex1(self,board,nextindex):
        DEBUG = 0
        if DEBUG==1: print('block_type-I')
        direction = 0
        width = self.board_data_width #width=10
        height = self.board_data_height #height=22
        order = self.makehorizontalorder()
        blockheight = self.maxblockheight(board)

        dic_dir0 = {0x0f:8,0x07:7,0x03:5,0x01:2}
        dic_dir1 = {          0x0001:1,0x0010:1,0x0011:1
                    ,0x0100:1,0x0101:1,0x0110:1,0x0111:1
                    ,0x1000:1,0x1001:1,0x1010:1,0x1011:1
                    ,0x1100:1,0x1101:1,0x1110:1,0x1111:8
                    }
        dic_dir2 = {0xf0:8,0x70:7,0x30:5,0x10:2}
        dic_dir3 = {0xf0f:9,0xf07:6,0x70f:6,0xf03:6,0x30f:6}

        dic_alix = [0,2,1,1]
        dic_aliy = [1,0,1,1]
        dic_widx = [1,4,1,1]
        dic_widy = [4,1,4,4]

        dic_dir = [0,1,0,0]

        x_start = 0
        x_end = width-1
        x_step = 1
        point = [-1,-1,-1,-1] #point,x,y,direction
        for y in range(height - 3, blockheight ,-1):
            for x in order:
                pat4 = self.calcBoardPat(self.board_backboard,x,y)
                pat3 = pat4 >> 4
                pat2 = pat4 >> 8
                nopoint = 0
                hole = 0
                direction=0
                #check over 4 hole
                if self.checkupper(board,x+dic_alix[direction],y)!=1 :
                    hole=self.counthole(board,x,y)
                    if (hole >= 4):
                        if DEBUG == 1 : print("### FOUND THE HOLE(",hole,")",x,y,format(pat4,'04x'))
                        point=[10,x,y,direction]
                if (x<(width-1))and((pat2) in dic_dir0):
                    getpoint = dic_dir0[pat2]
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        #print('x,y,point,getpoint0=',x,y,point,getpoint)
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if DEBUG ==1 : print('### BLOCKED BY UPPER at ',xx,y)
                                nopoint = 1
                                break
                            #hole=self.counthole(board,xx,y)
                            #if (hole <=1):
                            #    if DEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",xx,y,format(pat4,'04x'))
                            #    nopoint = 1
                            #    break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if DEBUG == 1 : print("dir0=",format(pat2,'02x'),"point=",point)
                            if DEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=1
                if  (x<(width-3))and((pat4) in dic_dir1):
                    getpoint = dic_dir1[pat4]
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        #print('x,y,point,getpoint1=',x,y,point,getpoint)
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if DEBUG ==1 : print('### BLOCKED BY UPPER at ',xx,y)
                                nopoint = 1
                                break
                            hole=self.counthole(board,xx,y)
                            if (hole >=1)and(hole <=4) :
                                if DEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",xx,y,format(pat4,'04x'))
                                nopoint = 1
                                break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if DEBUG == 1 : print("dir1=",format(pat4,'04x'),"point=",point)
                            if DEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=2
                if (x>0) and ((pat2) in dic_dir2):
                    getpoint = dic_dir2[pat2]
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        #print('x,y,point,getpoint2=',x,y,point,getpoint)
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if DEBUG ==1 : print('### BLOCKED BY UPPER at ',xx,y)
                                nopoint = 1
                                break
                            #hole=self.counthole(board,xx,y)
                            #if (hole <=1):
                            #    if DEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",xx,y,format(pat4,'04x'))
                            #    nopoint = 1
                            #    break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if DEBUG == 1 : print("dir2=",format(pat2,'02x'),"point=",point)
                            if DEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=3
                if (x<(width-1))and((pat3) in dic_dir3):
                    getpoint = dic_dir3[pat3]
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        #print('x,y,point,getpoint3=',x,y,point,getpoint)
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if DEBUG ==1 : print('### BLOCKED BY UPPER at ',xx,y)
                                nopoint = 1
                                break
                            #hole=self.counthole(board,xx,y)
                            #if (hole <=1) :
                            #    if DEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",xx,y,format(pat4,'04x'))
                            #    nopoint = 1
                            #    break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if DEBUG == 1 : print("dir3=",format(pat3,'03x'),"point=",point)
                            if DEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
        return point[0],point[1],point[3]
   
    #type-L
    def calcEvaluationValueIndex2(self,board,nextindex):
        DEBUG = 1
        if DEBUG==1: print('block_type-L')
        direction = 0
        width = self.board_data_width #width=10
        height = self.board_data_height #height=22
        blockheight = self.maxblockheight(board)

        dic_dir0 = {0x11:7}
        dic_dir1 = {0x133:8,\
                    0x123:8,0x132:8,0x122:8,0x131:2}
        dic_dir2 = {0x71:9,0x41:9,0x51:9,0x61:9,0x70:7,0x30:2,0x20:2,\
                    0xf1:2,0x81:2,0x91:2,0xa1:2,0xb1:2,0xc1:2,0xd1:2,0xe1:2} #add 210727a
        dic_dir3 = {0x111:8}

        order = self.makehorizontalorder()
        dic_alix = [0,1,1,1]
        dic_aliy = [1,1,1,1]
        dic_widx = [2,3,2,3]
        dic_widy = [3,2,3,2]

        dic_dir = [0,1,2,3]

        x_start = 0
        x_end = width-1
        x_step = 1
        point = [-1,-1,-1,-1] #point,x,y,direction
        for y in range(height - 3, blockheight ,-1):
            for x in order:
                pat4 = self.calcBoardPat(self.board_backboard,x,y)
                pat3 = pat4 >> 4
                pat2 = pat4 >> 8
                nopoint = 0
                hole = 0
                direction=0
                if (x<(width-1))and((pat2) in dic_dir0):
                    getpoint = dic_dir0[pat2]
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        #print('x,y,point,getpoint0=',x,y,point,getpoint)
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if DEBUG ==1 : print('### BLOCKED BY UPPER at ',xx,y)
                                nopoint = 1
                                break
                            hole=self.counthole(board,xx,y)
                            if (hole <=1):
                                if DEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",xx,y,format(pat4,'04x'))
                                nopoint = 1
                                break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if DEBUG == 1 : print("dir0=",format(pat2,'02x'),"point=",point)
                            if DEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=1
                if (x<(width-2))and((pat3) in dic_dir1):
                    getpoint = dic_dir1[pat3]
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if DEBUG ==1 : print('### BLOCKED BY UPPER at ',xx,y)
                                nopoint = 1
                                break
                            hole=self.counthole(board,xx,y)
                            if (hole >=1)and(hole <=4) :
                                if DEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",xx,y,format(pat4,'04x'))
                                nopoint = 1
                                break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if DEBUG == 1 : print("dir1=",format(pat4,'04x'),"point=",point)
                            if DEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=2
                if (x<(width-1))and((pat2) in dic_dir2):
                    getpoint = dic_dir2[pat2]
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        #print('x,y,point,getpoint1=',x,y,point,getpoint)
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if DEBUG ==1 : print('### BLOCKED BY UPPER at ',xx,y)
                                nopoint = 1
                                break
                            hole=self.counthole(board,xx,y)
                            if (hole >=1)and(hole <=4) :
                                if DEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",xx,y,format(pat4,'04x'))
                                nopoint = 1
                                break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if DEBUG == 1 : print("dir1=",format(pat4,'04x'),"point=",point)
                            if DEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=3
                if (x<(width-1))and((pat3) in dic_dir3):
                    getpoint = dic_dir3[pat3]
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        #print('x,y,point,getpoint1=',x,y,point,getpoint)
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if DEBUG ==1 : print('### BLOCKED BY UPPER at ',xx,y)
                                nopoint = 1
                                break
                            hole=self.counthole(board,xx,y)
                            if (hole >=1)and(hole <=4) :
                                if DEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",xx,y,format(pat4,'04x'))
                                nopoint = 1
                                break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if DEBUG == 1 : print("dir1=",format(pat4,'04x'),"point=",point)
                            if DEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
        return point[0],point[1],point[3]

    #type-J
    def calcEvaluationValueIndex3(self,board,nextindex):
        DEBUG = 1
        if DEBUG==1: print('block_type-J')
        direction = 0
        width = self.board_data_width #width=10
        height = self.board_data_height #height=22
        blockheight = self.maxblockheight(board)

        dic_dir0 = {0x11:7}
        dic_dir1 = {0x111:8}
        dic_dir2 = {0x17:9,0x14:9,0x15:9,0x16:9,0x07:7,0x03:2,0x02:2,\
                    0x1f:2,0x18:2,0x19:2,0x1a:2,0x1b:2,0x1c:2,0x1d:2,0x1e:2} #add 210727a
        dic_dir3 = {0x331:8,\
                    0x321:8,0x231:8,0x221:8,0x131:2}

        order = self.makehorizontalorder()
        dic_alix = [1,1,0,1]
        dic_aliy = [1,1,1,0]
        dic_widx = [2,3,2,3]
        dic_widy = [3,2,3,2]

        dic_dir = [0,1,2,3]

        x_start = 0
        x_end = width-1
        x_step = 1
        point = [-1,-1,-1,-1] #point,x,y,direction
        for y in range(height - 3, blockheight ,-1):
            for x in order:
                pat4 = self.calcBoardPat(self.board_backboard,x,y)
                pat3 = pat4 >> 4
                pat2 = pat4 >> 8
                nopoint = 0
                hole = 0
                direction=0
                if (x<(width-1))and((pat2) in dic_dir0):
                    getpoint = dic_dir0[pat2]
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        #print('x,y,point,getpoint0=',x,y,point,getpoint)
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if DEBUG ==1 : print('### BLOCKED BY UPPER at ',xx,y)
                                nopoint = 1
                                break
                            hole=self.counthole(board,xx,y)
                            if (hole <=1):
                                if DEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",xx,y,format(pat4,'04x'))
                                nopoint = 1
                                break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if DEBUG == 1 : print("dir0=",format(pat2,'02x'),"point=",point)
                            if DEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=1
                if (x<(width-2))and((pat3) in dic_dir1):
                    getpoint = dic_dir1[pat3]
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if DEBUG ==1 : print('### BLOCKED BY UPPER at ',xx,y)
                                nopoint = 1
                                break
                            hole=self.counthole(board,xx,y)
                            if (hole >=1)and(hole <=4) :
                                if DEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",xx,y,format(pat4,'04x'))
                                nopoint = 1
                                break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if DEBUG == 1 : print("dir1=",format(pat4,'04x'),"point=",point)
                            if DEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=2
                if (x<(width-1))and((pat2) in dic_dir2):
                    getpoint = dic_dir2[pat2]
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        #print('x,y,point,getpoint1=',x,y,point,getpoint)
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if DEBUG ==1 : print('### BLOCKED BY UPPER at ',xx,y)
                                nopoint = 1
                                break
                            hole=self.counthole(board,xx,y)
                            if (hole >=1)and(hole <=4) :
                                if DEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",xx,y,format(pat4,'04x'))
                                nopoint = 1
                                break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if DEBUG == 1 : print("dir1=",format(pat4,'04x'),"point=",point)
                            if DEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=3
                if (x<(width-1))and((pat3) in dic_dir3):
                    getpoint = dic_dir3[pat3]
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        #print('x,y,point,getpoint1=',x,y,point,getpoint)
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if DEBUG ==1 : print('### BLOCKED BY UPPER at ',xx,y)
                                nopoint = 1
                                break
                            hole=self.counthole(board,xx,y)
                            if (hole >=1)and(hole <=4) :
                                if DEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",xx,y,format(pat4,'04x'))
                                nopoint = 1
                                break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if DEBUG == 1 : print("dir1=",format(pat4,'04x'),"point=",point)
                            if DEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
        return point[0],point[1],point[3]

    #type-T
    def calcEvaluationValueIndex4(self,board,nextindex):
        DEBUG = 1
        if DEBUG==1: print('block_type-T')
        direction = 0
        width = self.board_data_width #width=10
        height = self.board_data_height #height=22
        blockheight = self.maxblockheight(board)

        dic_dir0 = {0x13:6,0x12:6}
        dic_dir1 = {0x313:7,0x213:7,0x312:7,0x212:7}
        dic_dir2 = {0x31:6,0x21:6}
        dic_dir3 = {0x111:9}

        order = self.makehorizontalorder()
        dic_alix = [1,1,0,1]
        dic_aliy = [1,1,1,0]
        dic_widx = [2,3,2,3]
        dic_widy = [3,2,3,2]

        dic_dir = [0,1,2,3]

        x_start = 0
        x_end = width-1
        x_step = 1
        point = [-1,-1,-1,-1] #point,x,y,direction
        for y in range(height - 3, blockheight ,-1):
            for x in order:
                pat4 = self.calcBoardPat(self.board_backboard,x,y)
                pat3 = pat4 >> 4
                pat2 = pat4 >> 8
                nopoint = 0
                hole = 0
                direction=0
                if (x<(width-1))and((pat2) in dic_dir0):
                    getpoint = dic_dir0[pat2]
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        #print('x,y,point,getpoint0=',x,y,point,getpoint)
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if DEBUG ==1 : print('### BLOCKED BY UPPER at ',xx,y)
                                nopoint = 1
                                break
                            hole=self.counthole(board,xx,y)
                            if (hole <=1):
                                if DEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",xx,y,format(pat4,'04x'))
                                nopoint = 1
                                break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if DEBUG == 1 : print("dir0=",format(pat2,'02x'),"point=",point)
                            if DEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=1
                if (x<(width-2))and((pat3) in dic_dir1):
                    getpoint = dic_dir1[pat3]
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if DEBUG ==1 : print('### BLOCKED BY UPPER at ',xx,y)
                                nopoint = 1
                                break
                            hole=self.counthole(board,xx,y)
                            if (hole >=1)and(hole <=4) :
                                if DEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",xx,y,format(pat4,'04x'))
                                nopoint = 1
                                break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if DEBUG == 1 : print("dir1=",format(pat4,'04x'),"point=",point)
                            if DEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=2
                if (x<(width-1))and((pat2) in dic_dir2):
                    getpoint = dic_dir2[pat2]
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        #print('x,y,point,getpoint1=',x,y,point,getpoint)
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if DEBUG ==1 : print('### BLOCKED BY UPPER at ',xx,y)
                                nopoint = 1
                                break
                            hole=self.counthole(board,xx,y)
                            if (hole >=1)and(hole <=4) :
                                if DEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",xx,y,format(pat4,'04x'))
                                nopoint = 1
                                break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if DEBUG == 1 : print("dir1=",format(pat4,'04x'),"point=",point)
                            if DEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=3
                if (x<(width-1))and((pat3) in dic_dir3):
                    getpoint = dic_dir3[pat3]
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        #print('x,y,point,getpoint1=',x,y,point,getpoint)
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if DEBUG ==1 : print('### BLOCKED BY UPPER at ',xx,y)
                                nopoint = 1
                                break
                            hole=self.counthole(board,xx,y)
                            if (hole >=1)and(hole <=4) :
                                if DEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",xx,y,format(pat4,'04x'))
                                nopoint = 1
                                break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if DEBUG == 1 : print("dir1=",format(pat4,'04x'),"point=",point)
                            if DEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
        return point[0],point[1],point[3]

    #type-O
    def calcEvaluationValueIndex5(self,board,nextindex):
        DEBUG = 1
        if DEBUG==1: print('block_type-O')
        direction = 0
        width = self.board_data_width #width=10
        height = self.board_data_height #height=22
        blockheight = self.maxblockheight(board)

        dic_dir0 = {0x11:7,\
                    0x13:4,0x31:4,0x12:4,0x21:4,\
                    0x17:3,0x14:3,0x16:3,0x71:3,0x41:3,0x61:3,\
                    0x10:2,0x01:2}
        dic_dir1 = {0x11f:7,0x118:7,0x119:7,0x11a:7,0x11b:7,0x11c:7,0x11d:7,0x11e:7,\
                    0x117:7,0x116:7,0x115:7,0x114:7}
        dic_dir2 = {0xf11:7,0xe11:7,0xd11:7,0xc11:7,0xb11:7,0xa11:7,0x911:7,0x811:7,\
                    0x711:7,0x611:7,0x511:7,0x411:7}

        order = self.makehorizontalorder()
        dic_alix = [0,0,1,0]
        dic_aliy = [1,1,1,0]
        dic_widx = [2,2,2,0]
        dic_widy = [2,2,2,0]

        dic_dir = [0,1,2,3]

        x_start = 0
        x_end = width-1
        x_step = 1
        point = [-1,-1,-1,-1] #point,x,y,direction
        for y in range(height - 3, blockheight ,-1):
            for x in order:
                pat4 = self.calcBoardPat(self.board_backboard,x,y)
                pat3 = pat4 >> 4
                pat2 = pat4 >> 8
                nopoint = 0
                hole = 0
                direction=0
                if (x<(width-1))and((pat2) in dic_dir0):
                    getpoint = dic_dir0[pat2]
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        #print('x,y,point,getpoint0=',x,y,point,getpoint)
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if DEBUG ==1 : print('### BLOCKED BY UPPER at ',xx,y)
                                nopoint = 1
                                break
                            hole=self.counthole(board,xx,y)
                            if (hole <=1):
                                if DEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",xx,y,format(pat4,'04x'))
                                nopoint = 1
                                break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if DEBUG == 1 : print("dir0=",format(pat2,'02x'),"point=",point)
                            if DEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=1
                if (x<(width-2))and((pat3) in dic_dir1):
                    getpoint = dic_dir1[pat3]
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if DEBUG ==1 : print('### BLOCKED BY UPPER at ',xx,y)
                                nopoint = 1
                                break
                            hole=self.counthole(board,xx,y)
                            if (hole >=1)and(hole <=4) :
                                if DEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",xx,y,format(pat4,'04x'))
                                nopoint = 1
                                break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if DEBUG == 1 : print("dir1=",format(pat4,'04x'),"point=",point)
                            if DEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=2
                if (x<(width-1))and((pat3) in dic_dir2):
                    getpoint = dic_dir2[pat3]
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        #print('x,y,point,getpoint1=',x,y,point,getpoint)
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if DEBUG ==1 : print('### BLOCKED BY UPPER at ',xx,y)
                                nopoint = 1
                                break
                            hole=self.counthole(board,xx,y)
                            if (hole >=1)and(hole <=4) :
                                if DEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",xx,y,format(pat4,'04x'))
                                nopoint = 1
                                break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if DEBUG == 1 : print("dir1=",format(pat4,'04x'),"point=",point)
                            if DEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
        return point[0],point[1],point[3]

    #type-S
    def calcEvaluationValueIndex6(self,board,nextindex):
        DEBUG = 1
        if DEBUG==1: print('block_type-S')
        direction = 0
        width = self.board_data_width #width=10
        height = self.board_data_height #height=22
        blockheight = self.maxblockheight(board)

        dic_dir0 = {0x113:7,0x112:7}
        dic_dir1 = {0x31:7,0x21:7,0x11:2,0x10:5} #add 210728:0120
    
        order = self.makehorizontalorder()
        dic_alix = [1,1,0,0]
        dic_aliy = [1,1,0,0]
        dic_widx = [3,2,0,0]
        dic_widy = [2,3,0,0]

        dic_dir = [0,1,2,3]

        x_start = 0
        x_end = width-1
        x_step = 1
        point = [-1,-1,-1,-1] #point,x,y,direction
        for y in range(height - 3, blockheight ,-1):
            for x in order:
                pat4 = self.calcBoardPat(self.board_backboard,x,y)
                pat3 = pat4 >> 4
                pat2 = pat4 >> 8
                nopoint = 0
                hole = 0
                direction=0
                if (x<(width-1))and((pat3) in dic_dir0):
                    getpoint = dic_dir0[pat3]
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        #print('x,y,point,getpoint0=',x,y,point,getpoint)
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if DEBUG ==1 : print('### BLOCKED BY UPPER at ',xx,y)
                                nopoint = 1
                                break
                            hole=self.counthole(board,xx,y)
                            if (hole <=1):
                                if DEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",xx,y,format(pat4,'04x'))
                                nopoint = 1
                                break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if DEBUG == 1 : print("dir0=",format(pat2,'02x'),"point=",point)
                            if DEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=1
                if (x<(width-2))and((pat2) in dic_dir1):
                    getpoint = dic_dir1[pat2]
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if DEBUG ==1 : print('### BLOCKED BY UPPER at ',xx,y)
                                nopoint = 1
                                break
                            hole=self.counthole(board,xx,y)
                            if (hole >=1)and(hole <=4) :
                                if DEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",xx,y,format(pat4,'04x'))
                                nopoint = 1
                                break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if DEBUG == 1 : print("dir1=",format(pat4,'04x'),"point=",point)
                            if DEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
        return point[0],point[1],point[3]

    #type-Z
    def calcEvaluationValueIndex7(self,board,nextindex):
        DEBUG = 1
        if DEBUG==1: print('block_type-Z')
        direction = 0
        width = self.board_data_width #width=10
        height = self.board_data_height #height=22
        blockheight = self.maxblockheight(board)

        dic_dir0 = {0x311:7,0x211:7}
        dic_dir1 = {0x13:7,0x12:7,0x11:2,0x01:5}#add 210728:0119

        order = self.makehorizontalorder()
        dic_alix = [1,1,0,0]
        dic_aliy = [1,1,0,0]
        dic_widx = [3,2,0,0]
        dic_widy = [2,3,0,0]

        dic_dir = [0,1,2,3]

        x_start = 0
        x_end = width-1
        x_step = 1
        point = [-1,-1,-1,-1] #point,x,y,direction
        for y in range(height - 3, blockheight ,-1):
            for x in order:
                pat4 = self.calcBoardPat(self.board_backboard,x,y)
                pat3 = pat4 >> 4
                pat2 = pat4 >> 8
                nopoint = 0
                hole = 0
                direction=0
                if (x<(width-1))and((pat3) in dic_dir0):
                    getpoint = dic_dir0[pat3]
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        #print('x,y,point,getpoint0=',x,y,point,getpoint)
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if DEBUG ==1 : print('### BLOCKED BY UPPER at ',xx,y)
                                nopoint = 1
                                break
                            hole=self.counthole(board,xx,y)
                            if (hole <=1):
                                if DEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",xx,y,format(pat4,'04x'))
                                nopoint = 1
                                break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if DEBUG == 1 : print("dir0=",format(pat2,'02x'),"point=",point)
                            if DEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=1
                if (x<(width-2))and((pat2) in dic_dir1):
                    getpoint = dic_dir1[pat2]
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if DEBUG ==1 : print('### BLOCKED BY UPPER at ',xx,y)
                                nopoint = 1
                                break
                            hole=self.counthole(board,xx,y)
                            if (hole >=1)and(hole <=4) :
                                if DEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",xx,y,format(pat4,'04x'))
                                nopoint = 1
                                break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if DEBUG == 1 : print("dir1=",format(pat4,'04x'),"point=",point)
                            if DEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
        return point[0],point[1],point[3]

    def calcBoardPat(self,board,x,y):

        width = self.board_data_width #width=10
        height = self.board_data_height #height=22

        pat0=0
        if x > (width-1) :
            pat0=15 #right
        else:
            if board[y * width + x]!=0:
                pat0 += 8
            if board[(y+1) * width + x]!=0:
                    pat0 += 4
            if board[(y+2) * width + x]!=0:
                    pat0 += 2
            if  y > (height-4):
                    pat0 += 1 #bottom
            elif board[(y+3) * width + x]!=0 :
                    pat0 += 1

        pat1=0
        if x > (width-2) :
            pat1=15 #right
        else:
            if board[y * width + (x + 1)]!=0:
                pat1 += 8
            if board[(y+1) * width + (x + 1)]!=0:
                pat1 += 4
            if board[(y+2) * width + (x + 1)]!=0:
                pat1 += 2
            if  y > (height-4):
                pat1 += 1 #bottom
            elif board[(y+3) * width + (x + 1)]!=0 :
                pat1 += 1

        pat2=0
        if x > (width-3) :
            pat2=15 #right
        else:
            if board[(y+0) * width + (x + 2)]!=0:
                pat2 += 8
            if board[(y+1) * width + (x + 2)]!=0:
                pat2 += 4
            if board[(y+2) * width + (x + 2)]!=0:
                pat2 += 2
            if  y > (height-4):
                pat2 += 1 #bottom
            elif board[(y+3) * width + (x + 2)]!=0 :
                pat2 += 1
                #print("pat2+=1:::",pat2)

        pat3=0
        if x > (width-4) :
            pat3=15 #right
        else:
            if  board[(y+0) * width + (x + 3)]!=0:
                pat3 += 8
            if  board[(y+1) * width + (x + 3)]!=0:
                pat3 += 4
            if  board[(y+2) * width + (x + 3)]!=0:
                pat3 += 2
            if  y > (height-4):
                pat3 += 1 #bottom
            elif board[(y+3) * width + (x + 3)]!=0 :
                pat3 += 1

        pat = pat0*4096+pat1*256+pat2*16+pat3
        #DEBUG
        #print("(index,x,y,pat)=(",self.CurrentShape_index,x,y,format(pat,'04x'),")")

        return pat

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

