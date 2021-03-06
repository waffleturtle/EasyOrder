from order import *
import os
import xlwt
import time

HEADINGS = ["序号", "项目名称", "订单号", "产品配置", "单片玻璃种类", "单片玻璃厚度(mm)", 
            "总片数", "总面积(m^2)", "长边单侧累计长度(mm)", "总周长(mm)", "", "交货日期",
            "EDD", "SOT(小时)", "STR(小时)", "订单延迟时间", " ", "月平均工作天数", "作业制", "标准作业时间"]

class Manager:
    def __init__(self):
        self.input_path = ""
        self.order_list = []
        self.num_orders = 0

        # below are user inputs
        self.tujiao_speed = 29 # 米/分钟
        self.zhijiao_tujiao = 3 # 秒
        self.wait_time = 1 #秒
        self.switch_time = 60 #秒

        self.working_days = 28
        self.shift_length = 9 # hours
        self.num_shift = 1  # or 2
        self.sort_method = "EDD"

    def set_input_path(self, path):
        self.input_path = path

    def read_input_dir(self):
        for filename in os.listdir(self.input_path):
            if ".xls" in filename:
                new_order = Order(self.input_path + '/' + filename)
                new_order.read_input()
                # （每个订单号的玻璃累计周长（mm）/涂胶速度(m/min)）+ 每片玻璃直角的涂胶时间(s)*4*玻璃片数）+（等待时间(s)*玻璃片数）+（切换时间(s)*玻璃片数/35）
                new_order.SOT = (new_order.total_circumference / self.tujiao_speed) / (1000 / 60) + (self.zhijiao_tujiao * 4 * new_order.amount) + (self.wait_time + new_order.amount) + (self.switch_time * new_order.amount / 35)
                new_order.SOT /= 3600
                new_order.STR = new_order.EDD * self.shift_length * self.num_shift - new_order.SOT
                self.order_list.append(new_order)

    def output(self):
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('Sheet1')
        # Sort using EDD, SOT, or STR
        if self.sort_method == "EDD":
            self.sort_edd()
        elif self.sort_method == "SOT":
            self.sort_sot()
        elif self.sort_method == "STR":
            self.sort_str()
        else:
            print("unknown sort method")
            pass
        # after sorting, the delay time should be calculated according to the sequence
        self.calculate_delay()
        for i in range(len(HEADINGS)):
            sheet.write(0, i, HEADINGS[i])
        
        sheet.write(1, 17, self.working_days)
        if self.num_shift == 1:
            sheet.write(1, 18, "单班作业制")
        else:
            sheet.write(1, 18, "双班作业制")
        sheet.write(1, 19, self.shift_length)

        for i in range(len(self.order_list)):
            current_order = self.order_list[i]
            sheet.write(i + 1, 0, i + 1)
            sheet.write(i + 1, 2, current_order.order_num)
            sheet.write(i + 1, 3, current_order.order_code)
            sheet.write(i + 1, 5, int(current_order.thickness))
            sheet.write(i + 1, 6, current_order.amount)
            sheet.write(i + 1, 7, current_order.total_area)
            sheet.write(i + 1, 8, current_order.total_longer)
            sheet.write(i + 1, 9, current_order.total_circumference)
            date_format = xlwt.XFStyle()
            date_format.num_format_str = 'yyyy/mm/dd'
            sheet.write(i + 1, 11, current_order.deadline, date_format)
            sheet.write(i + 1, 12, current_order.EDD)
            sheet.write(i + 1, 13, current_order.SOT)
            sheet.write(i + 1, 14, current_order.STR)
            sheet.write(i + 1, 15, current_order.remaining_delay)
        
        timestr = time.strftime("%Y%m%d-%H%M%S")
        workbook.save(timestr + '-' + self.sort_method + '.xls')

    def sort_edd(self):
        self.order_list.sort(key = lambda x: x.EDD, reverse = False)
        for order in self.order_list:
            print(str(order.order_num) + ": EDD = " + str(order.EDD))

    def sort_sot(self):
        self.order_list.sort(key = lambda x: x.SOT, reverse = False)
        for order in self.order_list:
            print(str(order.order_num) + ": SOT = " + str(order.SOT))
    
    def sort_str(self):
        self.order_list.sort(key = lambda x: x.STR, reverse = False)
        for order in self.order_list:
            print(str(order.order_num) + ": STR = " + str(order.STR))
    
    def calculate_delay(self):
        # please call this after sorting is complete
        SOT_SUM = 0
        for i in range(len(self.order_list)):
            order = self.order_list[i]
            SOT_SUM += order.SOT
            order.remaining_delay = (-1) * order.STR if i == 0 else (SOT_SUM - order.STR)


            
