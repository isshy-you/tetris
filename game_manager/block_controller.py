#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime
import pprint
import copy
import random

from numpy import iinfo

class Block_Controller(object):

    MYDEBUG = 1
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
            #strategy = (direction0,x0,1,self.board_data_height-1)
            strategy = (direction0,x0,1,1)
            if self.MYDEBUG == 1 : print("<<< isshy-you:(EvalValue,shape,strategy(dir,x,y_ope,y_mov))=(",EvalValue,self.CurrentShape_index,strategy,")")
            #LatestEvalValue = EvalValue
            LatestEvalValue = 19
        else:
            if self.MYDEBUG == 1 : print("<<< isshy-you:GiveUp")

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
                        if self.MYDEBUG == 1 : print(">>> SAMPLE   :(EvalValue,index,strategy(dir,x,y_ope,y_mov))=(",EvalValue,self.CurrentShape_index,(direction0, x0, 1, 1),")")
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

    def makehorizontalorder(self,maxheight):
        if maxheight < 10 :
            return(self.makehorizontalorder3())
        else :
            return(self.makehorizontalorder4())

    def makehorizontalorder1(self): #[0,1,2,3,4,5,6,6,8,9]
        #width = self.board_data_width #width=10
        #height = self.board_data_height #height=22
        #order = list(range(width))
        #for ii in range(0,width,1):
        #    order[ii]=ii
        return([0,1,2,3,4,5,6,7,8,9])

    def makehorizontalorder2(self): #[9,8,7,6,5,4,3,2,1,0]
        #width = self.board_data_width #width=10
        #height = self.board_data_height #height=22
        #order = list(range(width))
        #for ii in range(0,width,1):
        #    order[ii]=width-ii-1
        return([9,8,7,6,5,4,3,2,1,0])

    def makehorizontalorder3(self): #[0,9,1,8,2,7,3,6,4,5]
        width = self.board_data_width #width=10
        height = self.board_data_height #height=22
        order = list(range(width+1))
        for ii in range(0,width+1,1):
            if int(ii/2)==(ii/2) :
                order[ii] = int(ii/2)-1
            else:
                order[ii] = width-1-int(ii/2)
        if (self.MYDEBUG==1):print('order3=',order)
        return(order)

    def makehorizontalorder4(self): #[5,4,6,3,7,2,8,1,9,0]
        width = self.board_data_width #width=10
        height = self.board_data_height #height=22
        order = list(range(width+1))
        for ii in range(0,width+1,1):
            if int(ii/2)==(ii/2) :
                order[width-ii] = int(ii/2)-1
            else:
                order[width-ii] = width-1-int(ii/2)
        if (self.MYDEBUG==1):print('order4=',order)
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
        if (height-1<ypos+3): return(0)
        for yy in range(ypos,height,1):
            #if (yy < height):
            if board[(yy) * width + (xpos)] == 0:
                hole += 1
            else:
                break
        return(hole)

    def maxblockheight(self,board):
        width = self.board_data_width #width=10
        height = self.board_data_height #height=22
        # maxheight=height-4
        # for yy in range(height-1,4,-1):
        #     for xx in range(0,width,1):
        #         if board[yy*width+xx]!=0:
        #             maxheight = yy-4
        for yy in range(0,height,1):
            for xx in range(0,width,1):
                if board[yy*width+xx]!=0:
                    if (self.MYDEBUG==1):print('blockheight=',yy-4)
                    return(yy-4)
                    # if yy > 4 : 
                    #     return(yy-4)
                    # else:
                    #     return(0)
        return(0)

    #type-I
    def calcEvaluationValueIndex1(self,board,nextindex):
        #DEBUG = 1 #OFF
        if self.MYDEBUG == 1: print('block_type-I -> ',nextindex)
        direction = 0
        width = self.board_data_width #width=10
        height = self.board_data_height #height=22
        blockheight = self.maxblockheight(board)
        order = self.makehorizontalorder(blockheight)

        dic_dir0 = {0x0f:8,0x0e:8,0x0d:8,0x0c:8,0x0b:8,0x0a:8,0x09:8,0x08:8
                    ,0x07:7,0x06:7,0x05:7,0x04:7
                    ,0x03:5,0x02:5
                    ,0x01:2,0x00:1}
        dic_dir1 = { 0x3333:8,0x2222:8,0x1111:8
                    # ,0x2333:8,0x3233:8,0x3323:8,0x3332:8
                    # ,0x2233:8,0x2323:8,0x2332:8,0x3232:8,0x3322:8
                    # ,0x2223:8,0x2232:8,0x2322:8,0x3222:8
                    ,0x1333:2,0x3133:2,0x3313:2,0x3331:2
                    ,0x1233:2,0x2133:2,0x2313:2,0x2331:2
                    ,0x1323:2,0x3123:2,0x3213:2,0x3231:2
                    ,0x1332:2,0x3132:2,0x3312:2,0x3321:2
                    ,0x1223:2,0x2123:2,0x2213:2,0x2231:2
                    ,0x1232:2,0x2132:2,0x2312:2,0x2321:2
                    ,0x1322:2,0x3122:2,0x3212:2,0x3221:2
                    ,0x1222:2,0x2122:2,0x2212:2,0x2221:2
                    }
        dic_dir2 = {0xf0:8,0x70:7,0x30:3,0x10:1
                    ,0x80:8,0x90:8,0xa0:8,0xb0:8,0xc0:8,0xd0:8,0xe0:8
                    ,0x60:7,0x50:7,0x4:7
                    ,0x20:3}
        #dic_dir2 = {0xF1:7,0x71:5,0x31:2}
        dic_dir3 = { 0xf0f:9,0xe0f:9,0xd0f:9,0xc0f:9,0xb0f:9,0xa0f:9,0x90f:9,0x80f:9
                    ,0xf0e:9,0xe0e:9,0xd0e:9,0xc0e:9,0xb0e:9,0xa0e:9,0x90e:9,0x80e:9
                    ,0xf0d:9,0xe0d:9,0xd0d:9,0xc0d:9,0xb0d:9,0xa0d:9,0x90d:9,0x80d:9
                    ,0xf0c:9,0xe0c:9,0xd0c:9,0xc0c:9,0xb0c:9,0xa0c:9,0x90c:9,0x80c:9
                    ,0xf0b:9,0xe0b:9,0xd0b:9,0xc0b:9,0xb0b:9,0xa0b:9,0x90b:9,0x80b:9
                    ,0xf0a:9,0xe0a:9,0xd0a:9,0xc0a:9,0xb0a:9,0xa0a:9,0x90a:9,0x80a:9
                    ,0xf09:9,0xe09:9,0xd09:9,0xc09:9,0xb09:9,0xa09:9,0x909:9,0x809:9
                    ,0xf08:9,0xe08:9,0xd08:9,0xc08:9,0xb08:9,0xa08:9,0x908:9,0x808:9
                    ,0xf07:7,0xf06:7,0xf05:7,0xf04:7
                    ,0xe07:7,0xe06:7,0xe05:7,0xe04:7
                    ,0xd07:7,0xd06:7,0xd05:7,0xd04:7
                    ,0xc07:7,0xc06:7,0xc05:7,0xc04:7
                    ,0xb07:7,0xb06:7,0xb05:7,0xb04:7
                    ,0xa07:7,0xa06:7,0xa05:7,0xa04:7
                    ,0x907:7,0x906:7,0x905:7,0x904:7
                    ,0x807:7,0x806:7,0x805:7,0x804:7
                    ,0x70f:7,0x60f:7,0x50f:7,0x40f:7
                    ,0x70e:7,0x60e:7,0x50e:7,0x40e:7
                    ,0x70d:7,0x60d:7,0x50d:7,0x40d:7
                    ,0x70c:7,0x60c:7,0x50c:7,0x40c:7
                    ,0x70b:7,0x60b:7,0x50b:7,0x40b:7
                    ,0x70a:7,0x60a:7,0x50a:7,0x40a:7
                    ,0x709:7,0x609:7,0x509:7,0x409:7
                    ,0x708:7,0x608:7,0x508:7,0x408:7
                    ,0xf03:5,0xe03:5,0xd03:5,0xc03:5,0xb03:5,0xa03:5,0x903:5,0x803:5
                    ,0xf02:5,0xe02:5,0xd02:5,0xc02:5,0xb02:5,0xa02:5,0x902:5,0x802:5
                    ,0x30f:5,0x30e:5,0x30d:5,0x30c:5,0x30b:5,0x30a:5,0x309:5,0x308:5
                    ,0x20f:5,0x20e:5,0x20d:5,0x20c:5,0x20b:5,0x20a:5,0x209:5,0x208:5
                    ,0x707:6,0x706:6,0x705:6,0x704:6
                    ,0x607:6,0x606:6,0x605:6,0x604:6
                    ,0x507:6,0x506:6,0x505:6,0x504:6
                    ,0x407:6,0x406:6,0x405:6,0x404:6
                    ,0x303:3,0x302:3,0x203:3,0x202:3
                    ,0x301:2,0x201:2,0x102:2,0x103:2
                    ,0x101:1,0x100:1,0x001:1}
        #dic_dir3 = {0xf1f:6,0xf17:6,0x71f:6,0x31f:5,0xf13:5}

        dic_alix = [0,2,1,1]
        dic_aliy = [1,0,1,1]
        dic_ofsx = [0,0,1,1]
        dic_widx = [1,4,1,1]
        dic_widy = [4,1,4,4]

        dic_dir = [0,1,0,0]

        x_start = 0
        x_end = width-1
        x_step = 1
        point = [-1,-1,-1,-1] #point,x,y,direction
        for y in range(height - 3,blockheight , -1):
        # for y in range(height - 3, blockheight ,-1):
            for x in order:
                pat4 = self.calcBoardPat(board,x,y)
                pat3 = pat4 >> 4
                pat2 = pat4 >> 8
                nopoint = 0
                hole = 0
                direction=0
                #check over 4 hole
                # if self.checkupper(board,x+dic_alix[direction],y)!=1 :
                #     hole=self.counthole(board,x+dic_alix[direction],y)
                #     if (hole >= 4):
                #         getpoint = 10+hole-4+y*2
                #         if (((point[0]<getpoint))):
                #             if self.MYDEBUG == 1 : print("### FOUND THE HOLE(",hole,")",x,y,format(pat4,'04x'))
                #             point=getpoint,x,y,direction
                #             if self.MYDEBUG == 1 : print("hole=",format(pat4,'04x'),"point=",point)
                if (x<(width))and((pat2) in dic_dir0):
                    # getpoint = dic_dir0[pat2]+y*2+dic_widy[direction]-dic_aliy[direction] #for Lv2
                    getpoint = dic_dir0[pat2]+(y*2) #for Lv2
                    #getpoint = dic_dir0[pat2] #for Lv1
                    if self.MYDEBUG == 1 : print('I(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmin = x + dic_ofsx[direction]
                    xxmax = x + dic_ofsx[direction] + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        #print('x,y,point,getpoint0=',x,y,point,getpoint)
                        for xx in range(xxmin,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if self.MYDEBUG == 1 : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            #hole=self.counthole(board,xx,y)
                            #if (hole <=1):
                            #    if self.MYDEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #    nopoint = 1
                            #    break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if self.MYDEBUG == 1 : print("dir0=",format(pat2,'02x'),"point=",point)
                            # if self.MYDEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=1
                if  (x<(width-3))and((pat4) in dic_dir1):
                    # getpoint = dic_dir1[pat4]+y*2+dic_widy[direction]-dic_aliy[direction]
                    getpoint = dic_dir1[pat4]+(y*2)
                    if self.MYDEBUG == 1 : print('I(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmin = x + dic_ofsx[direction]
                    xxmax = x + dic_ofsx[direction] + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        #print('x,y,point,getpoint1=',x,y,point,getpoint)
                        for xx in range(xxmin,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if self.MYDEBUG == 1 : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            #hole=self.counthole(board,xx,y)
                            #if (hole >=1)and(hole <=4) :
                            #    if self.MYDEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #    getpoint -= hole*1
                            #    if nextindex==1 and hole>=4:
                            #        if self.MYDEBUG == 1 : print("### Next index is I, keep 4-hole. ###")
                            #        nopoint = 1
                            #        break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if self.MYDEBUG == 1 : print("dir1=",format(pat4,'04x'),"point=",point)
                            # if self.MYDEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=2
                if ((pat2) in dic_dir2):
                # if (x>0) and ((pat2) in dic_dir2):
                    # getpoint = dic_dir2[pat2]+y*2+dic_widy[direction]-dic_aliy[direction]
                    getpoint = dic_dir2[pat2]+(y*2)
                    if self.MYDEBUG == 1 : print('I(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmin = x + dic_ofsx[direction]
                    xxmax = x + dic_ofsx[direction] + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        #print('x,y,point,getpoint2=',x,y,point,getpoint)
                        for xx in range(xxmin,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if self.MYDEBUG == 1 : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            #hole=self.counthole(board,xx,y)
                            #if (hole <=1):
                            #    if self.MYDEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #    nopoint = 1
                            #    break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if self.MYDEBUG == 1 : print("dir2=",format(pat2,'02x'),"point=",point)
                            # if self.MYDEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=3
                if (x<(width-2))and((pat3) in dic_dir3):
                    # getpoint = dic_dir3[pat3]+y*2+dic_widy[direction]-dic_aliy[direction]
                    getpoint = dic_dir3[pat3]+(y*2)
                    if self.MYDEBUG == 1 : print('I(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmin = x + dic_ofsx[direction]
                    xxmax = x + dic_ofsx[direction] + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        #print('x,y,point,getpoint3=',x,y,point,getpoint)
                        for xx in range(xxmin,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if self.MYDEBUG == 1 : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            #hole=self.counthole(board,xx,y)
                            #if (hole <=1) :
                            #    if self.MYDEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #    nopoint = 1
                            #    break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if self.MYDEBUG == 1 : print("dir3=",format(pat3,'03x'),"point=",point)
                            # if self.MYDEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
            #if self.MYDEBUG == 1 : print("x,y,pat=",x,y,format(pat4,'04x'),"point=",point)
        return point[0],point[1],point[3]
   
    #type-L
    def calcEvaluationValueIndex2(self,board,nextindex):
        #DEBUG = 1 #OFF
        if self.MYDEBUG == 1: print('block_type-L -> ',nextindex)
        direction = 0
        width = self.board_data_width #width=10
        height = self.board_data_height #height=22
        blockheight = self.maxblockheight(board)
        order = self.makehorizontalorder(blockheight)

        dic_dir0 = {0x11:7,0x10:1,0x01:1}
        dic_dir1 = {0x133:8,0x123:7,0x132:7,0x122:7,  #for Lv2~ (Lv1:17520)
        #dic_dir1 = {0x133:8,0x123:8,0x132:8,0x122:8,   #for Lv1  (Lv1:18783)
                    0x131:4,0x121:4,
                    0x130:3,0x120:3,
                    0x033:2,0x032:2,0x023:2,0x022:2,
                    0x031:1,0x021:1}
        dic_dir2 = {0x71:6,0x61:6,0x51:6,0x41:6,
                    0x70:1,0x60:1,0x50:1,0x40:1,0x30:1,0x20:1,0x10:1, #for Lv3
                    0xf1:2,0xe1:2,0xd1:2,0xc1:2,0xb1:2,0xa1:2,0x91:2,0x81:2} #add 210727a
        dic_dir3 = {0x111:9,0x110:3,0x101:3,0x011:3,0x100:1,0x010:1,0x001:1}

        dic_alix = [0,1,1,1]
        dic_aliy = [1,1,1,1]
        dic_ofsx = [0,0,0,0]
        dic_widx = [2,3,2,3]
        dic_widy = [3,2,3,2]

        dic_dir = [0,1,2,3]

        x_start = 0
        x_end = width-1
        x_step = 1
        point = [-1,-1,-1,-1] #point,x,y,direction
        for y in range(height - 3,blockheight , -1):
            for x in order:
                pat4 = self.calcBoardPat(self.board_backboard,x,y)
                pat3 = pat4 >> 4
                pat2 = pat4 >> 8
                nopoint = 0
                hole = 0
                direction=0
                if (x<(width-1))and((pat2) in dic_dir0):
                    # getpoint = dic_dir0[pat2]+y*2+dic_widy[direction]-dic_aliy[direction]
                    getpoint = dic_dir0[pat2]+(y*2)
                    if self.MYDEBUG == 1 : print('L(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        #print('x,y,point,getpoint0=',x,y,point,getpoint)
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if self.MYDEBUG == 1 : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            #if (x==xx and pat2&0xf0==0)and(x+1==xx and pat2&0x0f==0): #穴開きテスト
                            # hole=self.counthole(board,xx,y)
                            # if (hole >=1)and(hole <=4) :
                            #     if self.MYDEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #     getpoint -= hole*1
                            #     if nextindex==1 and hole>=4:
                            #         if self.MYDEBUG == 1 : print("### Next index is I, keep 4-hole. ###")
                            #         nopoint = 1
                            #         break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if self.MYDEBUG == 1 : print("dir0=",format(pat2,'02x'),"point=",point)
                            # if self.MYDEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=1
                if (x<(width-2))and((pat3) in dic_dir1):
                    # getpoint = dic_dir1[pat3]+y*2+dic_widy[direction]-dic_aliy[direction]
                    getpoint = dic_dir1[pat3]+(y*2)
                    if self.MYDEBUG == 1 : print('L(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if self.MYDEBUG == 1 : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            # hole=self.counthole(board,xx,y)
                            # if (hole >=1)and(hole <=4) :
                            #     if self.MYDEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #     getpoint -= hole*1
                            #     if nextindex==1 and hole>=4:
                            #         if self.MYDEBUG == 1 : print("### Next index is I, keep 4-hole. ###")
                            #         nopoint = 1
                            #         break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if self.MYDEBUG == 1 : print("dir1=",format(pat3,'03x'),"point=",point)
                            # if self.MYDEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=2
                if (x>=0)and(x<(width-1))and((pat2) in dic_dir2):
                    # getpoint = dic_dir2[pat2]+y*2+dic_widy[direction]-dic_aliy[direction]
                    getpoint = dic_dir2[pat2]+(y*2)
                    if self.MYDEBUG == 1 : print('L(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        #print('x,y,point,getpoint1=',x,y,point,getpoint)
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if self.MYDEBUG == 1 : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            # hole=self.counthole(board,xx,y)
                            # if (hole >=1)and(hole <=4) :
                            #     if self.MYDEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #     getpoint -= hole*1
                            #     if nextindex==1 and hole>=4:
                            #         if self.MYDEBUG == 1 : print("### Next index is I, keep 4-hole. ###")
                            #         nopoint = 1
                            #         break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if self.MYDEBUG == 1 : print("dir2=",format(pat2,'02x'),"point=",point)
                            # if self.MYDEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=3
                if (x<(width-2))and((pat3) in dic_dir3):
                    # getpoint = dic_dir3[pat3]+y*2+dic_widy[direction]-dic_aliy[direction]
                    getpoint = dic_dir3[pat3]+(y*2)
                    if self.MYDEBUG == 1 : print('L(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        #print('x,y,point,getpoint1=',x,y,point,getpoint)
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if self.MYDEBUG == 1 : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            # hole=self.counthole(board,xx,y)
                            # if (hole >=1)and(hole <=4) :
                            #     if self.MYDEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #     getpoint -= hole*1
                            #     if nextindex==1 and hole>=4:
                            #         if self.MYDEBUG == 1 : print("### Next index is I, keep 4-hole. ###")
                            #         nopoint = 1
                            #         break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if self.MYDEBUG == 1 : print("dir3=",format(pat3,'03x'),"point=",point)
                            # if self.MYDEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
        return point[0],point[1],point[3]

    #type-J
    def calcEvaluationValueIndex3(self,board,nextindex):
        #DEBUG = 1 #OFF
        if self.MYDEBUG == 1: print('block_type-J -> ',nextindex)
        direction = 0
        width = self.board_data_width #width=10
        height = self.board_data_height #height=22
        blockheight = self.maxblockheight(board)
        order = self.makehorizontalorder(blockheight)

        dic_dir0 = {0x11:7,0x10:1,0x01:1}
        dic_dir1 = {0x111:9,0x110:3,0x101:3,0x001:3,0x100:1,0x010:1,0x001:1}
        dic_dir2 = {0x17:6,0x16:6,0x15:6,0x14:6,
                    0x07:1,0x06:1,0x05:1,0x04:1,
                    0x1f:2,0x1e:2,0x1d:2,0x1c:2,0x1b:2,0x1a:2,0x19:2,0x18:2} #add 210727a
        dic_dir3 = {0x331:8,0x321:8,0x231:8,0x221:8, #for Lv2~ (Lv1:17520)
        #dic_dir3 = {0x331:8,0x321:8,0x231:8,0x221:8,  #for Lv1  (Lv1:18783)
                    0x131:4,0x121:4,0x031:3,0x021:3,
                    0x033:2,0x032:2,0x023:2,0x022:2,
                    0x031:1,0x021:1}

        dic_alix = [1,1,0,1]
        dic_aliy = [1,1,1,0]
        dic_widx = [2,3,2,3]
        dic_widy = [3,2,3,2]

        dic_dir = [0,1,2,3]

        x_start = 0
        x_end = width-1
        x_step = 1
        point = [-1,-1,-1,-1] #point,x,y,direction
        for y in range(height - 3,blockheight , -1):
            for x in order:
                pat4 = self.calcBoardPat(self.board_backboard,x,y)
                pat3 = pat4 >> 4
                pat2 = pat4 >> 8
                nopoint = 0
                hole = 0
                direction=0
                if (x<(width-1))and((pat2) in dic_dir0):
                    # getpoint = dic_dir0[pat2]+y*2+dic_widy[direction]-dic_aliy[direction]
                    getpoint = dic_dir0[pat2]+(y*2)
                    if self.MYDEBUG == 1 : print('J(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        #print('x,y,point,getpoint0=',x,y,point,getpoint)
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if self.MYDEBUG == 1 : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            # hole=self.counthole(board,xx,y)
                            # if (hole >=1)and(hole <=4) :
                            #     if self.MYDEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #     getpoint -= hole*1
                            #     if nextindex==1 and hole>=4:
                            #         if self.MYDEBUG == 1 : print("### Next index is I, keep 4-hole. ###")
                            #         nopoint = 1
                            #         break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if self.MYDEBUG == 1 : print("dir0=",format(pat2,'02x'),"point=",point)
                            # if self.MYDEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=1
                if (x<(width-2))and((pat3) in dic_dir1):
                    # getpoint = dic_dir1[pat3]+y*2+dic_widy[direction]-dic_aliy[direction]
                    getpoint = dic_dir1[pat3]+(y*2)
                    if self.MYDEBUG == 1 : print('J(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if self.MYDEBUG == 1 : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            # hole=self.counthole(board,xx,y)
                            # if (hole >=1)and(hole <=4) :
                            #     if self.MYDEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #     getpoint -= hole*1
                            #     if nextindex==1 and hole>=4:
                            #         if self.MYDEBUG == 1 : print("### Next index is I, keep 4-hole. ###")
                            #         nopoint = 1
                            #         break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if self.MYDEBUG == 1 : print("dir1=",format(pat3,'03x'),"point=",point)
                            # if self.MYDEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=2
                if (x<(width-1))and((pat2) in dic_dir2):
                    # getpoint = dic_dir2[pat2]+y*2+dic_widy[direction]-dic_aliy[direction]
                    getpoint = dic_dir2[pat2]+(y*2)
                    if self.MYDEBUG == 1 : print('J(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        #print('x,y,point,getpoint1=',x,y,point,getpoint)
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if self.MYDEBUG == 1 : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            # hole=self.counthole(board,xx,y)
                            # if (hole >=1)and(hole <=4) :
                            #     if self.MYDEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #     getpoint -= hole*1
                            #     if nextindex==1 and hole>=4:
                            #         if self.MYDEBUG == 1 : print("### Next index is I, keep 4-hole. ###")
                            #         nopoint = 1
                            #         break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if self.MYDEBUG == 1 : print("dir2=",format(pat2,'02x'),"point=",point)
                            # if self.MYDEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=3
                if (x<(width-2))and((pat3) in dic_dir3):
                    # getpoint = dic_dir3[pat3]+y*2+dic_widy[direction]-dic_aliy[direction]
                    getpoint = dic_dir3[pat3]+(y*2)
                    if self.MYDEBUG == 1 : print('J(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        #print('x,y,point,getpoint1=',x,y,point,getpoint)
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if self.MYDEBUG == 1 : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            # hole=self.counthole(board,xx,y)
                            # if (hole >=1)and(hole <=4) :
                            #     if self.MYDEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #     getpoint -= hole*1
                            #     if nextindex==1 and hole>=4:
                            #         if self.MYDEBUG == 1 : print("### Next index is I, keep 4-hole. ###")
                            #         nopoint = 1
                            #         break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if self.MYDEBUG == 1 : print("dir3=",format(pat3,'03x'),"point=",point)
                            # if self.MYDEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
        return point[0],point[1],point[3]

    #type-T
    def calcEvaluationValueIndex4(self,board,nextindex):
        #DEBUG = 1 #OFF
        if self.MYDEBUG == 1: print('block_type-T -> ',nextindex)
        direction = 0
        width = self.board_data_width #width=10
        height = self.board_data_height #height=22
        blockheight = self.maxblockheight(board)
        order = self.makehorizontalorder(blockheight)

        dic_dir0 = {0x13:6,0x12:6,
                    0x11:2,0x10:1} #for Lv3
        dic_dir1 = {0x313:8,0x213:8,0x312:8,0x212:8,
                    0x101:2}
        dic_dir2 = {0x31:6,0x21:6,
                    0x11:2,0x01:1} #for Lv3
        dic_dir3 = {0x111:7,
                    0x110:2,0x101:2,0x011:2,
                    0x100:1,0x010:1,0x001:1}

        dic_alix = [0,1,1,1]
        dic_aliy = [1,1,1,0]
        dic_widx = [2,3,2,3]
        dic_widy = [3,2,3,2]

        dic_dir = [0,1,2,3]

        x_start = 0
        x_end = width-1
        x_step = 1
        point = [-1,-1,-1,-1] #point,x,y,direction
        for y in range(height - 3,blockheight , -1):
            for x in order:
                pat4 = self.calcBoardPat(self.board_backboard,x,y)
                pat3 = pat4 >> 4
                pat2 = pat4 >> 8
                nopoint = 0
                hole = 0
                direction=0
                if (x<(width-1))and((pat2) in dic_dir0):
                    # getpoint = dic_dir0[pat2]+y*2+dic_widy[direction]-dic_aliy[direction]
                    getpoint = dic_dir0[pat2]+(y*2)
                    if self.MYDEBUG == 1 : print('T(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        #print('x,y,point,getpoint0=',x,y,point,getpoint)
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if self.MYDEBUG == 1 : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            # hole=self.counthole(board,xx,y)
                            # if (hole >=1)and(hole <=4) :
                            #     if self.MYDEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #     getpoint -= hole*1
                            #     if nextindex==1 and hole>=4:
                            #         if self.MYDEBUG == 1 : print("### Next index is I, keep 4-hole. ###")
                            #         nopoint = 1
                            #         break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if self.MYDEBUG == 1 : print("dir0=",format(pat2,'02x'),"point=",point)
                            # if self.MYDEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=1
                if (x<(width-2))and((pat3) in dic_dir1):
                    # getpoint = dic_dir1[pat3]+y*2+dic_widy[direction]-dic_aliy[direction]
                    getpoint = dic_dir1[pat3]+(y*2)
                    if self.MYDEBUG == 1 : print('T(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if self.MYDEBUG == 1 : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            # hole=self.counthole(board,xx,y)
                            # if (hole >=2)and(hole <=4) :
                            #     if self.MYDEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #     getpoint -= hole*1
                            #     if nextindex==1 and hole>=4:
                            #         if self.MYDEBUG == 1 : print("### Next index is I, keep 4-hole. ###")
                            #         nopoint = 1
                            #         break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if self.MYDEBUG == 1 : print("dir1=",format(pat4,'04x'),"point=",point)
                            # if self.MYDEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=2
                if (x<(width-1))and((pat2) in dic_dir2):
                    # getpoint = dic_dir2[pat2]+y*2+dic_widy[direction]-dic_aliy[direction]
                    getpoint = dic_dir2[pat2]+(y*2)
                    if self.MYDEBUG == 1 : print('T(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        #print('x,y,point,getpoint1=',x,y,point,getpoint)
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if self.MYDEBUG == 1 : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            # hole=self.counthole(board,xx,y)
                            # if (hole >=1)and(hole <=4) :
                            #     if self.MYDEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #     getpoint -= hole*1
                            #     if nextindex==1 and hole>=4:
                            #         if self.MYDEBUG == 1 : print("### Next index is I, keep 4-hole. ###")
                            #         nopoint = 1
                            #         break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if self.MYDEBUG == 1 : print("dir1=",format(pat4,'04x'),"point=",point)
                            # if self.MYDEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=3
                if (x<(width-2))and((pat3) in dic_dir3):
                    # getpoint = dic_dir3[pat3]+y*2+dic_widy[direction]-dic_aliy[direction]
                    getpoint = dic_dir3[pat3]+(y*2)
                    if self.MYDEBUG == 1 : print('T(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        #print('x,y,point,getpoint1=',x,y,point,getpoint)
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if self.MYDEBUG == 1 : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            # hole=self.counthole(board,xx,y)
                            # if (hole >=2)and(hole <=4) :
                            #     if self.MYDEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #     getpoint -= hole*1
                            #     if nextindex==1 and hole>=4:
                            #         if self.MYDEBUG == 1 : print("### Next index is I, keep 4-hole. ###")
                            #         nopoint = 1
                            #         break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if self.MYDEBUG == 1 : print("dir1=",format(pat4,'04x'),"point=",point)
                            # if self.MYDEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
        return point[0],point[1],point[3]

    #type-O
    def calcEvaluationValueIndex5(self,board,nextindex):
        #DEBUG = 1 #OFF
        if self.MYDEBUG == 1: print('block_type-O -> ',nextindex)
        direction = 0
        width = self.board_data_width #width=10
        height = self.board_data_height #height=22
        blockheight = self.maxblockheight(board)
        order = self.makehorizontalorder(blockheight)

        dic_dir0 = {0x11:9,
                    0x13:4,0x12:4,0x31:4,0x21:4,
                    0x17:3,0x16:3,0x15:3,0x14:3,0x71:3,0x61:3,0x51:3,0x41:3}
                    # 0x10:2,0x01:2}
        dic_dir1 = {0x11f:7,0x11e:7,0x11d:7,0x11c:7,0x11b:7,0x11a:7,0x119:7,0x118:7,\
                    0x117:7,0x116:7,0x115:7,0x114:7}
        dic_dir2 = {0xf11:7,0xe11:7,0xd11:7,0xc11:7,0xb11:7,0xa11:7,0x911:7,0x811:7,\
                    0x711:7,0x611:7,0x511:7,0x411:7}

        dic_alix = [0,0,1,0]
        dic_aliy = [1,1,1,0]
        dic_widx = [2,2,2,0]
        dic_widy = [2,2,2,0]

        dic_dir = [0,1,2,3]

        x_start = 0
        x_end = width-1
        x_step = 1
        point = [-1,-1,-1,-1] #point,x,y,direction
        for y in range(height - 3,blockheight , -1):
            for x in order:
                pat4 = self.calcBoardPat(self.board_backboard,x,y)
                pat3 = pat4 >> 4
                pat2 = pat4 >> 8
                nopoint = 0
                hole = 0
                direction=0
                if (x<(width-1))and((pat2) in dic_dir0):
                    # getpoint = dic_dir0[pat2]+y*2+dic_widy[direction]-dic_aliy[direction]
                    getpoint = dic_dir0[pat2]+(y*2)
                    if self.MYDEBUG == 1 : print('O(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        #print('x,y,point,getpoint0=',x,y,point,getpoint)
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if self.MYDEBUG == 1 : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            # hole=self.counthole(board,xx,y)
                            # if (hole >=1)and(hole <=4) :
                            #     if self.MYDEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #     getpoint -= hole*1
                            #     if nextindex==1 and hole>=4:
                            #         if self.MYDEBUG == 1 : print("### Next index is I, keep 4-hole. ###")
                            #         nopoint = 1
                            #         break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if self.MYDEBUG == 1 : print("dir0=",format(pat2,'02x'),"point=",point)
                            # if self.MYDEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=1
                if (x<(width-1))and((pat3) in dic_dir1):
                    # getpoint = dic_dir1[pat3]+y*2+dic_widy[direction]-dic_aliy[direction]
                    getpoint = dic_dir1[pat3]+(y*2)
                    if self.MYDEBUG == 1 : print('O(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if self.MYDEBUG == 1 : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            # hole=self.counthole(board,xx,y)
                            # if (hole >=1)and(hole <=4) :
                            #     if self.MYDEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #     getpoint -= hole*1
                            #     if nextindex==1 and hole>=4:
                            #         if self.MYDEBUG == 1 : print("### Next index is I, keep 4-hole. ###")
                            #         nopoint = 1
                            #         break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if self.MYDEBUG == 1 : print("dir1=",format(pat4,'04x'),"point=",point)
                            # if self.MYDEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=2
                if (x<(width-2))and((pat3) in dic_dir2):
                    # getpoint = dic_dir2[pat3]+y*2+dic_widy[direction]-dic_aliy[direction]
                    getpoint = dic_dir2[pat3]+(y*2)
                    if self.MYDEBUG == 1 : print('O(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        #print('x,y,point,getpoint1=',x,y,point,getpoint)
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if self.MYDEBUG == 1 : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            # hole=self.counthole(board,xx,y)
                            # if (hole >=1)and(hole <=4) :
                            #     if self.MYDEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #     getpoint -= hole*1
                            #     if nextindex==1 and hole>=4:
                            #         if self.MYDEBUG == 1 : print("### Next index is I, keep 4-hole. ###")
                            #         nopoint = 1
                            #         break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if self.MYDEBUG == 1 : print("dir2=",format(pat3,'03x'),"point=",point)
                            # if self.MYDEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
        return point[0],point[1],point[3]

    #type-S
    def calcEvaluationValueIndex6(self,board,nextindex):
        #DEBUG = 1 #OFF
        if self.MYDEBUG == 1: print('block_type-S -> ',nextindex)
        direction = 0
        width = self.board_data_width #width=10
        height = self.board_data_height #height=22
        blockheight = self.maxblockheight(board)
        order = self.makehorizontalorder(blockheight)

        dic_dir0 = {0x113:8,0x112:8,0x111:4}
        dic_dir1 = {0x31:6,0x21:6,
                    0x11:2,
                    0x10:6,
                    0x20:1,
                    0x01:1
                    } 
    
        dic_alix = [1,0,0,0]
        dic_aliy = [1,1,0,0]
        dic_widx = [3,2,0,0]
        dic_widy = [2,3,0,0]

        dic_dir = [0,1,2,3]

        x_start = 0
        x_end = width-1
        x_step = 1
        point = [-1,-1,-1,-1] #point,x,y,direction
        for y in range(height - 3,blockheight , -1):
            for x in order:
                pat4 = self.calcBoardPat(self.board_backboard,x,y)
                pat3 = pat4 >> 4
                pat2 = pat4 >> 8
                nopoint = 0
                hole = 0
                direction=0
                if (x<(width-2))and((pat3) in dic_dir0):
                    # getpoint = dic_dir0[pat3]+y*2+dic_widy[direction]-dic_aliy[direction]
                    getpoint = dic_dir0[pat3]+(y*2)
                    if self.MYDEBUG == 1 : print('S(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        #print('x,y,point,getpoint0=',x,y,point,getpoint)
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if self.MYDEBUG == 1 : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            # hole=self.counthole(board,xx,y)
                            # if (hole >=3)and(hole <=4) :
                            #     if self.MYDEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #     getpoint -= hole*1
                            #     if nextindex==1 and hole>=4:
                            #         if self.MYDEBUG == 1 : print("### Next index is I, keep 4-hole. ###")
                            #         nopoint = 1
                            #         break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if self.MYDEBUG == 1 : print("dir0=",format(pat3,'03x'),"point=",point)
                            # if self.MYDEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=1
                if (x<(width-1))and((pat2) in dic_dir1):
                    # getpoint = dic_dir1[pat2]+y*2+dic_widy[direction]-dic_aliy[direction]
                    getpoint = dic_dir1[pat2]+(y*2)
                    if self.MYDEBUG == 1 : print('S(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if self.MYDEBUG == 1 : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            # hole=self.counthole(board,xx,y)
                            # if (hole >=3)and(hole <=4) :
                            #     if self.MYDEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #     getpoint -= hole*1
                            #     if nextindex==1 and hole>=4:
                            #         if self.MYDEBUG == 1 : print("### Next index is I, keep 4-hole. ###")
                            #         nopoint = 1
                            #         break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if self.MYDEBUG == 1 : print("dir1=",format(pat2,'02x'),"point=",point)
                            # if self.MYDEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
        return point[0],point[1],point[3]

    #type-Z
    def calcEvaluationValueIndex7(self,board,nextindex):
        #DEBUG = 1 #OFF
        if self.MYDEBUG == 1: print('block_type-Z -> ',nextindex)
        direction = 0
        width = self.board_data_width #width=10
        height = self.board_data_height #height=22
        blockheight = self.maxblockheight(board)
        order = self.makehorizontalorder(blockheight)

        dic_dir0 = {0x311:8,0x211:8,0x111:4}
        dic_dir1 = {0x13:6,0x12:6,
                    0x11:2,
                    0x01:6,
                    0x02:1,
                    0x10:1
                    }

        dic_alix = [1,0,0,0]
        dic_aliy = [1,1,0,0]
        dic_widx = [3,2,0,0]
        dic_widy = [2,3,0,0]

        dic_dir = [0,1,2,3]

        x_start = 0
        x_end = width-1
        x_step = 1
        point = [-1,-1,-1,-1] #point,x,y,direction
        for y in range(height - 3,blockheight , -1):
            for x in order:
                pat4 = self.calcBoardPat(self.board_backboard,x,y)
                pat3 = pat4 >> 4
                pat2 = pat4 >> 8
                nopoint = 0
                hole = 0
                direction=0
                if (x<(width-2))and((pat3) in dic_dir0):
                    # getpoint = dic_dir0[pat3]+y*2+dic_widy[direction]-dic_aliy[direction]
                    getpoint = dic_dir0[pat3]+(y*2)
                    if self.MYDEBUG == 1 : print('Z(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        #print('x,y,point,getpoint0=',x,y,point,getpoint)
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if self.MYDEBUG == 1 : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            # hole=self.counthole(board,xx,y)
                            # if (hole >=3)and(hole <=4) :
                            #     if self.MYDEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #     getpoint -= hole*1
                            #     if nextindex==1 and hole>=4:
                            #         if self.MYDEBUG == 1 : print("### Next index is I, keep 4-hole. ###")
                            #         nopoint = 1
                            #         break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if self.MYDEBUG == 1 : print("dir0=",format(pat3,'03x'),"point=",point)
                            if self.MYDEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=1
                if (x<(width-1))and((pat2) in dic_dir1):
                    # getpoint = dic_dir1[pat2]+y*2+dic_widy[direction]-dic_aliy[direction]
                    getpoint = dic_dir1[pat2]+(y*2)
                    if self.MYDEBUG == 1 : print('Z(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=width):
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if self.MYDEBUG == 1 : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            # hole=self.counthole(board,xx,y)
                            # if (hole >=3)and(hole <=4) :
                            #     if self.MYDEBUG == 1 : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #     getpoint -= hole*1
                            #     if nextindex==1 and hole>=4:
                            #         if self.MYDEBUG == 1 : print("### Next index is I, keep 4-hole. ###")
                            #         nopoint = 1
                            #         break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if self.MYDEBUG == 1 : print("dir1=",format(pat2,'02x'),"point=",point)
                            # if self.MYDEBUG == 1 : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
        return point[0],point[1],point[3]

    def calcBoardPat(self,board,x,y):

        width = self.board_data_width #width=10
        height = self.board_data_height #height=22

        pat0=0
        if x > (width-1) :
            pat0=15 #right
        elif x < 0:
            pat0=15 #left
        else:
            if (board[y * width + x]!=0)and(y>=0):
                pat0 += 8
            if (board[(y+1) * width + x]!=0)and(y>=-1):
                    pat0 += 4
            if (board[(y+2) * width + x]!=0)and(y>=-2):
                    pat0 += 2
            if  y > (height-4):
                    pat0 += 1 #bottom
            elif board[(y+3) * width + x]!=0 :
                    pat0 += 1

        pat1=0
        if x > (width-2) :
            pat1=15 #right
        else:
            if (board[y * width + (x + 1)]!=0)and(y>=0):
                pat1 += 8
            if (board[(y+1) * width + (x + 1)]!=0)and(y>=-1):
                pat1 += 4
            if (board[(y+2) * width + (x + 1)]!=0)and(y>=-2):
                pat1 += 2
            if  y > (height-4):
                pat1 += 1 #bottom
            elif board[(y+3) * width + (x + 1)]!=0 :
                pat1 += 1

        pat2=0
        if x > (width-3) :
            pat2=15 #right
        else:
            if (board[(y+0) * width + (x + 2)]!=0)and(y>=0):
                pat2 += 8
            if (board[(y+1) * width + (x + 2)]!=0)and(y>=-1):
                pat2 += 4
            if (board[(y+2) * width + (x + 2)]!=0)and(y>=-2):
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
            if  (board[(y+0) * width + (x + 3)]!=0)and(y>=0):
                pat3 += 8
            if  (board[(y+1) * width + (x + 3)]!=0)and(y>=-1):
                pat3 += 4
            if  (board[(y+2) * width + (x + 3)]!=0)and(y>=-2):
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

