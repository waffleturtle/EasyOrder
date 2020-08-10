import pandas as pd
import datetime
import xlrd

class Order:
    def __init__(self, path):
        self.workbook = xlrd.open_workbook(path)
        self.worksheet = self.workbook.sheet_by_name('Sheet1')
        self.order_num = ""
        self.order_code = ""
        self.deadline = 0
        self.EDD = 0
        self.amount = 0
        self.total_area = 0
        self.total_circumference = 0
        self.total_longer = 0
        # TODO:
        self.SOT = 0 #SOT  # needs to be calculated
        self.STR = 0
    
    def read_input(self):
        self.order_num = self.worksheet.cell(3, 3).value
        self.order_code = self.worksheet.cell(7, 4).value
        self.deadline = xlrd.xldate.xldate_as_datetime(self.worksheet.cell(9, 24).value, self.workbook.datemode)
        self.EDD = (self.deadline - datetime.datetime.now()).days
        self.amount = self.worksheet.cell(7, 32).value
        self.total_area = self.worksheet.cell(9, 30).value

        self.total_circumference = 0
        self.total_longer = 0
        for row in range(self.worksheet.nrows):
            pianshu = self.worksheet.cell(row,14).value
            changdu = self.worksheet.cell(row,8).value
            gaodu = self.worksheet.cell(row,12).value
            if type(pianshu) == type(changdu) == type(gaodu) == float:
                self.total_circumference += (pianshu * 2 * (changdu + gaodu))
                self.total_longer += (pianshu * max(changdu, gaodu))