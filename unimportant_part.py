class RecommendPosition:
    """推荐落子位置类，以score程度推荐落子于board上的（row，col）。注意!:这并非输出到屏幕上的row和col(因为棋盘有边缘的一圈2作为边界)
    什么位置可以得高分？如果是防守的话，优先堵对方《重要的棋》（下文所述），
    （因为考虑到别人的程序可能不会检测围堵活二）"""

    # TODO:堵对方可以形成双活三的棋
    # TODO:进攻的话，可以考虑埋伏一手，搞一个潜在的双活三，但不漏出来，最后一步再漏出来
    # TODO:可以前4步如果白棋被隔开，就开辟一个新区域去落第一步，然后执行先手必胜
    # TODO:可以设置""棋风一转"模块🐶，考虑如果对方强行追求和棋，有没有什么反制措施

    score = 0
    row = 0
    col = 0

    def __init__(self, row, col, score):
        self.row = row
        self.col = col
        self.score = score



def judge_must(row, col):
    """判断是否有重要的棋：单4（X11110)，活3(01110)，断3（010110）,
    row为对手上一落子所在行,col为列"""



def judge_must_row(row, col, color_now=-999):
    """判断本行是否有重要的棋"""
    if color_now != BLACK and color_now != WHITE:
        color_now = board_17x17[row][col]
    resultLeft = search_along(LEFT, row, col - 1, color_now)
    resultRight = search_along(RIGHT, row, col + 1, color_now)
    # 判断是否是活3
    if resultRight.emptyNum == 1 and resultLeft.emptyNum == 1 and 1 + resultRight.myLen + resultLeft.myLen == 3:
        pass  # 这就是活3了
    # 判断是否是4
    if 1 + resultRight.myLen + resultLeft.myLen == 4:
        # 判断单4还是双4
        if resultRight.emptyNum + resultLeft.emptyNum == 1:
            pass  # 这就是单4了
        else:
            pass  # 双四了，没救了or赢了
    if 1 + resultRight.myLen + resultLeft.myLen == 5:
        # TODO：在这里加如果连成五个子该怎么办（比如输出你输了/赢了之类的
        pass
    # 下面判断是否是断的棋（断3、断4）(长度一定是1或者2了）
    if resultRight.emptyNum + resultLeft.emptyNum == 2:
        resultRight_3 = search_along(RIGHT, row, col + 3, color_now)
        if resultRight_3.myLen + 1 + resultRight.myLen + resultLeft.myLen >= 3 and resultRight_3.emptyNum == 1:
            pass  # 断3或断4，一定要堵中间
        resultLeft_3 = search_along(LEFT, row, col - 3, color_now)
        if resultLeft_3.myLen + 1 + resultRight.myLen + resultLeft.myLen >= 3 and resultLeft_3.emptyNum == 1:
            pass  # 断3或断4，一定要堵中间

