import wx
from datetime import date, timedelta

def calculate_installment_plans(total_amount, periods):
    plans = []

    plans_info = {
        1: {'down_payment_percent': 25, 'service_fee_percent': 15},
        2: {'down_payment_percent': 25, 'service_fee_percent': 20},
        3: {'down_payment_percent': 25, 'service_fee_percent': 24}
    }

    for i in range(1, periods + 1):
        info = plans_info[i]
        down_payment = (info['down_payment_percent'] / 100) * total_amount
        service_fee = (info['service_fee_percent'] / 100) * total_amount
        initial_payment = down_payment + service_fee
        
        if i == 1:
            per_payment = round((total_amount * 0.75))
        elif i == 2:
            per_payment = round((total_amount * 0.75) / 2)
        else:
            per_payment = round((total_amount * 0.75) / 3)

        plan = {
            'periods': i,
            'initial_payment': round(initial_payment, 2),
            'per_payment': per_payment,
            'service_fee_percent': info['service_fee_percent'],
            'down_payment_percent': info['down_payment_percent']
        }
        plans.append(plan)

    return plans

def get_repayment_dates(start_date, periods):
    dates = [start_date + timedelta(days=30)]
    for _ in range(periods - 1):
        dates.append(dates[-1] + timedelta(days=30))
    return dates

class PayInstallmentCalculator(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="分期付款计算器", size=(533, 315))
        self.panel = wx.Panel(self)
        self.init_ui()

    def init_ui(self):
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        label_amount = wx.StaticText(self.panel, label="商品金额：")
        hbox1.Add(label_amount, flag=wx.RIGHT, border=8)
        
        self.amount_entry = wx.TextCtrl(self.panel, style=wx.TE_RIGHT)  # 设置文本右对齐
        hbox1.Add(self.amount_entry, proportion=1, flag=wx.EXPAND, border=5)
        
        label_unit = wx.StaticText(self.panel, label="元")
        hbox1.Add(label_unit, flag=wx.LEFT, border=8)
        
        self.calculate_button = wx.Button(self.panel, label="计算")
        hbox1.Add(self.calculate_button, flag=wx.LEFT, border=8)  # 将计算按钮放在输入框后面
        
        vbox.Add(hbox1, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)

        self.result_text_area = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        vbox.Add(self.result_text_area, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

        self.panel.SetSizer(vbox)
        self.calculate_button.Bind(wx.EVT_BUTTON, self.on_calculate)

    def on_calculate(self, event):
        amount = self.amount_entry.GetValue()
        if amount.strip() == "":
            wx.MessageBox("请输入商品金额", "错误", wx.OK | wx.ICON_ERROR)
            return

        try:
            total_amount = float(amount)
            plans = calculate_installment_plans(total_amount, 3)
            
            current_date = date.today().isoformat()
            result_text = f"现在时间是{current_date}日，您当前分期商品金额：{total_amount}元。\n\n"
            
            for plan in plans:
                result_text += f"办理{plan['periods']}期->这样付款：\n"
                result_text += f"今天先给我{plan['down_payment_percent']}%首付+{plan['service_fee_percent']}%服务费，一共是{plan['initial_payment']:.0f}元\n"
                dates = get_repayment_dates(date.today(), plan['periods'])
                for i, repayment_date in enumerate(dates):
                    year = repayment_date.year
                    month = repayment_date.month
                    day = repayment_date.day
                    month_str = f"{year}年{month:02d}月{day:02d}日"
                    result_text += f"{month_str}应还款{plan['per_payment']}元\n"
                result_text += "******************分割线******************\n\n"
            self.result_text_area.SetValue(result_text)
        except ValueError as e:
            wx.MessageBox(f"异常: {str(e)}", "错误", wx.OK | wx.ICON_ERROR)

if __name__ == "__main__":
    app = wx.App(False)
    frame = PayInstallmentCalculator()
    frame.Show()
    app.MainLoop()