"""黑方先行，为1，白方为-1，空棋盘为0，边界为2，
天元即棋盘的最中心，在board_17x17棋盘的（8，8）,在被打印出的棋盘中位置为(7,7)"""
from usefulHEAD import *
from structureWeight import *

board_17x17 = [[0 for i in range(17)] for j in range(17)]

MY_COLOR = 0
ENEMY_COLOR = 0
ZYT_TEST = True  # 是否输出测试内容
IF_IMPORT_BOARD = False  # 是否使用导入棋盘，还是初始化空棋盘


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
    """判断(row,col)是否在棋盘内,并且可以被搜索"""
    if row <= 0 or col <= 0 or row >= 16 or col >= 16:
        return False
    if board_17x17[row][col] == BLACK or board_17x17[row][col] == WHITE:
        return False
    return True


def printBoard():
    """输出整个棋盘"""
    for i in range(15, 0, -1):
        # 输出行索引
        print("\033[31m%02d\033[0m:" % (i - 1), end=' ')

        for j in range(1, 16):
            if board_17x17[i][j] == BLACK:
                print('\033[30;40mb\033[0m', end='  ')
            elif board_17x17[i][j] == WHITE:
                print('\033[37;47mw\033[0m', end='  ')
            else:
                print(board_17x17[i][j], end='  ')
        print()
    # 输出列索引
    print("    ", end='')
    for i in range(10):
        print("\033[31m%d\033[0m" % i, end='  ', sep='')
    for i in range(10, 15):
        print("\033[31m%d\033[0m" % i, end=' ', sep='')
    print()


def search_along(direction, row, col, myColor, first=True):
    """沿着direction方向递归搜索，返回一个SearchResult类"""
    if first:
        row += DIRECTION_LIST[direction - 3][1]
        col += DIRECTION_LIST[direction - 3][0]
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
    result = search_along(direction, row + DIRECTION_LIST[direction - 3][1], col + DIRECTION_LIST[direction - 3][0],
                          myColor, False)
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
    # TODO :朱涛：如果有必要，加进去更多形状结构，不过大概率不用了
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


def searchImportantStructure(row, col, mycolor):
    """搜索如果落子在(row,col)所能形成的重要性"""
    reup = search_along(UP, row, col, mycolor)
    redown = search_along(DOWN, row, col, mycolor)
    relu = search_along(LEFT_UP, row, col, mycolor)
    reru = search_along(RIGHT_UP, row, col, mycolor)
    releft = search_along(LEFT, row, col, mycolor)
    reright = search_along(RIGHT, row, col, mycolor)
    reld = search_along(LEFT_DOWN, row, col, mycolor)
    rerd = search_along(RIGHT_DOWN, row, col, mycolor)

    # 八个方向八个类，通过类成员的运算判定出所形成的棋子类型
    l3 = int(reup.myLen + redown.myLen >= 2 and reup.emptyNum + redown.emptyNum == 2) \
         + int(releft.myLen + reright.myLen >= 2 and releft.emptyNum + reright.emptyNum == 2) \
         + int(reru.myLen + reld.myLen >= 2 and reru.emptyNum + reld.emptyNum == 2) \
         + int(rerd.myLen + relu.myLen >= 2 and rerd.emptyNum + relu.emptyNum == 2)

    d3 = int(reup.myLen + redown.myLen >= 2) + int(releft.myLen + reright.myLen >= 2) + int(
        reru.myLen + reld.myLen >= 2) + int(rerd.myLen + relu.myLen >= 2)

    l4 = int(reup.myLen + redown.myLen >= 3 and reup.emptyNum + redown.emptyNum == 2) \
         + int(releft.myLen + reright.myLen >= 3 and releft.emptyNum + reright.emptyNum == 2) \
         + int(reru.myLen + reld.myLen >= 3 and reru.emptyNum + reld.emptyNum == 2) \
         + int(rerd.myLen + relu.myLen >= 3 and rerd.emptyNum + relu.emptyNum == 2)

    d4 = int(reup.myLen + redown.myLen >= 3) + int(releft.myLen + reright.myLen >= 3) + int(
        reru.myLen + reld.myLen >= 3) + int(rerd.myLen + relu.myLen >= 3)

    l5 = int(reup.myLen + redown.myLen >= 4) + int(releft.myLen + reright.myLen >= 4) + int(
        reru.myLen + reld.myLen >= 4) + int(rerd.myLen + relu.myLen >= 4)

    l2 = int(reup.myLen == 1 and reup.emptyNum == 1) + int(redown.myLen == 1 and redown.emptyNum == 1) + int(
        relu.myLen == 1 and relu.emptyNum == 1) \
         + int(reru.myLen == 1 and reru.emptyNum == 1) + int(releft.myLen == 1 and releft.emptyNum == 1) + int(
        reright.myLen == 1 and reright.emptyNum == 1) \
         + int(reld.myLen == 1 and reld.emptyNum == 1) + int(rerd.myLen == 1 and rerd.emptyNum == 1)

    d2 = int(reup.myLen == 1 and reup.emptyNum == 0) + int(redown.myLen == 1 and redown.emptyNum == 0) + int(
        relu.myLen == 1 and relu.emptyNum == 0) \
         + int(reru.myLen == 1 and reru.emptyNum == 0) + int(releft.myLen == 1 and releft.emptyNum == 0) + int(
        reright.myLen == 1 and reright.emptyNum == 0) \
         + int(reld.myLen == 1 and reld.emptyNum == 0) + int(rerd.myLen == 1 and rerd.emptyNum == 0)

    # 传参到importantSructureHere中
    imS = importantStructureHere(l3, d3, l4, d4, l5, l2, d2)
    return imS


