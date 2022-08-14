#!/usr/bin/python3
# -*- coding: utf-8 -*-

class lib_tetris:
    def __init__(self):
        self.MYDEBUG = True

        # Type-I(0)
        # Dir0
        dic_0_0={  0x0f:8,0x0e:8,0x0d:8,0x0c:8,0x0b:8,0x0a:8,0x09:8,0x08:8
                        ,0x07:6,0x06:6,0x05:6,0x04:6
                        ,0x03:3,0x02:3
                        ,0x01:2
                        ,0x00:1
                        }
        # Dir1
        dic_0_1={  0x3333:8,0x2222:8,0x1111:8
                        ,0x2333:7,0x3233:7,0x3323:7,0x3332:7                    # ish06e01
                        ,0x2233:7,0x2323:7,0x3223:7,0x3232:7,0x3322:7,0x2332:7  # ish06e01
                        ,0x2223:7,0x2232:7,0x2322:7,0x3222:7                    # ish06e01
                        ,0x1333:3,0x3133:3,0x3313:3,0x3331:3
                        ,0x1233:3,0x2133:3,0x2313:3,0x2331:3
                        ,0x1323:3,0x3123:3,0x3213:3,0x3231:3
                        ,0x1332:3,0x3132:3,0x3312:3,0x3321:3
                        ,0x1223:3,0x2123:3,0x2213:3,0x2231:3
                        ,0x1232:3,0x2132:3,0x2312:3,0x2321:3
                        ,0x1322:3,0x3122:3,0x3212:3,0x3221:3
                        ,0x1222:3,0x2122:3,0x2212:3,0x2221:3}
        # Dir2
        dic_0_2={  0xf0:8,0x80:8,0x90:8,0xa0:8,0xb0:8,0xc0:8,0xd0:8,0xe0:8
                        ,0x70:6,0x60:6,0x50:6,0x40:6
                        ,0x30:3,0x20:3
                        ,0x10:2
                        ,0x00:1
                        }
        # Dir3
        dic_0_3={  0xf0f:9,0xe0f:9,0xd0f:9,0xc0f:9,0xb0f:9,0xa0f:9,0x90f:9,0x80f:9
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
                        ,0x303:4,0x302:4,0x203:4,0x202:4
                        ,0x301:3,0x201:3,0x102:3,0x103:3
                        ,0x101:2,0x100:2,0x001:2}

        dic_alix_0 = [0,2,1,1]
        dic_aliy_0 = [1,0,1,1] # not use
        dic_ofsx_0 = [0,0,1,1] # not use
        dic_widx_0 = [1,4,1,1]
        dic_widy_0 = [4,1,4,4] # not use

        dic_dir_0 = [0,1,0,0]
        dic_pat_0 = [0,2,0,1] # pat2:0,pat3:1,pat4:2

        # TYPE-L(1)
        # Dir0
        dic_1_0=   {0x11:7,0x10:1,0x01:1}
        # Dir1
        dic_1_1=   {0x133:8,0x123:7,0x132:7,0x122:7,  #for Lv2~ (Lv1:17520)
                        # {0x133:8,0x123:8,0x132:8,0x122:8,   #for Lv1  (Lv1:18783)
                        0x131:4,0x121:4,
                        0x130:2,0x120:2,
                        0x033:2,0x032:2,0x023:2,0x022:2,
                        0x031:1,0x021:1}
        # Dir2
        dic_1_2=   {0x71:6,0x61:6,0x51:6,0x41:6,
                        0x70:1,0x60:1,0x50:1,0x40:1} #for Lv3
                        # 0xf1:2,0xe1:2,0xd1:2,0xc1:2,0xb1:2,0xa1:2,0x91:2,0x81:2} #add 210727a
        # Dir3
        dic_1_3=   {0x111:9,0x110:3,0x101:3,0x011:3
                        ,0x331:4,0x321:4,0x231:4,0x221:4
                        ,0x100:1,0x010:1,0x001:1
                        ,0x311:2,0x211:2,0x131:2,0x121:2,0x113:2,0x112:2}  

        dic_alix_1 = [0,1,1,1]
        dic_aliy_1 = [1,1,1,1]
        dic_ofsx_1 = [0,0,0,0]
        dic_widx_1 = [2,3,2,3]
        dic_widy_1 = [3,2,3,2]

        dic_dir_1 = [0,1,2,3]
        dic_pat_1 = [0,1,0,1] # pat2:0,pat3:1,pat4:2

        # TYPE-J(2)
        # Dir0
        dic_2_0=   {0x11:7,0x10:1,0x01:1}
        # Dir1
        dic_2_1=   {0x111:9,0x110:3,0x101:3,0x011:3
                        ,0x331:4,0x321:4,0x231:4,0x221:4
                        ,0x100:1,0x010:1,0x001:1
                        ,0x311:2,0x211:2,0x131:2,0x121:2,0x113:2,0x112:2}  
        # Dir2
        dic_2_2=   {0x17:6,0x16:6,0x15:6,0x14:6,
                        0x07:1,0x06:1,0x05:1,0x04:1}
                        # 0x1f:2,0x1e:2,0x1d:2,0x1c:2,0x1b:2,0x1a:2,0x19:2,0x18:2} #add 210727a
        # Dir3
        dic_2_3=   {0x331:8,0x321:8,0x231:8,0x221:8, #for Lv2~ (Lv1:17520)
                        # {0x331:8,0x321:8,0x231:8,0x221:8,  #for Lv1  (Lv1:18783)
                        0x131:4,0x121:4,0x031:3,0x021:3,
                        0x033:2,0x032:2,0x023:2,0x022:2,
                        0x031:1,0x021:1}

        dic_alix_2 = [1,1,0,1]
        dic_aliy_2 = [1,1,1,0] # not use
        dic_ofsx_2 = [0,0,0,0] # not use
        dic_widx_2 = [2,3,2,3] # not use
        dic_widy_2 = [3,2,3,2]

        dic_dir_2 = [0,1,2,3]
        dic_pat_2 = [0,1,0,1] # pat2:0,pat3:1,pat4:2

        # TYPE-T(3)
        # Dir0
        dic_3_0={  0x13:6,0x12:6,
                        0x11:2,0x10:1} #for Lv3
        # Dir1
        dic_3_1={  0x313:8,0x213:8,0x312:8,0x212:8,
                        0x515:2,
                        0x101:2}
        # Dir2
        dic_3_2={  0x31:6,0x21:6,
                        0x53:3,0x52:2,
                        0x11:2,0x01:1} #for Lv3
        # Dir3
        dic_3_3={  0x111:7,
                        0x110:2,0x101:2,0x011:2,
                        0x331:3,0x321:3,0x231:3,0x221:3,
                        0x313:3,0x213:3,0x312:3,0x212:3,
                        0x133:3,0x123:3,0x132:3,0x122:3,
                        0x100:1,0x010:1,0x001:1}

        dic_alix_3 = [0,1,1,1]
        dic_aliy_3 = [1,1,1,0] # not use
        dic_ofsx_3 = [0,0,0,0] # not use
        dic_widx_3 = [2,3,2,3]
        dic_widy_3 = [3,2,3,2] # not use

        dic_dir_3 = [0,1,2,3]
        dic_pat_3 = [0,1,0,1] # pat2:0,pat3:1,pat4:2

        # TYPE-O(4)
        # DIr0
        dic_4_0={  0x11:9,
                        0x13:4,0x12:4,0x31:4,0x21:4,
                        0x17:3,0x16:3,0x15:3,0x14:3,0x71:3,0x61:3,0x51:3,0x41:3}
        # Dir1
        dic_4_1={  0x11f:8,0x11e:8,0x11d:8,0x11c:8,0x11b:8,0x11a:8,0x119:8,0x118:8,\
                        0x117:8,0x116:8,0x115:8,0x114:8}
        # Dir2
        dic_4_2={  0xf11:8,0xe11:8,0xd11:8,0xc11:8,0xb11:8,0xa11:8,0x911:8,0x811:8,\
                        0x711:8,0x611:8,0x511:8,0x411:8}

        dic_alix_4 = [0,0,1,0]
        dic_aliy_4 = [1,1,1,0] # not use
        dic_ofsx_4 = [0,0,0,0] # not use
        dic_widx_4 = [2,2,2,0]
        dic_widy_4 = [2,2,2,0] # not use

        dic_dir_4 = [0,1,2]
        dic_pat_4 = [0,1,1] # pat2:0,pat3:1,pat4:2

        # TYPE-S(5)
        # Dir0
        dic_5_0={  0x113:8,0x112:8,0x111:4}
        # Dir1
        dic_5_1={  0x31:6,0x21:6,
                        0x11:2,
                        0x10:5,
                        # 0x20:1,
                        0x01:1
                    } 

        dic_alix_5 = [1,0,0,0]
        dic_aliy_5 = [1,1,0,0] # not use
        dic_ofsx_5 = [0,0,0,0] # not use
        dic_widx_5 = [3,2,0,0]
        dic_widy_5 = [2,3,0,0] # not use

        dic_dir_5 = [0,1]
        dic_pat_5 = [1,0] # pat2:0,pat3:1,pat4:2

        # TYPE-Z(6)
        # Dir0
        dic_6_0={  0x311:8,0x211:8,0x111:4}
        # Dir1
        dic_6_1={  0x13:6,0x12:6,
                        0x11:2,
                        0x01:5,
                        # 0x02:1,
                        0x10:1
                    }

        dic_alix_6 = [1,0,0,0]
        dic_aliy_6 = [1,1,0,0] # not use
        dic_ofsx_6 = [0,0,0,0] # not use
        dic_widx_6 = [3,2,0,0]
        dic_widy_6 = [2,3,0,0] # not use

        dic_dir_6 = [0,1]
        dic_pat_6 = [1,0] # pat2:0,pat3:1,pat4:2

        self.dic_pat_dir=[]
        dic_0=[]
        dic_1=[]
        dic_2=[]
        dic_3=[]
        dic_4=[]
        dic_5=[]
        dic_6=[]
        dic_0.append(dic_0_0)
        dic_0.append(dic_0_1)
        dic_0.append(dic_0_2)
        dic_0.append(dic_0_3)
        dic_1.append(dic_1_0)
        dic_1.append(dic_1_1)
        dic_1.append(dic_1_2)
        dic_1.append(dic_1_3)
        dic_2.append(dic_2_0)
        dic_2.append(dic_2_1)
        dic_2.append(dic_2_2)
        dic_2.append(dic_2_3)
        dic_3.append(dic_3_0)
        dic_3.append(dic_3_1)
        dic_3.append(dic_3_2)
        dic_3.append(dic_3_3)
        dic_4.append(dic_4_0)
        dic_4.append(dic_4_1)
        dic_4.append(dic_4_2)
        dic_5.append(dic_5_0)
        dic_5.append(dic_5_1)
        dic_6.append(dic_6_0)
        dic_6.append(dic_6_1)
        self.dic_pat_dir.append(dic_0) # TYPE-I
        self.dic_pat_dir.append(dic_1) # TYPE-L
        self.dic_pat_dir.append(dic_2) # TYPE-J
        self.dic_pat_dir.append(dic_3) # TYPE-T
        self.dic_pat_dir.append(dic_4) # TYPE-O
        self.dic_pat_dir.append(dic_5) # TYPE-S
        self.dic_pat_dir.append(dic_6) # TYPE-Z

        self.dic_alix=[]
        self.dic_aliy=[]
        self.dic_ofsx=[]
        self.dic_widx=[]
        self.dic_widy=[]
        self.dic_dir =[]
        self.dic_alix.append(dic_alix_0)
        self.dic_alix.append(dic_alix_1)
        self.dic_alix.append(dic_alix_2)
        self.dic_alix.append(dic_alix_3)
        self.dic_alix.append(dic_alix_4)
        self.dic_alix.append(dic_alix_5)
        self.dic_alix.append(dic_alix_6)
        self.dic_aliy.append(dic_aliy_0)
        self.dic_aliy.append(dic_aliy_1)
        self.dic_aliy.append(dic_aliy_2)
        self.dic_aliy.append(dic_aliy_3)
        self.dic_aliy.append(dic_aliy_4)
        self.dic_aliy.append(dic_aliy_5)
        self.dic_aliy.append(dic_aliy_6)
        self.dic_ofsx.append(dic_ofsx_0)
        self.dic_ofsx.append(dic_ofsx_1)
        self.dic_ofsx.append(dic_ofsx_2)
        self.dic_ofsx.append(dic_ofsx_3)
        self.dic_ofsx.append(dic_ofsx_4)
        self.dic_ofsx.append(dic_ofsx_5)
        self.dic_ofsx.append(dic_ofsx_6)
        self.dic_widx.append(dic_widx_0)
        self.dic_widx.append(dic_widx_1)
        self.dic_widx.append(dic_widx_2)
        self.dic_widx.append(dic_widx_3)
        self.dic_widx.append(dic_widx_4)
        self.dic_widx.append(dic_widx_5)
        self.dic_widx.append(dic_widx_6)
        self.dic_widy.append(dic_widy_0)
        self.dic_widy.append(dic_widy_1)
        self.dic_widy.append(dic_widy_2)
        self.dic_widy.append(dic_widy_3)
        self.dic_widy.append(dic_widy_4)
        self.dic_widy.append(dic_widy_5)
        self.dic_widy.append(dic_widy_6)
        self.dic_dir.append(dic_dir_0)
        self.dic_dir.append(dic_dir_1)
        self.dic_dir.append(dic_dir_2)
        self.dic_dir.append(dic_dir_3)
        self.dic_dir.append(dic_dir_4)
        self.dic_dir.append(dic_dir_5)
        self.dic_dir.append(dic_dir_6)

        self.dic_pat=[]
        self.dic_pat.append(dic_pat_0)
        self.dic_pat.append(dic_pat_1)
        self.dic_pat.append(dic_pat_2)
        self.dic_pat.append(dic_pat_3)
        self.dic_pat.append(dic_pat_4)
        self.dic_pat.append(dic_pat_5)
        self.dic_pat.append(dic_pat_6)

    def makehorizontalorder(self,maxheight):
        if maxheight < 10 :
            return(self.makehorizontalorder3())
        else :
            return(self.makehorizontalorder4())

    def makehorizontalorder1(self): #[0,1,2,3,4,5,6,6,8,9]
        #order = list(range(self.width))
        #for ii in range(0,self.width,1):
        #    order[ii]=ii
        return([0,1,2,3,4,5,6,7,8,9])

    def makehorizontalorder2(self): #[9,8,7,6,5,4,3,2,1,0]
        #order = list(range(self.width))
        #for ii in range(0,self.width,1):
        #    order[ii]=self.width-ii-1
        return([9,8,7,6,5,4,3,2,1,0])

    def makehorizontalorder3(self): #[0,9,1,8,2,7,3,6,4,5]
        # order = list(range(self.width+1))
        # for ii in range(0,self.width+1,1):
        #     if int(ii/2)==(ii/2) :
        #         order[ii] = int(ii/2)-1
        #     else:
        #         order[ii] = self.width-1-int(ii/2)
        # if ((self.MYDEBUG)):print('order3=',order)
        return([0,9,1,8,2,7,3,6,4,5])

    def makehorizontalorder4(self): #[5,4,6,3,7,2,8,1,9,0]
        # order = list(range(self.width+1))
        # for ii in range(0,self.width+1,1):
        #     if int(ii/2)==(ii/2) :
        #         order[self.width-ii] = int(ii/2)-1
        #     else:
        #         order[self.width-ii] = self.width-1-int(ii/2)
        # if ((self.MYDEBUG)):print('order4=',order)
        return([5,4,6,3,7,2,8,1,9,0])

    def checkupper(self,board,xpos,ypos): 
        block=0
        for yy in range(ypos,0,-1):
            if board[(yy) * self.width + (xpos)] != 0:
                block = 1
                break
        return(block)

    def counthole(self,board,xpos,ypos):
        hole=0
        if (self.height-1<ypos+3): return(0)
        for yy in range(ypos,self.height,1):
            #if (yy < height):
            if board[(yy) * self.width + (xpos)] == 0:
                hole += 1
            else:
                break
        return(hole)

    def maxblockheight(self,board):
        # maxheight=height-4
        # for yy in range(height-1,4,-1):
        #     for xx in range(0,self.width,1):
        #         if board[yy*self.width+xx]!=0:
        #             maxheight = yy-4
        for yy in range(0,self.height,1):
            for xx in range(0,self.width,1):
                if board[yy*self.width+xx]!=0:
                    return(yy-4)
        return(self.height-4)

    def calcEvaluationValue(self,GameStatus,board,nextindex):
        self.width  = GameStatus["field_info"]["width"] # width=10
        self.height = GameStatus["field_info"]["height"] # height=22
        self.index  = GameStatus["block_info"]["currentShape"]["index"] - 1 # 0:I,1:L,2:J,3:T,4:O,5:S,6:Z
        blockheight = self.maxblockheight(board)
        if ((self.MYDEBUG)):print('blockheight=',blockheight)
        order = self.makehorizontalorder(blockheight)
        ypos_change = -3
        point = [-1,-1,-1,-1] #point,x,y,direction
        for y in range(self.height - 3,blockheight , -1):
            for x in order:
                pat4 = self.calcBoardPat(board,x,y)
                pat3 = pat4 >> 4
                pat2 = pat4 >> 8
                pat=[pat2,pat3,pat4]
                #check over 4 hole
                # if self.checkupper(board,x+dic_alix[direction],y)!=1 :
                #     hole=self.counthole(board,x+dic_alix[direction],y)
                #     if (hole >= 4):
                #         getpoint = 10+hole-4+y*2
                #         if (((point[0]<getpoint))):
                #             if (self.MYDEBUG) : print("### FOUND THE HOLE(",hole,")",x,y,format(pat4,'04x'))
                #             point=getpoint,x,y,direction
                #             if (self.MYDEBUG) : print("hole=",format(pat4,'04x'),"point=",point)
                for direction in self.dic_dir[self.index]:
                    nopoint = 0
                    hole = 0
                    if (x<(self.width-self.dic_pat[self.index][direction]-self.dic_alix[self.index][direction]))\
                        and (pat[self.dic_pat[self.index][direction]] in self.dic_pat_dir[self.index][direction]):
                        # if self.MYDEBUG:
                        #     print('index,direction,patno,pat=',self.index,direction,self.dic_pat[self.index][direction],pat[self.dic_pat[self.index][direction]])
                        basepoint = self.dic_pat_dir[self.index][direction][pat[self.dic_pat[self.index][direction]]]
                        if y>= ypos_change :
                            getpoint = basepoint+(y*2)
                        else :
                            getpoint = basepoint
                        if (self.MYDEBUG) :
                            print('(index,dir,x,y)=',self.index,direction,x,y,'pat=',format(pat[self.dic_pat[self.index][direction]],'04x'),'gp=',getpoint)
                        xxmin = x + self.dic_ofsx[self.index][direction]
                        xxmax = xxmin + self.dic_widx[self.index][direction]
                        if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=self.width):
                            for xx in range(xxmin,xxmax,1):
                                if self.checkupper(board,xx,y)==1:
                                    if (self.MYDEBUG) : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                    nopoint = 1
                                    break
                                print('widy,aliy=',self.dic_widy[self.index][direction],self.dic_aliy[self.index][direction])
                                hole = self.counthole(board,xx,y+self.dic_widy[self.index][direction]-self.dic_aliy[self.index][direction]+1)
                                if (hole > 0):
                                    if (self.MYDEBUG) : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                                    getpoint = getpoint -int(hole/2)
                                #    nopoint = 1
                                #    break
                            if (nopoint==0):
                                point = getpoint,x+self.dic_alix[self.index][direction],y,direction
                                if (self.MYDEBUG) : print("pat=",format(pat[self.dic_pat[self.index][direction]],'04x'),"point=",point)

            #if (self.MYDEBUG) : print("x,y,pat=",x,y,format(pat4,'04x'),"point=",point)
        return point[0],point[1],point[3]

    #type-I(0)
    def calcEvaluationValueIndex1(self,GameStatus,board,nextindex):
        if (self.MYDEBUG) : print('block_type-I -> ',nextindex)
        self.width = GameStatus["field_info"]["width"] #width=10
        self.height = GameStatus["field_info"]["height"] #height=22
        blockheight = self.maxblockheight(board)
        order = self.makehorizontalorder(blockheight)
        ypos_change = -3

        dic_alix = [0,2,1,1]
        # dic_aliy = [1,0,1,1]
        dic_ofsx = [0,0,1,1]
        dic_widx = [1,4,1,1]
        # dic_widy = [4,1,4,4]

        dic_dir = [0,1,0,0]

        # x_start = 0
        # x_end = self.width-1
        # x_step = 1
        point = [-1,-1,-1,-1] #point,x,y,direction
        for y in range(self.height - 3,blockheight , -1):
        # for y in range(self.height - 3, blockheight ,-1):
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
                #             if (self.MYDEBUG) : print("### FOUND THE HOLE(",hole,")",x,y,format(pat4,'04x'))
                #             point=getpoint,x,y,direction
                #             if (self.MYDEBUG) : print("hole=",format(pat4,'04x'),"point=",point)
                if pat2 in self.dic_pat_dir[0][direction]:
                # if (x<(self.width))and((pat2) in self.dic_pat_dir[0][direction]):
                    basepoint = self.dic_pat_dir[0][direction][pat2]
                    # getpoint = basepoint+y*2+dic_widy[direction]-dic_aliy[direction] #for Lv2
                    if y>= ypos_change : getpoint = basepoint+(y*2)
                    else : getpoint = basepoint
                    #getpoint = basepoint #for Lv1
                    if (self.MYDEBUG) : print('I(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmin = x + dic_ofsx[direction]
                    xxmax = x + dic_ofsx[direction] + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=self.width):
                        #print('x,y,point,getpoint0=',x,y,point,getpoint)
                        for xx in range(xxmin,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if (self.MYDEBUG) : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            #hole=self.counthole(board,xx,y)
                            #if (hole <=1):
                            #    if (self.MYDEBUG) : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #    nopoint = 1
                            #    break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if (self.MYDEBUG) : print("dir0=",format(pat2,'02x'),"point=",point)
                            # if (self.MYDEBUG) : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=1
                if  (x<(self.width-3))and((pat4) in self.dic_pat_dir[0][direction]):
                    basepoint = self.dic_pat_dir[0][direction][pat4]
                    # getpoint = basepoint+y*2+dic_widy[direction]-dic_aliy[direction]
                    if y>= ypos_change : getpoint = basepoint+(y*2)
                    else : getpoint = basepoint
                    if (self.MYDEBUG) : print('I(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmin = x + dic_ofsx[direction]
                    xxmax = x + dic_ofsx[direction] + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=self.width):
                        #print('x,y,point,getpoint1=',x,y,point,getpoint)
                        for xx in range(xxmin,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if (self.MYDEBUG) : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            #hole=self.counthole(board,xx,y)
                            #if (hole >=1)and(hole <=4) :
                            #    if (self.MYDEBUG) : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #    getpoint -= hole*1
                            #    if nextindex==1 and hole>=4:
                            #        if (self.MYDEBUG) : print("### Next index is I, keep 4-hole. ###")
                            #        nopoint = 1
                            #        break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if (self.MYDEBUG) : print("dir1=",format(pat4,'04x'),"point=",point)
                            # if (self.MYDEBUG) : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=2
                if ((pat2) in self.dic_pat_dir[0][direction]):
                # if (x>0) and ((pat2) in self.dic_pat_dir[0][direction]):
                    basepoint = self.dic_pat_dir[0][direction][pat2]
                    # getpoint = basepoint+y*2+dic_widy[direction]-dic_aliy[direction]
                    if y>= ypos_change : getpoint = basepoint+(y*2)
                    else : getpoint = basepoint
                    if (self.MYDEBUG) : print('I(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmin = x + dic_ofsx[direction]
                    xxmax = x + dic_ofsx[direction] + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=self.width):
                        #print('x,y,point,getpoint2=',x,y,point,getpoint)
                        for xx in range(xxmin,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if (self.MYDEBUG) : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            #hole=self.counthole(board,xx,y)
                            #if (hole <=1):
                            #    if (self.MYDEBUG) : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #    nopoint = 1
                            #    break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if (self.MYDEBUG) : print("dir2=",format(pat2,'02x'),"point=",point)
                            # if (self.MYDEBUG) : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=3
                if (x<(self.width-2))and((pat3) in self.dic_pat_dir[0][direction]):
                    basepoint = self.dic_pat_dir[0][direction][pat3]
                    # getpoint = basepoint+y*2+dic_widy[direction]-dic_aliy[direction]
                    if y>= ypos_change : getpoint = basepoint+(y*2)
                    else : getpoint = basepoint
                    if (self.MYDEBUG) : print('I(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmin = x + dic_ofsx[direction]
                    xxmax = x + dic_ofsx[direction] + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=self.width):
                        #print('x,y,point,getpoint3=',x,y,point,getpoint)
                        for xx in range(xxmin,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if (self.MYDEBUG) : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            #hole=self.counthole(board,xx,y)
                            #if (hole <=1) :
                            #    if (self.MYDEBUG) : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #    nopoint = 1
                            #    break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if (self.MYDEBUG) : print("dir3=",format(pat3,'03x'),"point=",point)
                            # if (self.MYDEBUG) : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
            #if (self.MYDEBUG) : print("x,y,pat=",x,y,format(pat4,'04x'),"point=",point)
        return point[0],point[1],point[3]
   
    #type-L(1)
    def calcEvaluationValueIndex2(self,GameStatus,board,nextindex):
        #DEBUG = 1 #OFF
        if (self.MYDEBUG): print('block_type-L -> ',nextindex)
        direction = 0
        self.width = GameStatus["field_info"]["width"] #width=10
        self.height = GameStatus["field_info"]["height"] #height=22
        blockheight = self.maxblockheight(board)
        order = self.makehorizontalorder(blockheight)
        ypos_change = -3

        dic_alix = [0,1,1,1]
        # dic_aliy = [1,1,1,1]
        # dic_ofsx = [0,0,0,0]
        dic_widx = [2,3,2,3]
        # dic_widy = [3,2,3,2]

        dic_dir = [0,1,2,3]

        # x_start = 0
        # x_end = self.width-1
        # x_step = 1
        point = [-1,-1,-1,-1] #point,x,y,direction
        for y in range(self.height - 3,blockheight , -1):
            for x in order:
                pat4 = self.calcBoardPat(GameStatus["field_info"]["backboard"],x,y)
                pat3 = pat4 >> 4
                pat2 = pat4 >> 8
                nopoint = 0
                hole = 0
                direction=0
                if (x<(self.width-1))and((pat2) in self.dic_pat_dir[1][direction]):
                    basepoint = self.dic_pat_dir[1][direction][pat2]
                    # getpoint = basepoint+y*2+dic_widy[direction]-dic_aliy[direction]
                    if y>= ypos_change : getpoint = basepoint+(y*2)
                    else : getpoint = basepoint
                    if (self.MYDEBUG) : print('L(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=self.width):
                        #print('x,y,point,getpoint0=',x,y,point,getpoint)
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if (self.MYDEBUG) : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            #if (x==xx and pat2&0xf0==0)and(x+1==xx and pat2&0x0f==0): #穴開きテスト
                            # hole=self.counthole(board,xx,y)
                            # if (hole >=1)and(hole <=4) :
                            #     if (self.MYDEBUG) : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #     getpoint -= hole*1
                            #     if nextindex==1 and hole>=4:
                            #         if (self.MYDEBUG) : print("### Next index is I, keep 4-hole. ###")
                            #         nopoint = 1
                            #         break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if (self.MYDEBUG) : print("dir0=",format(pat2,'02x'),"point=",point)
                            # if (self.MYDEBUG) : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=1
                if (x<(self.width-2))and((pat3) in self.dic_pat_dir[1][direction]):
                    basepoint = self.dic_pat_dir[1][direction][pat3]
                    # getpoint = basepoint+y*2+dic_widy[direction]-dic_aliy[direction]
                    if y>= ypos_change : getpoint = basepoint+(y*2)
                    else : getpoint = basepoint
                    if (self.MYDEBUG) : print('L(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=self.width):
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if (self.MYDEBUG) : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            # hole=self.counthole(board,xx,y)
                            # if (hole >=1)and(hole <=4) :
                            #     if (self.MYDEBUG) : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #     getpoint -= hole*1
                            #     if nextindex==1 and hole>=4:
                            #         if (self.MYDEBUG) : print("### Next index is I, keep 4-hole. ###")
                            #         nopoint = 1
                            #         break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if (self.MYDEBUG) : print("dir1=",format(pat3,'03x'),"point=",point)
                            # if (self.MYDEBUG) : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=2
                if (x>=0)and(x<(self.width-1))and((pat2) in self.dic_pat_dir[1][direction]):
                    basepoint = self.dic_pat_dir[1][direction][pat2]
                    # getpoint = basepoint+y*2+dic_widy[direction]-dic_aliy[direction]
                    if y>= ypos_change : getpoint = basepoint+(y*2)
                    else : getpoint = basepoint
                    if (self.MYDEBUG) : print('L(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=self.width):
                        #print('x,y,point,getpoint1=',x,y,point,getpoint)
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if (self.MYDEBUG) : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            # hole=self.counthole(board,xx,y)
                            # if (hole >=1)and(hole <=4) :
                            #     if (self.MYDEBUG) : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #     getpoint -= hole*1
                            #     if nextindex==1 and hole>=4:
                            #         if (self.MYDEBUG) : print("### Next index is I, keep 4-hole. ###")
                            #         nopoint = 1
                            #         break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if (self.MYDEBUG) : print("dir2=",format(pat2,'02x'),"point=",point)
                            # if (self.MYDEBUG) : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=3
                if (x<(self.width-2))and((pat3) in self.dic_pat_dir[1][direction]):
                    basepoint = self.dic_pat_dir[1][direction][pat3]
                    # getpoint = basepoint+y*2+dic_widy[direction]-dic_aliy[direction]
                    if y>= ypos_change : getpoint = basepoint+(y*2)
                    else : getpoint = basepoint
                    if (self.MYDEBUG) : print('L(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=self.width):
                        #print('x,y,point,getpoint1=',x,y,point,getpoint)
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if (self.MYDEBUG) : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            # hole=self.counthole(board,xx,y)
                            # if (hole >=1)and(hole <=4) :
                            #     if (self.MYDEBUG) : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #     getpoint -= hole*1
                            #     if nextindex==1 and hole>=4:
                            #         if (self.MYDEBUG) : print("### Next index is I, keep 4-hole. ###")
                            #         nopoint = 1
                            #         break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if (self.MYDEBUG) : print("dir3=",format(pat3,'03x'),"point=",point)
                            # if (self.MYDEBUG) : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
        return point[0],point[1],point[3]

    #type-J(2)
    def calcEvaluationValueIndex3(self,GameStatus,board,nextindex):
        #DEBUG = 1 #OFF
        if (self.MYDEBUG): print('block_type-J -> ',nextindex)
        direction = 0
        self.width = GameStatus["field_info"]["width"] #width=10
        self.height = GameStatus["field_info"]["height"] #height=22
        blockheight = self.maxblockheight(board)
        order = self.makehorizontalorder(blockheight)
        ypos_change = -3

        dic_alix = [1,1,0,1]
        # dic_aliy = [1,1,1,0]
        dic_widx = [2,3,2,3]
        # dic_widy = [3,2,3,2]

        dic_dir = [0,1,2,3]

        # x_start = 0
        # x_end = self.width-1
        # x_step = 1
        point = [-1,-1,-1,-1] #point,x,y,direction
        for y in range(self.height - 3,blockheight , -1):
            for x in order:
                pat4 = self.calcBoardPat(GameStatus["field_info"]["backboard"],x,y)
                pat3 = pat4 >> 4
                pat2 = pat4 >> 8
                nopoint = 0
                hole = 0
                direction=0
                if (x<(self.width-1))and((pat2) in self.dic_pat_dir[2][direction]):
                    basepoint = self.dic_pat_dir[2][direction][pat2]
                    # getpoint = basepoint+y*2+dic_widy[direction]-dic_aliy[direction]
                    if y>= ypos_change : getpoint = basepoint+(y*2)
                    else : getpoint = basepoint
                    if (self.MYDEBUG) : print('J(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=self.width):
                        #print('x,y,point,getpoint0=',x,y,point,getpoint)
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if (self.MYDEBUG) : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            # hole=self.counthole(board,xx,y)
                            # if (hole >=1)and(hole <=4) :
                            #     if (self.MYDEBUG) : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #     getpoint -= hole*1
                            #     if nextindex==1 and hole>=4:
                            #         if (self.MYDEBUG) : print("### Next index is I, keep 4-hole. ###")
                            #         nopoint = 1
                            #         break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if (self.MYDEBUG) : print("dir0=",format(pat2,'02x'),"point=",point)
                            # if (self.MYDEBUG) : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=1
                if (x<(self.width-2))and((pat3) in self.dic_pat_dir[2][direction]):
                    basepoint = self.dic_pat_dir[2][direction][pat3]
                    # getpoint = basepoint+y*2+dic_widy[direction]-dic_aliy[direction]
                    if y>= ypos_change : getpoint = basepoint+(y*2)
                    else : getpoint = basepoint
                    if (self.MYDEBUG) : print('J(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=self.width):
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if (self.MYDEBUG) : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            # hole=self.counthole(board,xx,y)
                            # if (hole >=1)and(hole <=4) :
                            #     if (self.MYDEBUG) : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #     getpoint -= hole*1
                            #     if nextindex==1 and hole>=4:
                            #         if (self.MYDEBUG) : print("### Next index is I, keep 4-hole. ###")
                            #         nopoint = 1
                            #         break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if (self.MYDEBUG) : print("dir1=",format(pat3,'03x'),"point=",point)
                            # if (self.MYDEBUG) : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=2
                if (x<(self.width-1))and((pat2) in self.dic_pat_dir[2][direction]):
                    basepoint = self.dic_pat_dir[2][direction][pat2]
                    # getpoint = basepoint+y*2+dic_widy[direction]-dic_aliy[direction]
                    if y>= ypos_change : getpoint =basepoint+(y*2)
                    else : getpoint = basepoint
                    if (self.MYDEBUG) : print('J(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=self.width):
                        #print('x,y,point,getpoint1=',x,y,point,getpoint)
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if (self.MYDEBUG) : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            # hole=self.counthole(board,xx,y)
                            # if (hole >=1)and(hole <=4) :
                            #     if (self.MYDEBUG) : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #     getpoint -= hole*1
                            #     if nextindex==1 and hole>=4:
                            #         if (self.MYDEBUG) : print("### Next index is I, keep 4-hole. ###")
                            #         nopoint = 1
                            #         break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if (self.MYDEBUG) : print("dir2=",format(pat2,'02x'),"point=",point)
                            # if (self.MYDEBUG) : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=3
                if (x<(self.width-2))and((pat3) in self.dic_pat_dir[2][direction]):
                    basepoint = self.dic_pat_dir[2][direction][pat3]
                    # getpoint = basepoint+y*2+dic_widy[direction]-dic_aliy[direction]
                    if y>= ypos_change : getpoint = basepoint+(y*2)
                    else : getpoint = basepoint
                    if (self.MYDEBUG) : print('J(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=self.width):
                        #print('x,y,point,getpoint1=',x,y,point,getpoint)
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if (self.MYDEBUG) : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            # hole=self.counthole(board,xx,y)
                            # if (hole >=1)and(hole <=4) :
                            #     if (self.MYDEBUG) : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #     getpoint -= hole*1
                            #     if nextindex==1 and hole>=4:
                            #         if (self.MYDEBUG) : print("### Next index is I, keep 4-hole. ###")
                            #         nopoint = 1
                            #         break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if (self.MYDEBUG) : print("dir3=",format(pat3,'03x'),"point=",point)
                            # if (self.MYDEBUG) : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
        return point[0],point[1],point[3]

    #type-T(3)
    def calcEvaluationValueIndex4(self,GameStatus,board,nextindex):
        #DEBUG = 1 #OFF
        if (self.MYDEBUG): print('block_type-T -> ',nextindex)
        direction = 0
        self.width = GameStatus["field_info"]["width"] #width=10
        self.height = GameStatus["field_info"]["height"] #height=22
        blockheight = self.maxblockheight(board)
        order = self.makehorizontalorder(blockheight)
        ypos_change = -3

        dic_alix = [0,1,1,1]
        # dic_aliy = [1,1,1,0]
        dic_widx = [2,3,2,3]
        # dic_widy = [3,2,3,2]

        dic_dir = [0,1,2,3]

        # x_start = 0
        # x_end = self.width-1
        # x_step = 1
        point = [-1,-1,-1,-1] #point,x,y,direction
        for y in range(self.height - 3,blockheight , -1):
            for x in order:
                pat4 = self.calcBoardPat(GameStatus["field_info"]["backboard"],x,y)
                pat3 = pat4 >> 4
                pat2 = pat4 >> 8
                nopoint = 0
                hole = 0
                direction=0
                if (x<(self.width-1))and((pat2) in self.dic_pat_dir[3][direction]):
                    basepoint = self.dic_pat_dir[3][direction][pat2]
                    # getpoint = basepoint+y*2+dic_widy[direction]-dic_aliy[direction]
                    if y>= ypos_change : getpoint = basepoint+(y*2)
                    else : getpoint = basepoint
                    if (self.MYDEBUG) : print('T(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=self.width):
                        #print('x,y,point,getpoint0=',x,y,point,getpoint)
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if (self.MYDEBUG) : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            # hole=self.counthole(board,xx,y)
                            # if (hole >=1)and(hole <=4) :
                            #     if (self.MYDEBUG) : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #     getpoint -= hole*1
                            #     if nextindex==1 and hole>=4:
                            #         if (self.MYDEBUG) : print("### Next index is I, keep 4-hole. ###")
                            #         nopoint = 1
                            #         break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if (self.MYDEBUG) : print("dir0=",format(pat2,'02x'),"point=",point)
                            # if (self.MYDEBUG) : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=1
                if (x<(self.width-2))and((pat3) in self.dic_pat_dir[3][direction]):
                    basepoint = self.dic_pat_dir[3][direction][pat3]
                    # getpoint = basepoint+y*2+dic_widy[direction]-dic_aliy[direction]
                    if y>= ypos_change : getpoint = basepoint+(y*2)
                    else : getpoint = basepoint
                    if (self.MYDEBUG) : print('T(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=self.width):
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if (self.MYDEBUG) : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            # hole=self.counthole(board,xx,y)
                            # if (hole >=2)and(hole <=4) :
                            #     if (self.MYDEBUG) : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #     getpoint -= hole*1
                            #     if nextindex==1 and hole>=4:
                            #         if (self.MYDEBUG) : print("### Next index is I, keep 4-hole. ###")
                            #         nopoint = 1
                            #         break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if (self.MYDEBUG) : print("dir1=",format(pat4,'04x'),"point=",point)
                            # if (self.MYDEBUG) : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=2
                if (x<(self.width-1))and((pat2) in self.dic_pat_dir[3][direction]):
                    basepoint = self.dic_pat_dir[3][direction][pat2]
                    # getpoint = basepoint+y*2+dic_widy[direction]-dic_aliy[direction]
                    if y>= ypos_change : getpoint = basepoint+(y*2)
                    else : getpoint = basepoint
                    if (self.MYDEBUG) : print('T(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=self.width):
                        #print('x,y,point,getpoint1=',x,y,point,getpoint)
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if (self.MYDEBUG) : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            # hole=self.counthole(board,xx,y)
                            # if (hole >=1)and(hole <=4) :
                            #     if (self.MYDEBUG) : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #     getpoint -= hole*1
                            #     if nextindex==1 and hole>=4:
                            #         if (self.MYDEBUG) : print("### Next index is I, keep 4-hole. ###")
                            #         nopoint = 1
                            #         break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if (self.MYDEBUG) : print("dir1=",format(pat4,'04x'),"point=",point)
                            # if (self.MYDEBUG) : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=3
                if (x<(self.width-2))and((pat3) in self.dic_pat_dir[3][direction]):
                    basepoint = self.dic_pat_dir[3][direction][pat3]
                    # getpoint = basepoint+y*2+dic_widy[direction]-dic_aliy[direction]
                    if y>= ypos_change : getpoint = basepoint+(y*2)
                    else : getpoint =basepoint
                    if (self.MYDEBUG) : print('T(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=self.width):
                        #print('x,y,point,getpoint1=',x,y,point,getpoint)
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if (self.MYDEBUG) : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            # hole=self.counthole(board,xx,y)
                            # if (hole >=2)and(hole <=4) :
                            #     if (self.MYDEBUG) : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #     getpoint -= hole*1
                            #     if nextindex==1 and hole>=4:
                            #         if (self.MYDEBUG) : print("### Next index is I, keep 4-hole. ###")
                            #         nopoint = 1
                            #         break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if (self.MYDEBUG) : print("dir1=",format(pat4,'04x'),"point=",point)
                            # if (self.MYDEBUG) : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
        return point[0],point[1],point[3]

    #type-O(4)
    def calcEvaluationValueIndex5(self,GameStatus,board,nextindex):
        #DEBUG = 1 #OFF
        if (self.MYDEBUG): print('block_type-O -> ',nextindex)
        direction = 0
        self.width = GameStatus["field_info"]["width"] #width=10
        self.height = GameStatus["field_info"]["height"] #height=22
        blockheight = self.maxblockheight(board)
        order = self.makehorizontalorder(blockheight)
        ypos_change = -3

        dic_alix = [0,0,1,0]
        # dic_aliy = [1,1,1,0]
        dic_widx = [2,2,2,0]
        # dic_widy = [2,2,2,0]

        dic_dir = [0,1,2,3]

        # x_start = 0
        # x_end = self.width-1
        # x_step = 1
        point = [-1,-1,-1,-1] #point,x,y,direction
        for y in range(self.height - 3,blockheight , -1):
            for x in order:
                pat4 = self.calcBoardPat(GameStatus["field_info"]["backboard"],x,y)
                pat3 = pat4 >> 4
                pat2 = pat4 >> 8
                nopoint = 0
                hole = 0
                direction=0
                if (x<(self.width-1))and((pat2) in self.dic_pat_dir[4][direction]):
                    basepoint = self.dic_pat_dir[4][direction][pat2]
                    # getpoint = basepoint+y*2+dic_widy[direction]-dic_aliy[direction]
                    if y>= ypos_change : getpoint = basepoint+(y*2)
                    else : getpoint = basepoint
                    if (self.MYDEBUG) : print('O(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=self.width):
                        #print('x,y,point,getpoint0=',x,y,point,getpoint)
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if (self.MYDEBUG) : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            # hole=self.counthole(board,xx,y)
                            # if (hole >=1)and(hole <=4) :
                            #     if (self.MYDEBUG) : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #     getpoint -= hole*1
                            #     if nextindex==1 and hole>=4:
                            #         if (self.MYDEBUG) : print("### Next index is I, keep 4-hole. ###")
                            #         nopoint = 1
                            #         break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if (self.MYDEBUG) : print("dir0=",format(pat2,'02x'),"point=",point)
                            # if (self.MYDEBUG) : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=1
                if (x<(self.width-1))and((pat3) in self.dic_pat_dir[4][direction]):
                    basepoint = self.dic_pat_dir[4][direction][pat3]
                    # getpoint = basepoint+y*2+dic_widy[direction]-dic_aliy[direction]
                    if y>= ypos_change : getpoint = basepoint+(y*2)
                    else : getpoint = basepoint
                    if (self.MYDEBUG) : print('O(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=self.width):
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if (self.MYDEBUG) : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            # hole=self.counthole(board,xx,y)
                            # if (hole >=1)and(hole <=4) :
                            #     if (self.MYDEBUG) : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #     getpoint -= hole*1
                            #     if nextindex==1 and hole>=4:
                            #         if (self.MYDEBUG) : print("### Next index is I, keep 4-hole. ###")
                            #         nopoint = 1
                            #         break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if (self.MYDEBUG) : print("dir1=",format(pat4,'04x'),"point=",point)
                            # if (self.MYDEBUG) : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=2
                if (x<(self.width-2))and((pat3) in self.dic_pat_dir[4][direction]):
                    basepoint = self.dic_pat_dir[4][direction][pat3]
                    # getpoint = basepoint+y*2+dic_widy[direction]-dic_aliy[direction]
                    if y>= ypos_change : getpoint = basepoint+(y*2)
                    else : getpoint = basepoint
                    if (self.MYDEBUG) : print('O(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=self.width):
                        #print('x,y,point,getpoint1=',x,y,point,getpoint)
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if (self.MYDEBUG) : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            # hole=self.counthole(board,xx,y)
                            # if (hole >=1)and(hole <=4) :
                            #     if (self.MYDEBUG) : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #     getpoint -= hole*1
                            #     if nextindex==1 and hole>=4:
                            #         if (self.MYDEBUG) : print("### Next index is I, keep 4-hole. ###")
                            #         nopoint = 1
                            #         break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if (self.MYDEBUG) : print("dir2=",format(pat3,'03x'),"point=",point)
                            # if (self.MYDEBUG) : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
        return point[0],point[1],point[3]

    #type-S(5)
    def calcEvaluationValueIndex6(self,GameStatus,board,nextindex):
        if (self.MYDEBUG): print('block_type-S -> ',nextindex)
        direction = 0
        self.width = GameStatus["field_info"]["width"] #width=10
        self.height = GameStatus["field_info"]["height"] #height=22
        blockheight = self.maxblockheight(board)
        order = self.makehorizontalorder(blockheight)
        ypos_change = -3
    
        dic_alix = [1,0,0,0]
        # dic_aliy = [1,1,0,0]
        dic_widx = [3,2,0,0]
        # dic_widy = [2,3,0,0]

        dic_dir = [0,1,2,3]

        # x_start = 0
        # x_end = self.width-1
        # x_step = 1
        point = [-1,-1,-1,-1] #point,x,y,direction
        for y in range(self.height - 3,blockheight , -1):
            for x in order:
                pat4 = self.calcBoardPat(GameStatus["field_info"]["backboard"],x,y)
                pat3 = pat4 >> 4
                pat2 = pat4 >> 8
                nopoint = 0
                hole = 0
                direction=0
                if (x<(self.width-2))and((pat3) in self.dic_pat_dir[5][direction]):
                    basepoint = self.dic_pat_dir[5][direction][pat3]
                    # getpoint = basepoint+y*2+dic_widy[direction]-dic_aliy[direction]
                    if y>= ypos_change : getpoint = basepoint+(y*2)
                    else : getpoint = basepoint
                    if (self.MYDEBUG) : print('S(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=self.width):
                        #print('x,y,point,getpoint0=',x,y,point,getpoint)
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if (self.MYDEBUG) : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            # hole=self.counthole(board,xx,y)
                            # if (hole >=3)and(hole <=4) :
                            #     if (self.MYDEBUG) : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #     getpoint -= hole*1
                            #     if nextindex==1 and hole>=4:
                            #         if (self.MYDEBUG) : print("### Next index is I, keep 4-hole. ###")
                            #         nopoint = 1
                            #         break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if (self.MYDEBUG) : print("dir0=",format(pat3,'03x'),"point=",point)
                            # if (self.MYDEBUG) : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=1
                if (x<(self.width-1))and((pat2) in self.dic_pat_dir[5][direction]):
                    basepoint = self.dic_pat_dir[5][direction][pat2]
                    # getpoint = basepoint+y*2+dic_widy[direction]-dic_aliy[direction]
                    if y>= ypos_change : getpoint = basepoint+(y*2)
                    else : getpoint = basepoint
                    if (self.MYDEBUG) : print('S(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=self.width):
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if (self.MYDEBUG) : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            # hole=self.counthole(board,xx,y)
                            # if (hole >=3)and(hole <=4) :
                            #     if (self.MYDEBUG) : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #     getpoint -= hole*1
                            #     if nextindex==1 and hole>=4:
                            #         if (self.MYDEBUG) : print("### Next index is I, keep 4-hole. ###")
                            #         nopoint = 1
                            #         break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if (self.MYDEBUG) : print("dir1=",format(pat2,'02x'),"point=",point)
                            # if (self.MYDEBUG) : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
        return point[0],point[1],point[3]

    #type-Z(6)
    def calcEvaluationValueIndex7(self,GameStatus,board,nextindex):
        #DEBUG = 1 #OFF
        if (self.MYDEBUG): print('block_type-Z -> ',nextindex)
        direction = 0
        self.width = GameStatus["field_info"]["width"] #width=10
        self.height = GameStatus["field_info"]["height"] #height=22
        blockheight = self.maxblockheight(board)
        order = self.makehorizontalorder(blockheight)
        ypos_change = -3

        dic_alix = [1,0,0,0]
        # dic_aliy = [1,1,0,0]
        dic_widx = [3,2,0,0]
        # dic_widy = [2,3,0,0]

        dic_dir = [0,1,2,3]

        # x_start = 0
        # x_end = self.width-1
        # x_step = 1
        point = [-1,-1,-1,-1] #point,x,y,direction
        for y in range(self.height - 3,blockheight , -1):
            for x in order:
                pat4 = self.calcBoardPat(GameStatus["field_info"]["backboard"],x,y)
                pat3 = pat4 >> 4
                pat2 = pat4 >> 8
                nopoint = 0
                hole = 0
                direction=0
                if (x<(self.width-2))and((pat3) in self.dic_pat_dir[6][direction]):
                    basepoint = self.dic_pat_dir[6][direction][pat3]
                    # getpoint = basepoint+y*2+dic_widy[direction]-dic_aliy[direction]
                    if y>= ypos_change : getpoint = basepoint+(y*2)
                    else : getpoint = basepoint
                    if (self.MYDEBUG) : print('Z(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=self.width):
                        #print('x,y,point,getpoint0=',x,y,point,getpoint)
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if (self.MYDEBUG) : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            # hole=self.counthole(board,xx,y)
                            # if (hole >=3)and(hole <=4) :
                            #     if (self.MYDEBUG) : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #     getpoint -= hole*1
                            #     if nextindex==1 and hole>=4:
                            #         if (self.MYDEBUG) : print("### Next index is I, keep 4-hole. ###")
                            #         nopoint = 1
                            #         break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if (self.MYDEBUG) : print("dir0=",format(pat3,'03x'),"point=",point)
                            if (self.MYDEBUG) : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
                nopoint = 0
                hole = 0
                direction=1
                if (x<(self.width-1))and((pat2) in self.dic_pat_dir[6][direction]):
                    basepoint = self.dic_pat_dir[6][direction][pat2]
                    # getpoint = basepoint+y*2+dic_widy[direction]-dic_aliy[direction]
                    if y>= ypos_change : getpoint = basepoint+(y*2)
                    else : getpoint = basepoint
                    if (self.MYDEBUG) : print('Z(dir,x,y)=',direction,x,y,'pat4=',format(pat4,'04x'),'gp=',getpoint)
                    xxmax = x + dic_widx[direction]
                    if (((point[0]==getpoint)and(point[2]<y))or(point[0]<getpoint))and(xxmax<=self.width):
                        for xx in range(x,xxmax,1):
                            if self.checkupper(board,xx,y)==1:
                                if (self.MYDEBUG) : print('### BLOCKED BY UPPER at ',direction,xx,y)
                                nopoint = 1
                                break
                            # hole=self.counthole(board,xx,y)
                            # if (hole >=3)and(hole <=4) :
                            #     if (self.MYDEBUG) : print("### BLOCKED BY HOLE(",hole,")",x,xx,y,format(pat4,'04x'))
                            #     getpoint -= hole*1
                            #     if nextindex==1 and hole>=4:
                            #         if (self.MYDEBUG) : print("### Next index is I, keep 4-hole. ###")
                            #         nopoint = 1
                            #         break
                        if (nopoint==0):
                            point = getpoint,x+dic_alix[direction],y,dic_dir[direction]
                            if (self.MYDEBUG) : print("dir1=",format(pat2,'02x'),"point=",point)
                            # if (self.MYDEBUG) : print('(x,y)=',x,y,'pat4=',format(pat4,'04x'))
        return point[0],point[1],point[3]

    def calcBoardPat(self,board,x,y):

        pat0=0
        if x > (self.width-1) :
            pat0=15 #right
        elif x < 0:
            pat0=15 #left
        else:
            if (board[y * self.width + x]!=0)and(y>=0):
                pat0 += 8
            if (board[(y+1) * self.width + x]!=0)and(y>=-1):
                    pat0 += 4
            if (board[(y+2) * self.width + x]!=0)and(y>=-2):
                    pat0 += 2
            if  y > (self.height-4):
                    pat0 += 1 #bottom
            elif board[(y+3) * self.width + x]!=0 :
                    pat0 += 1

        pat1=0
        if x > (self.width-2) :
            pat1=15 #right
        else:
            if (board[y * self.width + (x + 1)]!=0)and(y>=0):
                pat1 += 8
            if (board[(y+1) * self.width + (x + 1)]!=0)and(y>=-1):
                pat1 += 4
            if (board[(y+2) * self.width + (x + 1)]!=0)and(y>=-2):
                pat1 += 2
            if  y > (self.height-4):
                pat1 += 1 #bottom
            elif board[(y+3) * self.width + (x + 1)]!=0 :
                pat1 += 1

        pat2=0
        if x > (self.width-3) :
            pat2=15 #right
        else:
            if (board[(y+0) * self.width + (x + 2)]!=0)and(y>=0):
                pat2 += 8
            if (board[(y+1) * self.width + (x + 2)]!=0)and(y>=-1):
                pat2 += 4
            if (board[(y+2) * self.width + (x + 2)]!=0)and(y>=-2):
                pat2 += 2
            if  y > (self.height-4):
                pat2 += 1 #bottom
            elif board[(y+3) * self.width + (x + 2)]!=0 :
                pat2 += 1
                #print("pat2+=1:::",pat2)

        pat3=0
        if x > (self.width-4) :
            pat3=15 #right
        else:
            if  (board[(y+0) * self.width + (x + 3)]!=0)and(y>=0):
                pat3 += 8
            if  (board[(y+1) * self.width + (x + 3)]!=0)and(y>=-1):
                pat3 += 4
            if  (board[(y+2) * self.width + (x + 3)]!=0)and(y>=-2):
                pat3 += 2
            if  y > (self.height-4):
                pat3 += 1 #bottom
            elif board[(y+3) * self.width + (x + 3)]!=0 :
                pat3 += 1

        pat = pat0*4096+pat1*256+pat2*16+pat3
        #DEBUG
        #print("(index,x,y,pat)=(",self.CurrentShape_index,x,y,format(pat,'04x'),")")

        return pat


if __name__ == '__main__':
    isshy=lib_tetris()
    # test for dic
    # TYPE-I
    print(isshy.dic_pat_dir[0][0]) #dir0
    print(isshy.dic_pat_dir[0][1]) #dir1
    print(isshy.dic_pat_dir[0][2]) #dir2
    print(isshy.dic_pat_dir[0][3]) #dir3
    # TYPE-L
    print(isshy.dic_pat_dir[1][0]) #dir0
    print(isshy.dic_pat_dir[1][1]) #dir1
    print(isshy.dic_pat_dir[1][2]) #dir2
    print(isshy.dic_pat_dir[1][3]) #dir3
    # TYPE-J
    print(isshy.dic_pat_dir[2][0]) #dir0
    print(isshy.dic_pat_dir[2][1]) #dir1
    print(isshy.dic_pat_dir[2][2]) #dir2
    print(isshy.dic_pat_dir[2][3]) #dir3
    # TYPE-T
    print(isshy.dic_pat_dir[3][0]) #dir0
    print(isshy.dic_pat_dir[3][1]) #dir1
    print(isshy.dic_pat_dir[3][2]) #dir2
    print(isshy.dic_pat_dir[3][3]) #dir3
    # TYPE-O
    print(isshy.dic_pat_dir[4][0]) #dir0
    print(isshy.dic_pat_dir[4][1]) #dir1
    print(isshy.dic_pat_dir[4][2]) #dir2
    # TYPE-S
    print(isshy.dic_pat_dir[5][0]) #dir0
    print(isshy.dic_pat_dir[5][1]) #dir1
    # TYPE-Z
    print(isshy.dic_pat_dir[6][0]) #dir0
    print(isshy.dic_pat_dir[6][1]) #dir1

    print('TYPE-I,dir0,pat0',isshy.dic_pat_dir[0][0][0])
    print('TYPE-I,dir0,pat0',isshy.dic_pat_dir[1][0][0])
    print('TYPE-I,dir1,pat1',isshy.dic_pat_dir[0][1][0x1333])
    print('TYPE-Z,dir0,pat0',isshy.dic_pat_dir[6][0][0x211])
    print('TYPE-Z,dir1,pat1',isshy.dic_pat_dir[6][1][0x12])

    print('dic_widx_2',isshy.dic_widx[2])

    print('dic_pat',isshy.dic_pat[1])