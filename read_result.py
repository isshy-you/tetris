import os
import pandas as pd
import json
from pygit2 import Repository

branch_list=['ish04d','ish05g6','ish05h3','ish06a','ish06b']
# branch_list=['ish04d']
DROP_INTERVAL=1
print("branch,seed,level,score,block_index,elapsed_time,line,gameover_count,line1,line2,line3,line4")
df = pd.DataFrame(columns=['branch','seed','level','score','block_index','elapsed_time',
                            'line','gameover_count','line1','line2','line3','line4']
                            )
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
            seed_max = 30
            DROP_INTERVAL = 1        # drop interval
        elif GAME_LEVEL==3:
            GAME_TIME = 999
            GAME_LINE = 180
            seed_max = 30
            DROP_INTERVAL = 1         # drop interval
        for ii in range (1,seed_max+1,1):
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
            if os.path.isfile(RESULT_LOG_JSON):
                f = open(RESULT_LOG_JSON, 'r')
                jsdic=json.load(f)
                df2 = pd.DataFrame({'branch':[branch],
                                    'seed':seed,
                                    'level':GAME_LEVEL,
                                    'score':jsdic['judge_info']['score'],
                                    'block_index':jsdic['judge_info']['block_index'],
                                    'elapsed_time':jsdic['judge_info']['elapsed_time'],
                                    'line':jsdic['judge_info']['line'],
                                    'gameover_count':jsdic['judge_info']['gameover_count'],
                                    'line1':jsdic['debug_info']['line_score_stat'][0],
                                    'line2':jsdic['debug_info']['line_score_stat'][1],
                                    'line3':jsdic['debug_info']['line_score_stat'][2],
                                    'line4':jsdic['debug_info']['line_score_stat'][3]})
                df = pd.concat([df,df2])
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
print("Saving to result.csv")
df.reset_index(drop=True, inplace=True)
df.to_csv('result.csv')