def Mycolor_calImportance(importantStructureHere):
    """以一个importantStructureHere为参数,返回一个整数,代表这个点的重要性数值"""
    sum = 0
    sum += importantStructureHere.live5 * mylive5weight
    sum += importantStructureHere.live4 * mylive4weight
    sum += importantStructureHere.live3 * mylive3weight
    sum += importantStructureHere.died4 * mydie4weight
    sum += importantStructureHere.live2 * mylive2weight
    sum += importantStructureHere.died3 * mydie3weight
    sum += importantStructureHere.died2 * mydie2weight

    return sum


def Enemy_color_calImportance(importantStructureHere):
    """以一个importantStructureHere为参数,返回一个整数,代表这个点的重要性数值"""
    sum = 1
    sum += importantStructureHere.live5 * enemylive5weight
    sum += importantStructureHere.live4 * enemylive4weight
    sum += importantStructureHere.live3 * enemylive3weight
    sum += importantStructureHere.died4 * enemydie4weight
    sum += importantStructureHere.live2 * enemylive2weight
    sum += importantStructureHere.died3 * enemydie3weight
    sum += importantStructureHere.died2 * enemydie2weight

    return sum


if IF_IMPORT_BOARD:
    import_board_17x17()
else:
    for ii in range(17):  # 设置棋盘边界
        board_17x17[ii][0] = 2
        board_17x17[0][ii] = 2
        board_17x17[ii][16] = 2
        board_17x17[16][ii] = 2
printBoard()

MyscoreBoard = [[0 for x1 in (range(17))] for y1 in range(17)]
EnemyscoreBoard = [[0 for x2 in (range(17))] for y2 in range(17)]
myx = 0
myy = 0

