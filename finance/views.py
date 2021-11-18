from django.shortcuts import render,redirect
from django.views import View

from .models import Category,Balance
from .forms import CategoryForm

import datetime

class IndexView(View):
    
    #日ごとの収支計算し返却する。
    def calc(self, balances):

        today       = ""
        before_day  = ""

        day_balance = []
        dic         = { "day":"","income":0,"spending":0 }

        for balance in balances:
            today   = str(balance.pay_dt.day)

            #前回のループと日付不一致の時、アペンドして新規作成
            if today != before_day:

                #初期状態ではない場合のみアペンド
                if dic["day"] != "":
                    day_balance.append(dic)

                dic         = { "day":"","income":0,"spending":0 }
                dic["day"]  = today

            if balance.category.income:
                dic["income"] += balance.value
            else:
                dic["spending"] += balance.value

            before_day  = today

        day_balance.append(dic)
        print(day_balance)

        return day_balance

    def get(self, request, *args, **kwargs):

        self.calc(Balance.objects.all())
        

        context     = {}
        context["categories"]   = Category.objects.all()

        #TODO:ここのバランスは全データを抜き取っているため、カレンダーと食い違う。.filter()で当月か指定した月だけ抜き取り
        context["balances"]     = Balance.objects.all()


        #今月の初日を手に入れる。
        dt  = datetime.datetime.now()
        dt  = dt.replace(day=1)

        #今月を手に入れる
        month       = dt.month

        #month_dateはweek_dateのリスト、week_dateは日付のリスト
        month_date  = []
        week_date   = []

        #最終的に作られるmonth_dateのイメージ。このように複数のweek_dateを含む。月の最初が日曜日ではない場合、必要な数だけ空欄をアペンドしておく
        """
        [ ['  ', '  ', '1 ', '2 ', '3 ', '4 ', '5 '],
          ['6 ', '7 ', '8 ', '9 ', '10', '11', '12'],
          ['13', '14', '15', '16', '17', '18', '19'],
          ['20', '21', '22', '23', '24', '25', '26'],
          ['27', '28', '29', '30']
          ]

          [ {"dt":'6 ',"income":3000,"spending":600 }, '7 ', '8 ', '9 ', '10', '11', '12'],
        """

        #一日ずつずらしてweek_dateにアペンドする。
        #datetimeのオブジェクトは .weekday() で数値化した曜日が出力される(月曜日が0、日曜日が6)

        #日曜日以外の場合、空欄を追加する。
        if dt.weekday() != 6:
            for i in range(dt.weekday()+1):
                week_date.append("")

        #1日ずつ追加して月が変わったらループ終了
        while month == dt.month:
            
            #TODO:ここで辞書型をアペンド(日付、収入の合計、支出の合計)
            dic = {"dt":"","income":0,"spending":0 }
            week_date.append(dt.day)

            #1日追加する
            dt  = dt + datetime.timedelta(days=1)

            #週末になるたびに追加する。
            if dt.weekday() == 6:
                month_date.append(week_date)
                week_date   = []

        #一ヶ月の最終週を追加する。
        if dt.weekday() != 6:
            month_date.append(week_date)

        context["month_date"]   = month_date


        return render(request,"finance/index.html",context)

index   = IndexView.as_view()


class CategoryView(View):

    def post(self, request, *args, **kwargs):

        form    = CategoryForm(request.POST)

        if form.is_valid():
            print("OK")
            form.save()
        else:
            print("NG")

        return redirect("finance:index")

category    = CategoryView.as_view()

