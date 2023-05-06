# easyfund


laugh



---



#### 介绍



##### 安装包：

pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple



##### 参考：

https://github.com/weibycn/fund.git

https://github.com/refraction-ray/xalpha.git



##### 设计思路：

获取所有基金信息

通过策略打分，选择前百分之几的基金，进行模拟交易

模拟交易策略：选择  公司估值法、趋势法和资金法三大类 之一



默认使用趋势法：金叉进场，3，12，25





##### 特点：

客观

高效

精准

迅速

分散



#### 其他：

##### 统计套利：

利用证券价格的历史统计规律进行套利，在方法上可以分为 两类，一类是利用股票的收益率序列建模，称之为β中性策略；另一类是利用 股票的价格序列的协整关系建模，我们称之为协整策略



##### 海龟交易策略：

充分利用了ATR指标



\#多头持仓，当价格跌破开仓价-2*ATR止损出场

 Low <= preEntryPrice - 2 * ATR 

#空头持仓，当价格突破开仓价+2*ATR止损离场

 High >= preEntryPrice + 2 * ATR