# 我方和敌人的得分列表
stringColor = input("请输入我方是 黑(h) 还是 白：")
if stringColor == "黑" or stringColor == "h":
    MY_COLOR = BLACK
    ENEMY_COLOR = WHITE

    # 我方第一步
    print("以最左下角可落子处为（0，0），我方第一步落子于（7，7）")
    board_17x17[8][8] = BLACK
    printBoard()

    enemyWhite = input("请输入白棋落子位置，以空格分开")
    enemyRow, enemyCol = enemyWhite.split(" ")
    enemyRow = int(enemyRow) + 1
    enemyCol = int(enemyCol) + 1
    board_17x17[enemyRow][enemyCol] = ENEMY_COLOR
    printBoard()

    # 我方第二步
    if (enemyRow == 9 and enemyCol == 9) or (enemyRow == 10 and enemyCol == 10) or (
            enemyRow == 11 and enemyCol == 11) or (enemyRow == 7 and enemyCol == 7) \
            or (enemyRow == 9 and enemyCol == 8) or (enemyRow == 7 and enemyCol == 8) \
            or (enemyRow == 8 and enemyCol == 7) or (enemyRow == 8 and enemyCol == 9):
        board_17x17[11][5] = BLACK
        print("落子于10,4")
        secondStep = (11, 5)

    else:
        board_17x17[11][11] = BLACK
        print("落子于10,10")
        secondStep = (11, 11)
    printBoard()

    # 我方第三步
    myStepNum = 2  # myStepNum为我方该下哪一步了
    while True:
        # 初始化
        myStepNum += 1

        enemyWhite = input("请输入白棋落子位置，以空格分开")
        enemyRow, enemyCol = enemyWhite.split(" ")
        enemyRow = int(enemyRow) + 1
        enemyCol = int(enemyCol) + 1
        board_17x17[enemyRow][enemyCol] = ENEMY_COLOR

        MyscoreBoard = [[0 for x1 in (range(17))] for y1 in range(17)]
        EnemyscoreBoard = [[0 for x2 in (range(17))] for y2 in range(17)]

        for row in range(15, 0, -1):
            for col in range(15, 0, -1):
                if board_17x17[row][col] == 0:
                    imSmy = searchImportantStructure(row, col, MY_COLOR)
                    MyscoreBoard[row][col] = Mycolor_calImportance(imSmy)
                    imSen = searchImportantStructure(row, col, ENEMY_COLOR)
                    EnemyscoreBoard[row][col] = Enemy_color_calImportance(imSen)
        mymax = 0
        # if myStepNum

        if myStepNum <= 10:  # 如果步数小，前几步进行手工推荐部分落子点
            recommandNum1 = 9e7
            # recommandNum2 = 8e7
            if secondStep == (11, 5):
                MyscoreBoard[10][6] += mydie4weight
                if board_17x17[8][7] != ENEMY_COLOR:
                    if board_17x17[8][9] != ENEMY_COLOR:
                        MyscoreBoard[8][6] = recommandNum1
                    MyscoreBoard[9][5] = recommandNum1
                    MyscoreBoard[8][5] *= 200
                elif board_17x17[9][8] != ENEMY_COLOR:
                    MyscoreBoard[10][8] = recommandNum1
                    MyscoreBoard[11][7] = recommandNum1
                    MyscoreBoard[11][8] *= 200
            else:
                MyscoreBoard[10][10]+=mydie4weight
                if board_17x17[8][9] != ENEMY_COLOR:
                    MyscoreBoard[8][10] = recommandNum1
                    MyscoreBoard[9][11] = recommandNum1
                    MyscoreBoard[8][11] *= 200
                elif board_17x17[9][8] != ENEMY_COLOR:
                    MyscoreBoard[10][8] = recommandNum1
                    MyscoreBoard[11][9] = recommandNum1
                    MyscoreBoard[11][8] *= 200

        for row in range(15, 0, -1):
            for col in range(15, 0, -1):
                # if (max(MyscoreBoard[row][col] ,EnemyscoreBoard[row][col])>mymax and board_17x17[row][col] == 0):
                # mymax=max(MyscoreBoard[row][col], EnemyscoreBoard[row][col])

                if MyscoreBoard[row][col] + EnemyscoreBoard[row][col] > mymax and board_17x17[row][col] == 0:
                    mymax = MyscoreBoard[row][col] + EnemyscoreBoard[row][col]
                    myx = row
                    myy = col
                    if ZYT_TEST:
                        print("mymax:", mymax, "x:", myx, "y:", myy)
                        print(MyscoreBoard[row][col])
                        print(EnemyscoreBoard[row][col])

        board_17x17[myx][myy] = BLACK
        printBoard()
        print("我方落子于（", myx - 1, ",", myy - 1, ")")




