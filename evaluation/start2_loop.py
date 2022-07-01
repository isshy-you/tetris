#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import subprocess
from argparse import ArgumentParser
from pygit2 import Repository

def get_option(game_level, game_time, mode, random_seed, drop_interval, resultlogjson, train_yaml, predict_weight, user_name, ShapeListMax, BlockNumMax):
    argparser = ArgumentParser()
    argparser.add_argument('-l', '--game_level', type=int,
                            default=game_level,
                            help='Specify game level')
    argparser.add_argument('-t', '--game_time', type=int,
                            default=game_time,
                            help='Specify game time(s), if specify -1, do endless loop')
    argparser.add_argument('-m', '--mode', type=str,
                            default=mode,
                            help='Specify mode (keyboard/gamepad/sample/train/predict/train_sample/predict_sample/train_sample2/predict_sample2) if necessary')
    argparser.add_argument('-r', '--random_seed', type=int,
                            default=random_seed,
                            help='Specify random seed if necessary') 
    argparser.add_argument('-d', '--drop_interval', type=int,
                            default=drop_interval,
                            help='Specify drop interval (msec) if necessary') 
    argparser.add_argument('-f', '--resultlogjson', type=str,
                            default=resultlogjson,
                            help='Specigy result log file path if necessary')
    argparser.add_argument('--train_yaml', type=str,
                            default=train_yaml,
                            help='yaml file for machine learning')
    argparser.add_argument('--predict_weight', type=str,
                            default=predict_weight,
                            help='weight file for machine learning')
    argparser.add_argument('-u', '--user_name', type=str,
                            default=user_name,
                            help='Specigy user name if necessary')
    argparser.add_argument('--ShapeListMax', type=int,
                            default=ShapeListMax,
                            help='Specigy ShapeListMax if necessary')
    argparser.add_argument('--BlockNumMax', type=int,
                            default=BlockNumMax,
                            help='Specigy BlockNumMax if necessary')
    return argparser.parse_args()

def get_python_cmd():
    ret = subprocess.run("python --version", shell=True, \
                         stderr=subprocess.PIPE, encoding="utf-8")
    print(ret)
    if "Python 2" in ret.stderr:
        return "python3"
    return "python"


