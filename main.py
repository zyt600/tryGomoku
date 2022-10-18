Skip to content
Search or jump to…
Pull requests
Issues
Marketplace
Explore
 
@pigpeach 
zyt600
/
try-python
Private
Code
Issues
Pull requests
Actions
Projects
Security
Insights
try-python/main.py /
@zyt600
zyt600 Update main.py
Latest commit 1fd20a2 3 minutes ago
 History
 2 contributors
@zyt600@pigpeach
363 lines (292 sloc)  12.7 KB

"""黑方先行，为1，白方为-1，空棋盘为0，边界为2，
天元即棋盘的最中心，在board_17x17棋盘的（8，8）,在被打印出的棋盘中位置为(7,7)"""
board_17x17 = [[0 for i in range(17)] for j in range(17)]
EMPTY = 0
BLACK = 1
WHITE = -1
BOUNDARY = 2
UP = 3  # 定义方向常量，上
DOWN = 4  # 定义方向常量，下
LEFT_UP = 5  # 定义方向常量，左上
RIGHT_UP = 6  # 定义方向常量，右上
LEFT = 7  # 定义方向常量，左
RIGHT = 8  # 定义方向常量，右
LEFT_DOWN = 9  # 定义方向常量，左下
RIGHT_DOWN = 10  # 定义方向常量，右下
DIRECTION_LIST = [[0, 1], [0, -1], [-1, 1], [1, 1], [-1, 0], [1, 0], [-1, -1], [1, -1]]
MY_COLOR = 0
ENEMY_COLOR = 0


class SearchResult:
    """搜索结果类，包含搜索方向、颜色、棋子连成的长度、是否有空格、是否有障碍"""
    direction = -1
    myColor = 0  # 正在搜索的颜色颜色
    myLen = 0  # 表示我方连续棋子的长度
    emptyNum = 0  # 遇到的空格子数量，不难发现最多唯一
    barrierNum = 0  # 遇到的障碍（对方棋子、棋盘边界）数量，不难发现最多唯一

    def __init__(self, direction, myColor, myLen, emptyNum, barrierNum):
        self.direction = direction
        self.barrierNum = barrierNum
        self.emptyNum = emptyNum
        self.myColor = myColor
        self.myLen = myLen

def searchable(row, col):
    """判断(row,col)是否在棋盘内"""
    if row <= 0 or col <= 0 or row >= 16 or col >= 16:
        return False
    if board_17x17[row][col]==BLACK or board_17x17[row][col]==WHITE:
        return False
    return True


def printBoard():
    """输出整个棋盘"""
    for i in range(15, 0, -1):
        # print('\033[30;40mb\033[0m', end=' ')
        #
        # print("\033[31m这是红色字体\033[0m")
        print("%02d:" % (i - 1), end=' ')
        ##$##输出横索引
        for j in range(1, 17):
            if board_17x17[i][j] == BLACK:
                print('\033[30;40mb\033[0m', end=' ')
            elif board_17x17[i][j] == WHITE:
                print('\033[37;47mw\033[0m', end=' ')
            else:
                print('0', end=' ')
        print()


def search_along(direction, row, col, myColor):
    """沿着direction方向递归搜索，返回一个SearchResult类"""
    row += DIRECTION_LIST[direction - 3][1];
    col += DIRECTION_LIST[direction - 3][0];
    if row <= 0 or col <= 0 or row >= 16 or col >= 16:  # 边界检查
        re = SearchResult(direction, myColor, 0, 0, 1)
        return re
    elif board_17x17[row][col] == myColor * -1 or board_17x17[row][col] == 2:  # 碰壁（边界或对方棋子）的情况
        re = SearchResult(direction, myColor, 0, 0, 1)
        return re
    elif board_17x17[row][col] == 0:  # 空棋盘情况
        re = SearchResult(direction, myColor, 0, 1, 0)
        return re
    # 有我方棋子情况，注意返回值
    result = search_along(direction, row + DIRECTION_LIST[direction - 3][1], col + DIRECTION_LIST[direction - 3][0], myColor)
    result.myLen += 1
    return result


