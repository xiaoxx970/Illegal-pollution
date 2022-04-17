import argparse

# from matplotlib import rc_params_from_file
import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import KernelPCA as PCA
from sklearn.preprocessing import MinMaxScaler, StandardScaler


def read_data(filename):
    header = ['企业编码','排污口编码','污染物编码','记录时间','污染物浓度','污染物排放量']
    pollution = pd.read_csv(filename, names=header, encoding='utf-8', low_memory=False)
    pollution.dropna()

    pollution_shaped = pd.pivot_table(pollution,index =["记录时间", "企业编码","排污口编码"],values=["污染物浓度", "污染物排放量"],columns='污染物编码')
    pollution_mean = pollution_shaped.count(axis=0).mean()
    for key, count in pollution_shaped.count(axis=0).items():
        if count < pollution_mean:
            pollution_shaped.drop(key, axis=1, inplace=True)
    return pollution_shaped.dropna()

def pca(input_data,outfile):
    X_data1 = input_data#聚类数据，
    Sta=StandardScaler()
    # Sta=MinMaxScaler()
    # print("开始标准化")
    Sta.fit(X=X_data1)####标准化用均值跟方差算的，对有个别极值的点不敏感
    # MM=MinMaxScaler()#######最大最小归一化，现在是屏蔽的，想用这个可以取消屏蔽，这个和标准化只能选一个用
    # MM.fit(X=X_data1)#####最大最小归一化是用最大值和最小值算的，对极值比较敏感，这里可能不适用
    
    X_data1=Sta.transform(X_data1)
    pca = PCA(n_components=3)
    pca = pca.fit(X_data1)#降维
    X_dr = pca.transform(X_data1)#执行降维
    print("开始聚类")
    kmeans = KMeans(n_clusters=4,init='k-means++', n_init=10,  max_iter=300, tol=0.0001,
           verbose=0,  random_state=None,  copy_x=True,   algorithm='auto'
           )#使用Kmeans聚类，聚2类，初始化方式k-means++，随机初始质心10，最大迭代次数300，相关的扰动在两次迭代的聚类中心，
    kmeans.fit(X_data1)
    y_kmeans = kmeans.predict(X_data1)
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # for c, m, zlow, zhigh in [('r', 'o', -500, -250), ('b', '^', -300, -50)]:
    #     xs =X_dr[:,0]
    #     ys = X_dr[:,1]
    #     zs = X_dr[:,2]
        # ax.scatter(xs, ys, zs, c=y_kmeans, marker='o')
    # ax.set_xlabel('xs')
    # ax.set_ylabel('ys')
    # ax.set_zlabel('zs')
    # plt.show()

    name=np.reshape(input_data.index,(-1,1))
    y_kmeans=np.reshape(y_kmeans,(-1,1))
    out=np.concatenate((name,y_kmeans),axis=1)
    np.savetxt(outfile,out,fmt='%s')

def do_calc(infile, outfile):
    pollution_vaild = read_data(infile)
    pca(pollution_vaild, outfile)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', nargs='?', required=True)
    parser.add_argument('-o', '--outfile', nargs='?', required=True)
    args = parser.parse_args()
    do_calc(args.infile, args.outfile)