def start():
    ## define
    EXEC_LOG_ON = 1    
    SEED_FIX = 0
    ## default value
    GAME_LEVEL = 3
    GAME_TIME = 180
    IS_MODE = "default"
    IS_SAMPLE_CONTROLL = "n"
    INPUT_RANDOM_SEED = 1
    DROP_INTERVAL = 1        # drop interval
    RESULT_LOG_JSON = "result.json"
    USER_NAME = "window_sample"
    SHAPE_LIST_MAX = 6
    BLOCK_NUM_MAX = 1000
    TRAIN_YAML = "config/default.yaml"
    PREDICT_WEIGHT = "outputs/latest/best_weight.pt"

    branch_list=['master','master_seigot','ish05h3']

    repo = Repository('.git')
    for branch_name in branch_list:
        # branch = repo.lookup_branch(branch_name)
        # ref = repo.lookup_reference(branch.name)
        # repo.checkout(ref)
        # print('branch=',Repository('.').head.shorthand)
        cmd = 'git checkout '+branch_name+' ./game_manager/block_controller.py'
        print('cmd : '+cmd)
        ret = subprocess.run(cmd, shell=True)
        if ret.returncode != 0:
            print('error: subprocess failed.', file=sys.stderr)
            sys.exit(1)
        for GAME_LEVEL in [1,2,3]:
            if GAME_LEVEL==1:
                GAME_TIME = 999
                BLOCK_NUM_MAX = 180
                seed_max = 1
                DROP_INTERVAL = 1        # drop interval
            elif GAME_LEVEL==2:
                GAME_TIME = 999
                BLOCK_NUM_MAX = 180
                seed_max = 10
                DROP_INTERVAL = 1        # drop interval
            elif GAME_LEVEL==3:
                GAME_TIME = 30
                BLOCK_NUM_MAX = -1
                seed_max = 10
                DROP_INTERVAL = 1         # drop interval
            for ii in range(1,seed_max+1,1):
                result_name = branch_name.replace('/','-').replace('_','-')\
                            +"_"+f'{GAME_LEVEL:1}'\
                            +"_"+f'{GAME_TIME:03}'\
                            +"_"+f'{BLOCK_NUM_MAX:04}'\
                            +"_"+f'{DROP_INTERVAL:03}'\
                            +"_"+f'{INPUT_RANDOM_SEED:+03}'\
                            +"_"+f'{ii:03}'
                if GAME_LEVEL==1:
                    INPUT_RANDOM_SEED = -1
                else:
                    if SEED_FIX == 1:
                        INPUT_RANDOM_SEED = ii
                    else:
                        INPUT_RANDOM_SEED = -1
                ## update value if args are given
                args = get_option(GAME_LEVEL,
                                GAME_TIME,
                                IS_MODE,
                                INPUT_RANDOM_SEED,
                                DROP_INTERVAL,
                                '', # RESULT_LOG_JSON,
                      TRAIN_YAML,
                      PREDICT_WEIGHT,
                      USER_NAME,
                      SHAPE_LIST_MAX,
                      BLOCK_NUM_MAX)
                if args.game_level >= 0:
                    GAME_LEVEL = args.game_level
                if args.game_time >= 0 or args.game_time == -1:
                    GAME_TIME = args.game_time
                if args.mode in ("keyboard", "gamepad", "sample", "train", "predict", "train_sample", "predict_sample"):
                    IS_MODE = args.mode
                if args.random_seed >= 0:
                    INPUT_RANDOM_SEED = args.random_seed
                if args.drop_interval > 0:
                    DROP_INTERVAL = args.drop_interval
                if len(args.resultlogjson) != 0:
                    RESULT_LOG_JSON = args.resultlogjson
                else:
                    # RESULT_LOG_JSON = "result/"+Repository('.').head.shorthand\
                    RESULT_LOG_JSON = "result/"+result_name+".json"
                if len(args.user_name) != 0:
                    USER_NAME = args.user_name
                if args.ShapeListMax > 1:
                    SHAPE_LIST_MAX = args.ShapeListMax
                if args.BlockNumMax > 1:
                    BLOCK_NUM_MAX = args.BlockNumMax
                if len(args.train_yaml) != 0:
                    TRAIN_YAML = args.train_yaml
                if args.predict_weight != None:
                    PREDICT_WEIGHT = args.predict_weight

                ## set field parameter for level 1
                RANDOM_SEED = 0            # random seed for field
                OBSTACLE_HEIGHT = 0        # obstacle height (blocks)
                OBSTACLE_PROBABILITY = 0   # obstacle probability (percent)

                ## update field parameter level
                if GAME_LEVEL == 0:   # level0
                    GAME_TIME = -1
                elif GAME_LEVEL == 1: # level1
                    RANDOM_SEED = 0
                elif GAME_LEVEL == 2: # level2
                    RANDOM_SEED = -1
                elif GAME_LEVEL == 3: # level3
                    RANDOM_SEED = -1
                    OBSTACLE_HEIGHT = 10
                    OBSTACLE_PROBABILITY = 40
                else:
                    print('invalid level: ' + str(GAME_LEVEL), file=sys.stderr)
                    sys.exit(1)

                ## update random seed
                if INPUT_RANDOM_SEED >= 0:
                    RANDOM_SEED = INPUT_RANDOM_SEED

                ## print
                print('branch:' + branch_name)
                print('game_level: ' + str(GAME_LEVEL))
                print('game_time: ' + str(GAME_TIME))
                print('RANDOM_SEED: ' + str(RANDOM_SEED))
                print('BLOCK_NUM_MAX: ' + str(BLOCK_NUM_MAX))
                print('IS_MODE :' + str(IS_MODE))
                print('OBSTACLE_HEIGHT: ' + str(OBSTACLE_HEIGHT))
                print('OBSTACLE_PROBABILITY: ' + str(OBSTACLE_PROBABILITY))
                print('USER_NAME: ' + str(USER_NAME))
                print('SHAPE_LIST_MAX: ' + str(SHAPE_LIST_MAX))
                print('RESULT_LOG_JSON: ' + str(RESULT_LOG_JSON))
                print('TRAIN_YAML: ' + str(TRAIN_YAML))
                print('PREDICT_WEIGHT: ' + str(PREDICT_WEIGHT))

                os.makedirs('result', exist_ok=True)
                ## start game
                PYTHON_CMD = get_python_cmd()
                cmd = PYTHON_CMD + ' ' + 'game_manager/game_manager.py' \
			        + ' ' + '--game_time' + ' ' + str(GAME_TIME) \
			        + ' ' + '--seed' + ' ' + str(RANDOM_SEED) \
			        + ' ' + '--obstacle_height' + ' ' + str(OBSTACLE_HEIGHT) \
			        + ' ' + '--obstacle_probability' + ' ' + str(OBSTACLE_PROBABILITY) \
			        + ' ' + '--drop_interval' + ' ' + str(DROP_INTERVAL) \
			        + ' ' + '--mode' + ' ' + str(IS_MODE) \
			        + ' ' + '--user_name' + ' ' + str(USER_NAME) \
			        + ' ' + '--resultlogjson' + ' ' + str(RESULT_LOG_JSON) \
			        + ' ' + '--ShapeListMax' + ' ' + str(SHAPE_LIST_MAX) \
			        + ' ' + '--ShapeListMax' + ' ' + str(SHAPE_LIST_MAX) \
			        + ' ' + '--train_yaml' + ' ' + str(TRAIN_YAML) \
			        + ' ' + '--predict_weight' + ' ' + str(PREDICT_WEIGHT) \
			        + ' ' + '--BlockNumMax' + ' ' + str(BLOCK_NUM_MAX)

                if EXEC_LOG_ON==1:
                    # EXEC_LOG = "result/"+Repository('.').head.shorthand\
                    EXEC_LOG = "result/"+result_name+".log"
                    cmd = cmd + ' ' + '>'+EXEC_LOG

                ret = subprocess.run(cmd, shell=True)
                if ret.returncode != 0:
                    print('error: subprocess failed.', file=sys.stderr)
                    sys.exit(1)
                #p = subprocess.Popen(cmd, shell=True)
                #try:
                #    p.wait()
                #except KeyboardInterrupt:
                #    print("KeyboardInterrupt, call p.terminate()")
                #    p.terminate()

    cmd = 'git restore ./game_manager/block_controller.py'
    print('cmd : '+cmd)
    ret = subprocess.run(cmd, shell=True)
    if ret.returncode != 0:
        print('error: subprocess failed.', file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    start()
