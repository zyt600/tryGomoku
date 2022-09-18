"""黑方先行，为1，白方为-1，空棋盘为0，边界为2，
天元即棋盘的最中心，在棋盘的（8，8）（以0为起始），左下角为（0，0）"""
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


class RecommendPosition:
    """推荐落子位置类，以score程度推荐落子于board上的（row，col）。注意!:这并非输出到屏幕上的row和col
    什么位置可以得高分？如果是防守的话，优先堵对方《重要的棋》（下文所述），
    TODO:堵对方可以形成双活三的棋
    TODO:进攻的话，可以考虑埋伏一手，搞一个潜在的双活三，但不漏出来，最后一步再漏出来
    （因为考虑到别人的程序可能不会检测围堵活二）"""
    score = 0
    row = 0
    col = 0

    def __init__(self, row, col, score):
        self.row = row
        self.col = col
        self.score = score


def printBoard():
    """输出整个棋盘"""
    for i in range(15, 0, -1):
        print("%02d" % (i - 1), board_17x17[i][1:16])


def search_along(direction, row, col, myColor):
    """沿着direction方向递归搜索，返回一个SearchResult类"""
    if row < 0 or col < 0 or row > 16 or col > 16:  # 边界检查
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


def judge_must(row, col):
    """判断是否有重要的棋：单4（X11110)，双3(01110)，断3（010110）,
    row为对手上一落子所在行,col为列"""


def judge_must_row(row, col, color_now=5):
    """判断本行是否有重要的棋"""
    if color_now == 5:
        color_now = board_17x17[row][col]
    resultLeft = search_along(LEFT, row, col - 1, color_now)
    resultRight = search_along(RIGHT, row, col + 1, color_now)
    # 判断是否是双3
    if resultRight.emptyNum == 1 and resultLeft.emptyNum == 1 and 1 + resultRight.myLen + resultLeft.myLen == 3:
        pass  # 这就是双3了
    # 判断是否是4
    if 1 + resultRight.myLen + resultLeft.myLen == 4:
        # 判断单4还是双4
        if resultRight.emptyNum + resultLeft.emptyNum == 1:
            pass  # 这就是单4了
        else:
            pass  # 双四了，没救了or赢了
    if 1 + resultRight.myLen + resultLeft.myLen == 5:
    # TODO：
    # 下面判断是否是断的棋（断3、断4）(长度一定是1或者2了）
        if resultRight.emptyNum + resultLeft.emptyNum == 2:
            resultRight_3 = search_along(RIGHT, row, col + 3, color_now)
            if resultRight_3.myLen + 1 + resultRight.myLen + resultLeft.myLen >= 3 and resultRight_3.emptyNum == 1:
                pass  # 断3或断4，一定要堵中间
            resultLeft_3 = search_along(LEFT, row, col - 3, color_now)
            if resultLeft_3.myLen + 1 + resultRight.myLen + resultLeft.myLen >= 3 and resultLeft_3.emptyNum == 1:
                pass  # 断3或断4，一定要堵中间


printBoard()
for ii in range(17):  # 设置棋盘边界
    board_17x17[ii][0] = 2
    board_17x17[0][ii] = 2
    board_17x17[ii][16] = 2
    board_17x17[16][ii] = 2

stringColor = input("请输入我方是 黑 还是 白")
if stringColor == "黑":
    MY_COLOR = BLACK
    ENEMY_COLOR = WHITE
    print("以最左下角可落子处为（0，0），我方第一步落子于（7，7）")
    board_17x17[8][8] = BLACK
    printBoard()
    enemyWhite = input("请输入白棋落子位置，以空格分开")
    enemyRow, enemyCol = enemyWhite.split(" ")
    enemyRow = int(enemyRow)
    enemyCol = int(enemyCol)
    board_17x17[enemyRow + 1][enemyCol + 1] = ENEMY_COLOR
    printBoard()
    # 该黑棋落第三个子了，注意，不能落在天元5x5范围内，也就是说输出到屏幕的坐标范围必须不是[5~9]

else:
    MY_COLOR = WHITE
    ENEMY_COLOR = BLACK
    board_17x17[8][8] = BLACK