def import_board_17x17():
    f = open("board17x17.txt", "r+")
    for i in range(17):
        line = f.readline()
        for j in range(17):
            if line[j] == '0':
                board_17x17[i][j] = 0
            elif line[j] == '2':
                board_17x17[i][j] = 2
            elif line[j] == 'b':
                board_17x17[i][j] = BLACK
            elif line[j] == 'w':
                board_17x17[i][j] = WHITE
            else:
                print("import board error!\n")
                return
    print("finish importing\n")
    return


class importantStructureHere:
    """这一个点所能够形成的各类棋型的数量"""
    live3 = 0
    died3 = 0

    live4 = 0
    died4 = 0

    live5 = 0

    live2 = 0
    died2 = 0

    def __init__(self, l3=0, d3=0, l4=0, d4=0, l5=0, l2=0, d2=0):
        self.live2 = l2
        self.live3 = l3
        self.live4 = l4
        self.live5 = l5

        self.died2 = d2
        self.died3 = d3
        self.died4 = d4

def searchImportantStructure(row,col,mycolor):
    """搜索如果落子在(row,col)所能形成的重要性"""
#     TODO:朱涛,通过search_along函数的返回值判断形成的各个importantStructureHere结构的数量,返回一个importantStructureHere结构
    reup =search_along(UP, row, col, mycolor)
    redown =search_along(DOWN, row, col, mycolor)
    relu=search_along(LEFT_UP, row, col, mycolor)
    reru=search_along(RIGHT_UP, row, col, mycolor)
    releft=search_along(LEFT, row, col, mycolor)
    reright=search_along(RIGHT, row, col, mycolor)
    reld=search_along(LEFT_DOWN, row, col, mycolor)
    rerd=search_along(RIGHT_DOWN, row, col, mycolor)

# 八个方向八个类，通过类成员的运算判定出所形成的棋子类型
    l3=int(reup.myLen+redown.myLen >=2 and reup.emptyNum + redown.emptyNum==2)\
       +int(releft.myLen+reright.myLen >=2 and releft.emptyNum + reright.emptyNum==2)\
       +int(reru.myLen+reld.myLen >=2 and reru.emptyNum + reld.emptyNum==2)\
       +int(rerd.myLen+relu.myLen >=2 and rerd.emptyNum + relu.emptyNum==2)

    d3=int(reup.myLen+redown.myLen >=2)+int(releft.myLen+reright.myLen >=2)+int(reru.myLen+reld.myLen >=2)+int(rerd.myLen+relu.myLen >=2)

    l4=int(reup.myLen+redown.myLen >=3 and reup.emptyNum + redown.emptyNum==2)\
       +int(releft.myLen+reright.myLen >=3 and releft.emptyNum + reright.emptyNum==2)\
       +int(reru.myLen+reld.myLen >=3 and reru.emptyNum + reld.emptyNum==2)\
       +int(rerd.myLen+relu.myLen >=3 and rerd.emptyNum + relu.emptyNum==2)

    d4=int(reup.myLen+redown.myLen >=3)+int(releft.myLen+reright.myLen >=3)+int(reru.myLen+reld.myLen >=3)+int(rerd.myLen+relu.myLen >=3)

    l5=int(reup.myLen+redown.myLen >=4)+int(releft.myLen+reright.myLen >=4)+int(reru.myLen+reld.myLen >=4)+int(rerd.myLen+relu.myLen >=4)


    l2 = int(reup.myLen==1 and reup.emptyNum==1) +int(redown.myLen==1 and redown.emptyNum==1) + int(relu.myLen==1 and relu.emptyNum==1) \
       + int(reru.myLen == 1 and reru.emptyNum == 1)+int(releft.myLen==1 and releft.emptyNum==1)+int(reright.myLen==1 and reright.emptyNum==1) \
       + int(reld.myLen == 1 and reld.emptyNum == 1)+int(rerd.myLen==1 and rerd.emptyNum == 1)


    d2 = int(reup.myLen==1 and reup.emptyNum==0)+int(redown.myLen==1 and redown.emptyNum==0)+int(relu.myLen==1 and relu.emptyNum==0) \
       + int(reru.myLen == 1 and reru.emptyNum == 0)+int(releft.myLen==1 and releft.emptyNum==0)+int(reright.myLen==1 and reright.emptyNum==0) \
       + int(reld.myLen == 1 and reld.emptyNum == 0)+int(rerd.myLen==1 and rerd.emptyNum==0)


