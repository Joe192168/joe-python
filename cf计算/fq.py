import tkinter as tk
from tkinter import messagebox
from datetime import date, timedelta

def calculate_installment_plans(total_amount, periods):
    plans = []

    # 固定首付款和服务费比例
    plans_info = {
        1: {'down_payment_percent': 25, 'service_fee_percent': 15},
        2: {'down_payment_percent': 25, 'service_fee_percent': 20},
        3: {'down_payment_percent': 25, 'service_fee_percent': 24}
    }

    # 计算每个分期计划
    for i in range(1, periods + 1):
        info = plans_info[i]
        down_payment = (info['down_payment_percent'] / 100) * total_amount
        service_fee = (info['service_fee_percent'] / 100) * total_amount
        initial_payment = down_payment + service_fee
        remaining_amount = total_amount - initial_payment
        
        if i == 1:
            per_payment = round((total_amount * 0.75))
        elif i == 2:
            per_payment = round((total_amount * 0.75) / 2)
        else:
            per_payment = round((total_amount * 0.75) / 3)

        # 构建分期计划
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

def on_calculate():
    try:
        total_amount = float(amount_entry.get())
        plans = calculate_installment_plans(total_amount, 3)
        
        current_date = date.today().isoformat()
        result_text = f"现在时间是{current_date}日，您当前分期商品金额：{total_amount}元。\n\n"
        
        for plan in plans:
            result_text += f"办理{plan['periods']}期->这样付款：\n"
            result_text += f"今天先给我{plan['down_payment_percent']}%首付+{plan['service_fee_percent']}%服务费，一共是{plan['initial_payment']:.0f}元\n"
            dates = get_repayment_dates(date.today(), plan['periods'])
            for i, repayment_date in enumerate(dates):
                month = repayment_date.strftime("%Y年%m月%d日")
                result_text += f"{month}应还款{plan['per_payment']}元\n"
            result_text += "******************分割线******************\n\n"
        result_text_area.delete('1.0', tk.END)
        result_text_area.insert(tk.END, result_text)
    except ValueError:
        messagebox.showerror("错误", "请输入有效的数字")

# 创建主窗口
root = tk.Tk()
root.title("分期付款计算器")

# 设置窗口的最小宽度、最大宽度和高度，禁止放大缩小
root.minsize(533, 315) # Adjusted for smaller height
root.maxsize(533, 315) # Adjusted for smaller height
root.resizable(False, False)

# 创建商品金额标签和输入框
tk.Label(root, text="商品金额：").grid(row=0, column=0, padx=10, pady=10, sticky="e")
amount_entry = tk.Entry(root)
amount_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

tk.Label(root, text="元").grid(row=0, column=2, padx=10, pady=10)

# 创建计算按钮
calculate_button = tk.Button(root, text="计算", command=on_calculate)
calculate_button.grid(row=0, column=3, padx=10, pady=10)

# 创建结果显示文本域
result_text_area = tk.Text(root, height=15, width=70)
result_text_area.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

# 运行主循环
root.mainloop()