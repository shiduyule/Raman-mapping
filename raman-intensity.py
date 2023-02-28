# -*- coding: utf-8 -*-
# 适用于 X 先变化 如果 Y先变化 需要改动第33行的if nlist[0] != nextlist[0]:为if nlist[1] != nextlist[1]:  
# 适用于横排书写式扫描  不适用于蛇形扫描  
import linecache
import numpy as np
import matplotlib.pyplot as plt
filename = ('2.txt')   #  文件名  最好放在同一个文件夹下 这样不用输入路径
line = 343             #  输入第一个峰值对应的行数直接输入看到的行数就行  可以有偏差
density = 10           #  插入的矩阵行数为data2d的行数  也是放大的倍数
data = []   
#%% 获取总行数 count      rU 只读 文本文件
count = len(open(filename,'rU').readlines())  
print(count)
#%% 获取单个点的测试 波数数据量   dandianzongboshu
n = 2
while True:
    nline = linecache.getline(filename,n)   # 这个函数 是从1开始的 不是从0
    nextline = linecache.getline(filename,n+1)
    nlist = nline.split()
    nextlist = nextline.split()
    if nlist[0] != nextlist[0]:
        dandianzongboshu = n - 1  
        break
    n = n + 1
#%%  每个测试点 单个峰 峰强度分离    
while True:
    if line >= count:
        break
    data.append(linecache.getline(filename,line).split())
    line +=  dandianzongboshu       # 这里输入的是 周期
#%% 获取  xfanwei   dandianzongboshu
n = 0
while True:
    if data[n][1] != data[n + 1][1]:
        xfanwei =  n  +  1
        break
    n =  n  +  1
yfanwei = int(len(data)/xfanwei)
data = np.array(data)
#%% 分离出 x y  并且将它赋给  data2d
data2d = np.empty((yfanwei,xfanwei))  # 设置 二维数组 y行  x列
i = 0
j = 0 
while i  <= yfanwei - 1:  #  当 i 小于 行数总值时
    j = 0 
    while j <= xfanwei - 1:   #  当 j 小于 列数总值时
        data2d[i,j] = data[xfanwei * i + j,3]  #  将原数据中 以x 范围为间隔的数据 依次赋给每一行
        j = j + 1
    i = i + 1
filename= filename.rstrip('.txt')
np.savetxt('F:\\02-28\\%s-%dhang-%dlie.txt'%(filename,np.shape(data2d)[0],np.shape(data2d)[1]),data2d)
#%%  提高分辨率
# 矩阵扩充  matrix expand 至少扩充到 100 * 100
benzhenghangshu = np.shape(data2d)[0]  #行数  
benzhenglieshu = np.shape(data2d)[1]  #列数
#=============================================================================
#扩充列数  设置density 即可
j = 0
while True: 
    insertcolumn = np.empty([np.shape(data2d)[0] ,density], dtype = float)
    i = 0
    while i < np.shape(data2d)[0]:  # 当行数在总行数范围内
        insertcolumn[i,:] = np.linspace(data2d[i,j],data2d[i,j+1],density+1,endpoint = False)[1:density+1] # 以第i行第j列 和第i行第j+1列为起始值   这里是 5行 10列数组   ## 注意数组 索引的左闭右开 
        i = i + 1 
        # print(j,i)
        # print('\n')    
    insertcolumn = insertcolumn.transpose()
    data2d = np.insert(data2d, j+1,insertcolumn, axis=1) # 插入density列
    j = j + 1 + density 
    muqianlieshu = np.shape(data2d)[1]
    if muqianlieshu >= ((benzhenglieshu-1)*density + benzhenglieshu):
        break
#============================================================================
#扩充行数
i = 0
# 插入的矩阵行数为data2d的行数  列数为设置的密度值
# density = int((height * density)/width)
while True:
    insertline = np.empty([density,np.shape(data2d)[1]], dtype = float)
    j = 0   # 从第1列开始
    while j < np.shape(data2d)[1] :  # 当列数在总列数范围内
        insertline[:,j] = np.linspace(data2d[i,j],data2d[i+1,j],density+1,endpoint = False)[1:density+1]  # 将第i行和第i加一行的中间值赋给insertline的第j列
        j = j + 1 
        
    data2d = np.insert(data2d, i+1,insertline, axis=0) # 插入多行
    i = i + 1 + density 
    muqianhangshu = np.shape(data2d)[0]  # 目前行数
    if muqianhangshu == (benzhenghangshu-1)*density + benzhenghangshu:
        break
#%% 创建画布
fig, ax = plt.subplots(figsize = (5.4,4.0),dpi = 600)#facecolor='#F5F5EB',  
im = ax.imshow(data2d,origin='lower',cmap = 'jet' )   #         

#%% 坐标轴 标题 图例
# ax.set_title('mapping of raman intensity of  %s'%(filename))
fig.colorbar(im, ax=ax, label='intensity')  # ,fraction=0.046, pad=0.04
plt.savefig('F:\\02-28\\%s.png'%(filename)) # 保存图片 
plt.rc('font', family='Times New Roman')  # , size=13
plt.show()
#np.savetxt('F:/data2d.txt', data2d)