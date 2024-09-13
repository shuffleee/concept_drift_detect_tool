# 项目说明：因子漂移的工程化应用

# 关键问题
a. 这次漂移的程度如何，定量
    1. 漂移的次数
    2. 漂移的程度
b. 此次漂移是否结束，什么时候结束的
c. 过去是否发生过来类似漂移
d. 未来再次发生类似漂移如何应对（能够解释这段时间使用该方法解决概念漂移的原因）

# 方案：漂移检测与诊断
漂移检测器：使用ADWIN概念漂移检测器，基于滑动窗口的漂移检测器， 适合实时检测市场环境中的突然漂移。
    ADWIN原理：AdWin算法通过维护一个可变大小的滑动窗口来检测概念漂移。窗口内的数据被分成两个子窗口，计算两个子窗口的平均值，并检查它们是否有显著差异。如果存在显著差异，就认为发生了概念漂移。
检测指标：（wind 中证2000- 沪深300） 过去 252 个工作日的收益率差形成相对强弱指标生成信号得到的净值、日收益率、预测准确率等。

# 参数选择
adwin参数可默认（delta=0.002，检测频率为32）

逻辑：adwin检测出来的漂移点反映前面数据分布可能发生了变化，再使用漂移点前后32个数据点方差的差值（这里的指标参考2019_ESWA_On learning guarantees to unsupervised concept drift detection on data streams 论文输入标普500的收盘价作为数据流，使用标准偏差和功率谱作为测量函数以及Plover算法，来检测08年金融危机。）
方差是衡量一组数据离散程度的统计量，可以反映数据的波动程度。差值能够反映前后数据分布离散程度的差异，我们采用方差差值的前20%的漂移点认为是漂移程度大的点，前20%是为了避免数据流输入量纲的影响，自动适应调整判断阈值，前10%可能会漏掉部分大跌或者大涨的情况，前30%可能会包含太多的漂移点，导致崩溃或者大牛市检测准确度降低。
根据方差差值选出漂移点的同时需要满足与后一个漂移点之间(累积净值）百分比相差15%以上，我们认为是一个崩盘事件或者是牛市事件。

漂移的次数：检测到漂移的次数
漂移程度：净值相差百分比
漂移开始以及结束：挑选出前20%方差差值较大的漂移点时作为概念漂移的开始点，下一个漂移点作为漂移的结束点。若当前漂移点与前一个漂移点百分比发生超过15%，且与后一个漂移点百分比低于15%，那么将前一个漂移点作为开始点，当前漂移点作为结束点。

# 执行：
执行main文件，判断是否读取本地文件数据。然后选择是否检测个股（使用本地文件数据），输入股票代码以及检测的列名。若不适用本地文件数据，可导入模块后，将data的列数据传入进行检测。

# 结果：
检测指标为：累计净值
    adwin的delta参数为0.01，检测频率为24的情况下，效果比较明显，能够检测出三段小盘股崩溃或者牛市的事件。时间段在2015-09-2016-02、2022-05-06-2022-11-01、2024-01-2024-04。
    
    adwin的delta参数为0.002，检测频率为32的情况下，检测了市场4只大盘股以及4只小盘股，均能够检测出短期内股价明显动荡的时间段。000001.SZ 平安银行，000002.SZ 万科A，000568.sz 泸州老窖，000625.SZ 长安汽车，002786.SZ银宝山新，600683.SH京投发展，603222.SH济民健康，002952.SZ 亚世光电。结果图放于result/中。
    
检测指标为：
日收益率
    adwin在delta=0.1/0.05/0.01/0.002，检测频率为11/12/13/14/18/20/24/32的参数下，几乎没有检测出漂移点
    
预测准确率
    adwin在delta=0.01/0.002，检测频率为11/12/13/14/18/20/24/32的参数下，大多次有1-2个漂移点，delta增大到0.1，漂移点再增加1-2个，平均模型准确率是0.516432，

# 其他尝试结果
#- 更换其他概念漂移检测器
    DDM、PHT、EDDM、HDDMA、HDDMW，在日收益率指标上几乎检测不出来漂移点；在预测准确率中EDDM有6个漂移点，HDDMA 1个，HDDMW 2个，DDM、PHT均未检测出漂移点；净值检测则大多数有漂移点。

#- 更换检测指标，如中证2000与沪深300的日收益率差以及净值。
    ADWIN更换到更低的频率11个数据点检测一次，delta为0.002/0.01/0.05，日收益率差仍为0个漂移点

#- 更换漂移检测器参数
    PHT检测算法在阈值为50的时候检测不出漂移点，阈值由50调整到0.05，日收益率有10个漂移点，0.01，日收益率有52个漂移点，预测准确率有80个漂移点。
        PHT原理：是一种基于 CUSUM 算法的漂移检测方法，它通过计算累积和的平方和来检测漂移。