#传参到importantSructureHere中
    imS=importantStructureHere(l3, d3, l4, d4, l5, l2, d2)
    return imS





def Mycolor_calImportance(importantStructureHere):
    """以一个importantStructureHere为参数,返回一个整,代表这个点的重要性数值"""
#     TODO:朱涛,选择合适的权重
    if importantStructureHere.live5 >=1:
        return 10001
    elif importantStructureHere.live4 >=1:
        return 8888
    elif importantStructureHere.live3 >=1:
        return 7777
    elif importantStructureHere.live2 >=1:
        return 5555
    elif importantStructureHere.died4 >=1:
        return 6666
    elif importantStructureHere.died3 >=1:
        return 4444
    elif importantStructureHere.died2 >=1:
        return 3333
    else:
        return 1111


def Enemy_color_calImportance(importantStructureHere):
    if importantStructureHere.live5 >= 1:
        return 10000
    elif importantStructureHere.live4 >= 1:
        return 8887
    elif importantStructureHere.live3 >= 1:
        return 7776
    elif importantStructureHere.live2 >= 1:
        return 5554
    elif importantStructureHere.died4 >= 1:
        return 6665
    elif importantStructureHere.died3 >= 1:
        return 4443
    elif importantStructureHere.died2 >= 1:
        return 3332
    else:
        return 1110


import_board_17x17()
printBoard()
# for ii in range(17):  # 设置棋盘边界
#     board_17x17[ii][0] = 2
#     board_17x17[0][ii] = 2
#     board_17x17[ii][16] = 2
#     board_17x17[16][ii] = 2

MyscoreBoard=[[0 for x1 in (range(17))]for y1 in range(17)]
EnemyscoreBoard=[[0 for x2 in (range(17))]for y2 in range(17)]
mymax=0
enemymax=0
myx=0
myy=0
eny=0
enx=0


#我方和敌人的得分列表

