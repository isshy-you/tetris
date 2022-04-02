import pandas as pd
import json
from pygit2 import Repository

branch_list=['ish04d','ish05g6','ish05h3','ish06a']
# branch_list=['ish04d']
DROP_INTERVAL=1
print("branch,seed,level,score,block_index,elapsed_time,line,gameover_count,line1,line2,line3,line4")
for branch in branch_list:
    for GAME_LEVEL in [1,2,3]:
        if GAME_LEVEL==1:
            GAME_TIME = 999
            GAME_LINE = 180
            seed_max = 1
            DROP_INTERVAL = 1        # drop interval
        elif GAME_LEVEL==2:
            GAME_TIME = 999
            GAME_LINE = 180
            seed_max = 10
            DROP_INTERVAL = 1        # drop interval
        elif GAME_LEVEL==3:
            GAME_TIME = 999
            GAME_LINE = 180
            seed_max = 10
            DROP_INTERVAL = 1         # drop interval
        for ii in range (0,seed_max,1):
            if GAME_LEVEL==1:
                seed = -1
            else:
                seed = ii
            RESULT_LOG_JSON = "result/"+branch\
                                +"_"+str(GAME_LEVEL)\
                                +"_"+str(GAME_TIME)\
                                +"_"+str(GAME_LINE)\
                                +"_"+str(DROP_INTERVAL)\
                                +"_"+str(seed)\
                                +".json"
            f = open(RESULT_LOG_JSON, 'r')
            jsdic=json.load(f)
            print(  branch+',',seed,',',
                    GAME_LEVEL,',',
                    jsdic['judge_info']['score'],',',
                    jsdic['judge_info']['block_index'],',',
                    jsdic['judge_info']['elapsed_time'],',',
                    jsdic['judge_info']['line'],',',
                    jsdic['judge_info']['gameover_count'],',',
                    jsdic['debug_info']['line_score_stat'][0],',',
                    jsdic['debug_info']['line_score_stat'][1],',',
                    jsdic['debug_info']['line_score_stat'][2],',',
                    jsdic['debug_info']['line_score_stat'][3],',',
                    # jsdic['debug_info']['line_score']['line1'],',',
                    # jsdic['debug_info']['line_score']['line2'],',',
                    # jsdic['debug_info']['line_score']['line3'],',',
                    # jsdic['debug_info']['line_score']['line4'],',',
                    # jsdic['debug_info']['line_score']['gameover'],',',
                    )