# 我方是白棋子
else:
    MY_COLOR = WHITE
    ENEMY_COLOR = BLACK
    enemyWhite = input("请输入黑棋落子位置，以空格分开")
    enemyRow, enemyCol = enemyWhite.split(" ")
    enemyRow = int(enemyRow) + 1
    enemyCol = int(enemyCol) + 1
    x1 = enemyRow
    y1 = enemyCol
    board_17x17[enemyRow][enemyCol] = ENEMY_COLOR

    # 我方第一步棋子，使用棋谱中的斜指，默认向右上指
    board_17x17[enemyRow + 1][enemyCol + 1] = MY_COLOR
    printBoard()

    # 我方第二步棋子
    enemyWhite = input("请输入黑棋落子位置，以空格分开")
    enemyRow, enemyCol = enemyWhite.split(" ")
    enemyRow = int(enemyRow) + 1
    enemyCol = int(enemyCol) + 1
    x2 = enemyRow
    y2 = enemyCol
    case1 = 0
    case2 = 0
    case3 = 0
    case4 = 0
    board_17x17[enemyRow][enemyCol] = ENEMY_COLOR
    if (x1 == enemyRow - 1 and y1 == enemyCol):
        board_17x17[enemyRow + 1][enemyCol] = MY_COLOR
        case1 += 1
    elif (x1 == enemyRow + 1 and y1 == enemyCol):
        board_17x17[enemyRow + 2][enemyCol] = MY_COLOR
        case2 += 1
    elif (x1 == enemyRow and y1 == enemyCol + 1):
        board_17x17[enemyRow][enemyCol + 2] = MY_COLOR
        case3 += 1
    elif (x1 == enemyRow and y1 == enemyCol - 1):
        board_17x17[enemyRow][enemyCol + 1] = MY_COLOR
        case4 += 1
    else:
        for row in range(15, 0, -1):
            for col in range(15, 0, -1):
                if board_17x17[row][col] != BLACK and board_17x17[row][col] != WHITE:
                    imSmy = searchImportantStructure(row, col, MY_COLOR)
                    MyscoreBoard[row][col] = Mycolor_calImportance(imSmy)
                    imSen = searchImportantStructure(row, col, ENEMY_COLOR)
                    EnemyscoreBoard[row][col] = Enemy_color_calImportance(imSen)
        mymax = 0

        for row in range(15, 0, -1):
            for col in range(15, 0, -1):
                if row == 9 and col == 9:
                    aaaaa = 999
                # if (max(MyscoreBoard[row][col] ,EnemyscoreBoard[row][col])>mymax and board_17x17[row][col] == 0):
                # mymax=max(MyscoreBoard[row][col], EnemyscoreBoard[row][col])

                if MyscoreBoard[row][col] + EnemyscoreBoard[row][col] > mymax and board_17x17[row][col] == 0:
                    mymax = MyscoreBoard[row][col] + EnemyscoreBoard[row][col]
                    myx = row
                    myy = col
                    if ZYT_TEST:
                        print("mymax:", mymax, "x:", myx, "y:", myy)
                        print(MyscoreBoard[row][col])
                        print(EnemyscoreBoard[row][col])

        board_17x17[myx][myy] = WHITE
    printBoard()

    # 我方第三步棋子
    enemyWhite = input("请输入黑棋落子位置，以空格分开")
    enemyRow, enemyCol = enemyWhite.split(" ")
    enemyRow = int(enemyRow) + 1
    enemyCol = int(enemyCol) + 1
    board_17x17[enemyRow][enemyCol] = ENEMY_COLOR
    if (case1 == 1 and x1 == enemyRow and y1 == enemyCol + 1):
        board_17x17[enemyRow][enemyCol + 2] = MY_COLOR
    elif (case1 == 1 and x1 == enemyRow and y1 == enemyCol - 1):
        board_17x17[enemyRow][enemyCol + 1] = MY_COLOR
    elif (case2 == 1 and x1 == enemyRow and y1 == enemyCol - 1):
        board_17x17[enemyRow + 2][enemyCol - 2] = MY_COLOR
    elif (case2 == 1 and x1 == enemyRow - 1 and y1 == enemyCol - 1):
        board_17x17[enemyRow + 1][enemyCol + 1] = MY_COLOR
    elif (case2 == 1 and x1 == enemyRow - 1 and y1 == enemyCol + 1):
        board_17x17[enemyRow][enemyCol + 2] = MY_COLOR
    elif (case3 == 1 and x1 == enemyRow - 1 and y1 == enemyCol + 1):
        board_17x17[enemyRow - 2][enemyCol + 2] = MY_COLOR
    elif (case3 == 1 and x1 == enemyRow - 1 and y1 == enemyCol):
        board_17x17[enemyRow + 1][enemyCol + 1] = MY_COLOR
    elif (case3 == 1 and x1 == enemyRow + 1 and y1 == enemyCol):
        board_17x17[enemyRow + 2][enemyCol] = MY_COLOR
    elif (case4 == 1 and x1 == enemyRow + 1 and y1 == enemyCol):
        board_17x17[enemyRow + 2][enemyCol + 2] = MY_COLOR
    elif (case4 == 1 and x1 == enemyRow - 1 and y1 == enemyCol):
        board_17x17[enemyRow - 2][enemyCol + 2] = MY_COLOR
    else:
        MyscoreBoard = [[0 for x1 in (range(17))] for y1 in range(17)]
        EnemyscoreBoard = [[0 for x2 in (range(17))] for y2 in range(17)]
        for row in range(15, 0, -1):
            for col in range(15, 0, -1):
                if board_17x17[row][col] != BLACK and board_17x17[row][col] != WHITE:
                    imSmy = searchImportantStructure(row, col, MY_COLOR)
                    MyscoreBoard[row][col] = Mycolor_calImportance(imSmy)
                    imSen = searchImportantStructure(row, col, ENEMY_COLOR)
                    EnemyscoreBoard[row][col] = Enemy_color_calImportance(imSen)
        mymax = 0

        for row in range(15, 0, -1):
            for col in range(15, 0, -1):
                # if (max(MyscoreBoard[row][col] ,EnemyscoreBoard[row][col])>mymax and board_17x17[row][col] == 0):
                # mymax=max(MyscoreBoard[row][col], EnemyscoreBoard[row][col])

                if MyscoreBoard[row][col] + EnemyscoreBoard[row][col] > mymax and board_17x17[row][col] == 0:
                    mymax = MyscoreBoard[row][col] + EnemyscoreBoard[row][col]
                    myx = row
                    myy = col
                    # if ZYT_TEST:
                    print("mymax:", mymax, "x:", myx, "y:", myy)
                    print(MyscoreBoard[row][col])
                    print(EnemyscoreBoard[row][col])

        board_17x17[myx][myy] = WHITE
    printBoard()

    # 后面为自动下棋
    while True:
        enemyWhite = input("请输入黑棋落子位置，以空格分开")
        enemyRow, enemyCol = enemyWhite.split(" ")
        enemyRow = int(enemyRow) + 1
        enemyCol = int(enemyCol) + 1
        board_17x17[enemyRow][enemyCol] = ENEMY_COLOR

        MyscoreBoard = [[0 for x1 in (range(17))] for y1 in range(17)]
        EnemyscoreBoard = [[0 for x2 in (range(17))] for y2 in range(17)]

        for row in range(15, 0, -1):
            for col in range(15, 0, -1):
                if board_17x17[row][col] != BLACK and board_17x17[row][col] != WHITE:
                    imSmy = searchImportantStructure(row, col, MY_COLOR)
                    MyscoreBoard[row][col] = Mycolor_calImportance(imSmy)
                    imSen = searchImportantStructure(row, col, ENEMY_COLOR)
                    EnemyscoreBoard[row][col] = Enemy_color_calImportance(imSen)
        mymax = 0

        for row in range(15, 0, -1):
            for col in range(15, 0, -1):
                # if (max(MyscoreBoard[row][col] ,EnemyscoreBoard[row][col])>mymax and board_17x17[row][col] == 0):
                # mymax=max(MyscoreBoard[row][col], EnemyscoreBoard[row][col])

                if MyscoreBoard[row][col] + EnemyscoreBoard[row][col] > mymax and board_17x17[row][col] == 0:
                    mymax = MyscoreBoard[row][col] + EnemyscoreBoard[row][col]
                    myx = row
                    myy = col
                    # if ZYT_TEST:
                    print("mymax:", mymax, "x:", myx, "y:", myy)
                    print(MyscoreBoard[row][col])
                    print(EnemyscoreBoard[row][col])

        board_17x17[myx][myy] = WHITE
        printBoard()
        print("我方落子于（", myx - 1, ",", myy - 1, ")")
