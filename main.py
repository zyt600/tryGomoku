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

def printBoard():
    """输出整个棋盘"""
    for i in range(15, 0, -1):
        # print('\033[30;40mb\033[0m', end=' ')
        #
        # print("\033[31m这是红色字体\033[0m")
        print("%02d:" % (i - 1), end=' ')
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
    if row <= 0 or col <= 0 or row >= 16 or col >= 16:  # 边界检查
        re = SearchResult(direction, myColor, 0, 0, 1)
        return re
    elif board_17x17[row][col] == myColor * -1 or board_17x17[row][col] == 2:  # 碰壁（边界或对方棋子）的情况
        re = SearchResult(direction, myColor, 0, 0, 1)
        return re
    elif board_17x17[row][col] == 0:  # 空棋盘情况
        re = SearchResult(direction, myColor, 0, 1, 0)
        return re
    # 有我方棋子情况
    result = search_along(direction, row + DIRECTION_LIST[direction - 3], col + DIRECTION_LIST[direction - 3], myColor)
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

class 



import_board_17x17()
printBoard()
# for ii in range(17):  # 设置棋盘边界
#     board_17x17[ii][0] = 2
#     board_17x17[0][ii] = 2
#     board_17x17[ii][16] = 2
#     board_17x17[16][ii] = 2

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
        printBoard()


        # TODO:朱涛通过一些方法,输出黑棋应当落子的位置
        # 比如搜索附近的所有点的推荐值
        printBoard()


else:
    MY_COLOR = WHITE
    ENEMY_COLOR = BLACK
    board_17x17[8][8] = BLACK
