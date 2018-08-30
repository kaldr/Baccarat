import xlsxwriter
import os


class PlayerExporter:
    def __init__(self, player):
        # 玩家
        self.player = player

    def get_filename(self, idx=0):
        winStr = '赢'
        if self.player.current_money - self.player.money < 0:
            winStr = '输'
        self.filename = "%s_%s_%s_%.1f" % (self.player.name, idx, winStr, (self.player.current_money - self.player.money))

    def export_player(self, folder=False, idx=0):
        self.get_filename(idx=idx)
        workbook = self.player_workbook(self.filename, folder=folder)
        workbook.set_size(1200, 800)
        history_sheet = workbook.add_worksheet('押注历史')
        chart_sheet = workbook.add_worksheet('曲线图')
        stake_sheet = workbook.add_worksheet('牌局流水')
        self.history_sheet(history_sheet)
        self.stake_sheet(stake_sheet, False)
        self.chart_sheet(chart_sheet, workbook)
        workbook.close()

    def player_workbook(self, filename, folder=False):

        if folder:
            if not folder.endswith("/"):
                folder = folder + '/'
            path = '%s%s.xlsx' % (folder, filename)
        else:
            path = './Export/%s.xlsx' % filename
        file_dir = os.path.split(path)[0]
        if not os.path.isdir(file_dir):
            os.makedirs(file_dir)
        workbook = xlsxwriter.Workbook(path)
        formatZhuang = workbook.add_format({"font_color": 'white', 'bold': 1, 'bg_color': 'blue'})
        formatXian = workbook.add_format({"font_color": 'white', 'bold': 1, 'bg_color': 'purple'})
        formatWin = workbook.add_format({"font_color": 'white', 'bold': 1, 'bg_color': 'red'})
        formatLose = workbook.add_format({"font_color": 'white', 'bold': 1, 'bg_color': 'green'})
        formatZhuangStake = workbook.add_format({"font_color": 'red', 'bold': 1})
        formatXianStake = workbook.add_format({"font_color": 'blue', 'bold': 1})
        formatHeStake = workbook.add_format({"font_color": 'green', 'bold': 1})
        self.formats = {'zhuang': formatZhuang, 'xian': formatXian, 'win': formatWin, 'lose': formatLose, 'zhuang_stake': formatZhuangStake, 'xian_stake': formatXianStake, 'he_stake': formatHeStake}
        return workbook

    def format_history_sheet(self, sheet, rowCount):
        sheet.conditional_format("H1:I%d" % rowCount, {'type': 'text', 'criteria': 'begins with', 'value': u'庄', 'format': self.formats['zhuang']})
        sheet.conditional_format("H1:I%d" % rowCount, {'type': 'text', 'criteria': 'begins with', 'value': u'闲', 'format': self.formats['xian']})
        sheet.conditional_format("J1:L%d" % rowCount, {'type': 'cell', 'criteria': ">", 'value': '0', 'format': self.formats['win']})
        sheet.conditional_format("J1:L%d" % rowCount, {'type': 'cell', 'criteria': "<", 'value': '0', 'format': self.formats['lose']})
        sheet.conditional_format("N1:N%d" % rowCount, {'type': 'cell', 'criteria': ">", 'value': '0', 'format': self.formats['win']})
        sheet.conditional_format("N1:N%d" % rowCount, {'type': 'cell', 'criteria': "<", 'value': '0', 'format': self.formats['lose']})

    def history_sheet(self, sheet):
        data = self.player.result_history
        rowCount = len(self.player.result_history)
        header = {
            'id': '序号',
            'baccarat_id': "局",
            'round_id': "轮",
            'zhuang': "庄牌",
            "zhuang_point": "庄家点数",
            'xian': "闲牌",
            "xian_point": "闲家点数",
            'winner': "赢家",
            'stake': "押注",
            "change": "本轮变化",
            'win': "本轮输赢",
            'win_or_lose': "净",
            'stake_money': "押注金额",
            # "money_before": "押注前金额",
            # 'money': "本轮后金额",
            'profit': "总盈利",
            'win_times': "总赢次数",
            'lose_times': "总输次数",
            'win_lose_differ': "输赢差",
            'info': "决策"
        }
        col = 0
        row = 0
        i = 0
        for (key, title) in header.items():
            sheet.write(row, col, title)
            for d in data:
                row += 1
                if key == 'id':
                    sheet.write(row, col, row)
                elif key == 'win':
                    if d[key]:
                        sheet.write(row, col, 1)
                    else:
                        if d['winner_id'] == 3:
                            sheet.write(row, col, 0)
                        else:
                            sheet.write(row, col, -1)
                else:
                    if title in ['赢家', '押注', '决策', '庄牌', '闲牌']:
                        sheet.write(row, col, u'%s' % d[key])
                    else:
                        sheet.write(row, col, d[key])
            col += 1
            row = 0
        self.format_history_sheet(sheet, rowCount)

    def chart_sheet(self, sheet, workbook):
        chart1 = workbook.add_chart({'type': 'line'})
        sheet.insert_chart('A15', chart1)
        chart1.add_series({
            'categories': '=押注历史!$A$1:$A$%d' % len(self.player.result_history),
            'values': '=押注历史!$N$1:$N$%d' % len(self.player.result_history),
            'overlap': 10,
        })
        chart1.set_legend({'none': True})
        chart1.set_x_axis({'visible': False})
        chart1.set_title({'name': '盈利'})
        chart1.set_plotarea({'layout': {'x': 0, 'y': 0, 'width': 1, 'height': 1}})

        chart2 = workbook.add_chart({'type': 'column'})
        sheet.insert_chart('A1', chart2)
        chart2.add_series({
            'categories': '=押注历史!$A$1:$A$%d' % len(self.player.result_history),
            'values': '=押注历史!$L$1:$L$%d' % len(self.player.result_history),
            'overlap': 10,
        })
        chart2.set_legend({'none': True})
        chart2.set_x_axis({'visible': False})
        chart2.set_title({'name': '净输赢'})
        chart2.set_plotarea({'layout': {'x': 0, 'y': 0, 'width': 1, 'height': 1}})
        chart3 = workbook.add_chart({'type': 'line'})
        sheet.insert_chart('A30', chart3)
        chart3.add_series({
            'categories': '=押注历史!$A$1:$A$%d' % len(self.player.result_history),
            'values': '=押注历史!$M$1:$M$%d' % len(self.player.result_history),
            'overlap': 10,
        })
        chart3.set_legend({'none': True})
        chart3.set_x_axis({'visible': False})
        chart3.set_title({'name': '押注'})
        chart3.set_plotarea({'layout': {'x': 0, 'y': 0, 'width': 1, 'height': 1}})
        # chart4 = workbook.add_chart({'type': 'line'})
        # sheet.insert_chart('A15', chart4)
        # chart4.add_series({
        #     'categories':
        #     '=押注历史!$A$1:$A$%d' % len(self.player.result_history),
        #     'values':
        #     '=押注历史!$Q$1:$Q$%d' % len(self.player.result_history),
        #     'overlap':
        #     10,
        # })
        # chart4.set_legend({'none': True})
        # chart4.set_x_axis({'visible': False})
        # chart4.set_title({'name': '输赢总次数差'})
        # chart4.set_plotarea({
        #     'layout': {
        #         'x': 0,
        #         'y': 0,
        #         'width': 1,
        #         'height': 1
        #     }
        # })
        chart1.set_size({'width': 1000, 'height': 250})
        chart2.set_size({'width': 1000, 'height': 250})
        chart3.set_size({'width': 1000, 'height': 250})
        # chart4.set_size({'width': 1000, 'height': 250})

    def stake_sheet(self, sheet, print_he=True, with_win=True):
        data = self.player.result_history
        current_baccarat_id = 0
        col = 0
        row = 0
        last_win_id = 0
        current_baccarat_row = 0
        max_same_count = 0
        same_count = 0
        win_count = 0
        total_win_count = 0
        lose_count = 0
        total_lose_count = 0
        zhuang_count = 0
        total_zhuang_count = 0
        xian_count = 0
        total_xian_count = 0
        he_count = 0
        total_he_count = 0
        sheet.set_column('A:CA', 4)
        max_pure_lose = 0
        max_pure_win = 0
        first_col = True
        # 输总次数
        for d in data:
            if d['win_or_lose'] < max_pure_lose:
                max_pure_lose = d['win_or_lose']
            if d['win_or_lose'] > max_pure_win:
                max_pure_win = d['win_or_lose']
            if d['baccarat_id'] != current_baccarat_id:
                current_baccarat_id = d['baccarat_id']

                last_win_id = 0
                row += max_same_count
                row += 2
                if with_win:
                    col = 1
                sheet.write(row, 0, u'第%d局' % d['baccarat_id'])
                last_title_row = current_baccarat_row
                if current_baccarat_id > 1:
                    statistic = '本局赢%d局，输%d局，共有庄%d局，闲%d局，和%d局' % (win_count, lose_count, zhuang_count, xian_count, he_count)
                    sheet.write(last_title_row - 1, 0, u'%s' % statistic)
                row += 2
                current_baccarat_row = row
                max_same_count = 0
                win_count = 0
                lose_count = 0
                zhuang_count = 0
                xian_count = 0
                he_count = 0

            if last_win_id == 0:
                last_win_id = d['winner_id']
                row -= 1
            flag = False
            if print_he:
                flag = True
            else:
                if d['winner_id'] != 3:
                    flag = True

            if flag:
                if d['winner_id'] == last_win_id:
                    same_count += 1
                    if same_count > max_same_count:
                        max_same_count = same_count
                    row += 1
                    if with_win:
                        col -= 1
                else:
                    last_win_id = d['winner_id']
                    same_count = 0
                    col += 1
                    row = current_baccarat_row
                if d['winner_id'] == 1:
                    zhuang_count += 1
                    total_zhuang_count += 1
                else:
                    xian_count += 1
                    total_xian_count += 1
            else:
                he_count += 1
                total_he_count += 1
            if d['win']:
                win_count += 1
                total_win_count += 1
            else:
                if d['winner_id'] != 3:
                    lose_count += 1
                    total_lose_count += 1

            win = '●◆'
            lose = '○◇'
            if d['win']:
                s = win[0]
            else:
                s = lose[0]
            if d['winner_id'] == 1:
                f = self.formats['zhuang_stake']
            elif d['winner_id'] == 2:
                f = self.formats['xian_stake']
            else:
                f = self.formats['he_stake']
                s = lose[1]
            if flag:
                sheet.write(row, col, s, f)
                col += 1
                sheet.write(row, col, d['win_or_lose'])
        last_title_row = current_baccarat_row
        statistic = '本局赢%d局，输%d局，共有庄%d局，闲%d局，和%d局' % (win_count, lose_count, zhuang_count, xian_count, he_count)
        sheet.write(last_title_row - 1, 0, u'%s' % statistic)

        total_statistic = '盈利%s，最大净赢%d，最大净输%d，赢%d局，输%d局，共有庄%d局，闲%d局，和%d局' % (self.player.current_money - self.player.money, max_pure_win, max_pure_lose, total_win_count, total_lose_count,
                                                                             total_zhuang_count, total_xian_count, total_he_count)
        sheet.write(0, 0, u'%s' % total_statistic)