stringColor = input("请输入我方是 黑 还是 白")
if stringColor == "黑":
    MY_COLOR = BLACK
    ENEMY_COLOR = WHITE
    print("以最左下角可落子处为（0，0），我方第一步落子于（7，7）")
    board_17x17[8][8] = BLACK
    printBoard()

    enemyWhite = input("请输入白棋落子位置，以空格分开")
    enemyRow, enemyCol = enemyWhite.split(" ")
    enemyRow = int(enemyRow) + 1
    enemyCol = int(enemyCol) + 1
    board_17x17[enemyRow][enemyCol] = ENEMY_COLOR
    printBoard()

    if enemyRow == 9 and enemyCol == 9:
        board_17x17[11][5] = BLACK
        print("落子于10,4")
    elif enemyRow == 7 and enemyCol == 7:
        board_17x17[11][5] = BLACK
        print("落子于10,4")
    elif enemyRow == 10 and enemyCol == 10:
        board_17x17[11][5] = BLACK
        print("落子于10,4")
    else:
        board_17x17[11][11] = BLACK
        print("落子于10,10")

    printBoard()


    while True:
        enemyWhite = input("请输入白棋落子位置，以空格分开")
        enemyRow, enemyCol = enemyWhite.split(" ")
        enemyRow = int(enemyRow) + 1
        enemyCol = int(enemyCol) + 1
        board_17x17[enemyRow][enemyCol] = ENEMY_COLOR

        # for row in range(15, 0, -1):
        #     for col in range(15, 0, -1):
        #         if board_17x17[row][col]!=BLACK and board_17x17[row][col] !=WHITE:
        #             imSmy=searchImportantStructure(row, col, MY_COLOR)
        #             MyscoreBoard[row][col]=Mycolor_calImportance(imSmy)
        #             imSen = searchImportantStructure(row, col, ENEMY_COLOR)
        #             EnemyscoreBoard[row][col]=Enemy_color_calImportance(imSen)

        imSmy = searchImportantStructure(9, 9, MY_COLOR)



        for row in range(15, 0, -1):
            for col in range(15, 0, -1):
                if MyscoreBoard[row][col]>=mymax:
                    mymax=MyscoreBoard[row][col]
                    myx=row
                    myy=col
                    print("aaa",mymax,myx,myy)

        for row in range(15, 0, -1):
            for col in range(15, 0, -1):
                if EnemyscoreBoard[row][col] >= mymax:
                    enemymanx = EnemyscoreBoard[row][col]
                    enx = row
                    eny = col


        if MyscoreBoard[myx][myy]>=EnemyscoreBoard[enx][eny]:
            board_17x17[myx][myy] = BLACK
        else:
            board_17x17[enx][eny] = BLACK

        # TODO:朱涛通过一些方法,输出黑棋应当落子的位置
        # 比如搜索附近的所有点的推荐值
        printBoard()
        # print(MyscoreBoard)
        # print(EnemyscoreBoard)

        MyscoreBoard = [[0 for x1 in (range(17))] for y1 in range(17)]
        EnemyscoreBoard = [[0 for x2 in (range(17))] for y2 in range(17)]




#我方是白棋子
else:
    MY_COLOR = WHITE
    ENEMY_COLOR = BLACK
    # TODO:白棋同理于黑棋,输出推荐落子
    while True:
        enemyWhite = input("请输入黑棋落子位置，以空格分开")
        enemyRow, enemyCol = enemyWhite.split(" ")
        enemyRow = int(enemyRow) + 1
        enemyCol = int(enemyCol) + 1
        board_17x17[enemyRow][enemyCol] = ENEMY_COLOR


        searchList=[]#存储可搜索,离得近,应当被搜索的点的元组列表 注意:!!!这里的坐标是数组下标而非用户输入输出的数字
        for row in range(15, 0, -1):
            for col in range(15, 0, -1):
                if board_17x17[row][col]!=BLACK and board_17x17[row][col] !=WHITE:
                    imSmy=searchImportantStructure(row, col, MY_COLOR)
                    MyscoreBoard[row][col]=Mycolor_calImportance(imSmy)
                    imSen = searchImportantStructure(row, col, ENEMY_COLOR)
                    EnemyscoreBoard[row][col]=Enemy_color_calImportance(imSen)


        for row in range(15, 0, -1):
            for col in range(15, 0, -1):
                if MyscoreBoard[row][col]>=mymax:
                    mymax=MyscoreBoard[row][col]
                    myx=row
                    myy=col

        for row in range(15, 0, -1):
            for col in range(15, 0, -1):
                if EnemyscoreBoard[row][col] >= mymax:
                    enemymanx = EnemyscoreBoard[row][col]
                    enx = row
                    eny = col


        if MyscoreBoard[myx][myy]>EnemyscoreBoard[enx][eny]:
            board_17x17[myx][myy] = WHITE
        else:
            board_17x17[enx][eny] = WHITE

        MyscoreBoard = [[0 for x1 in (range(17))] for y1 in range(17)]
        EnemyscoreBoard = [[0 for x2 in (range(17))] for y2 in range(17)]


        printBoard()
Footer
© 2022 GitHub, Inc.
Footer navigation
Terms
Privacy
Security
Status
Docs
Contact GitHub
Pricing
API
Training
Blog
About
