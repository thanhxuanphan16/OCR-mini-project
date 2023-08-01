## Update: Oct 2021
import numpy as np
import imageio
import pydicom as dicom
import matplotlib.pyplot as plt

### Statistics and histogram ###################################
def ImageInfor(inputfile, isdicom=False):
    if (isdicom):
        dc = dicom.read_file(inputfile)
        a = dc.pixel_array
    else:
        a = imageio.imread(inputfile) # numpy array
        
    """ Xem thông tin thống kê của ảnh """
    print(f"Ảnh................: {inputfile}")
    print(f"Kích thước.........: {a.shape}")
    print(f"Loại dữ liệu.......: {a.dtype}")
    print(f"Độ đậm trung bình..: {a.mean()}")
    print(f"Độ đậm nhỏ nhất....: {a.min()}")
    print(f"Độ đậm lớn nhất....: {a.max()}")
    print("--------------------------------")
    return a

### PLOT PLOT PLOT ##############################
def showImg(a,title):
    """ Vẽ ảnh """
    plt.imshow(a, cmap=plt.cm.gray)
    plt.title(title)
    plt.axis('off')

def showHist(hist,bin_edges,xmin=None,xmax=None,ymin=None,ymax=None):
    """ Vẽ biểu đồ phân bố độ xám """
    if (xmin == None): xmin = bin_edges.min()
    if (xmax == None): xmax = bin_edges.max() 
    if (ymin == None): ymin = hist.min()
    if (ymax == None): ymax = 1.05*hist.max()

    plt.plot(bin_edges[0:-1], hist)
    plt.title("Biểu đồ độ xám")
    plt.xlabel("Độ xám")
    plt.ylabel("Số pixel")
    plt.xlim([xmin, xmax])
    plt.ylim([ymin, ymax])

def ImageHist(img1=[],hxmin=None,hxmax=None,nbins=None,bstep=1,pltymin=None,pltymax=None,
              img2=[],otitle='Ảnh kết quả'):
    """ 
    Vẽ ảnh gốc, ảnh kết quả và histogram
    - img1: ma trận ảnh gốc
    - hxmin: độ đậm thấp nhất
    - hxmax: độ đậm cao nhất
    - nbins: số bin
    - bstep: số độ xám trong mỗi bin
    - pltymin: giâ trị y nhỏ nhẩt trên đồ thị
    - pltymax: giâ trị y lớn nhẩt trên đồ thị
    - img2: ma trận ảnh kết quả
    - otitle: tiêu đề ảnh kết quả
    """
    if (len(img1)==0):
        help(ImageHist)
        return
    
    # Thống kê histogram:
    if (hxmin==None): hxmin = img1.min()
    if (hxmax==None): hxmax = img1.max()
    if (nbins==None): nbins = (hxmax - hxmin)//bstep
    # Tạo biểu đồ từ xmin đến xmax với nbins khoảng chia
    hist, bin_edges = np.histogram(img1,bins=nbins,range=[hxmin,hxmax])

    # Thống kê từ histogram:
    print('Đồ thị phân bố độ đậm (histogram):')
    print(f"Khoảng độ đậm.......: [{bin_edges.min()}, {bin_edges.max()}]")
    print(f"Số khoảng chia......: {nbins} bin")
    print(f"Số pixel thấp nhất..: {hist.min()}, bin id: {np.where(hist == hist.min())[0]}")
    print(f"Số pixel cao nhất...: {hist.max()}, bin id: {np.where(hist == hist.max())[0]}")
    print(f"Tổng số pixel.......: {hist.sum()}")
    
    # Vẽ ảnh gốc, histogram và ảnh kết quả (nếu có)
    plt.figure(figsize=(20,5))
    plt.subplot(131)
    showImg(img1,"Ảnh gốc")
    plt.subplot(132)
    showHist(hist,bin_edges,hxmin,hxmax,pltymin,pltymax)
    if (not len(img2)==0):
        plt.subplot(133)
        showImg(img2,otitle)
    plt.show()
    

def MultipleImages(imgs,titles=[],figsize=[20,5],ncols=2):
    nimg = len(imgs)
    nrows = nimg//ncols
    if (nimg % ncols): nrows = nrows + 1

    # Tạo khung hình (fig), và dãy các trục tọa độ (ax)
    fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)
    
    ai = 0
    for i, axi in enumerate(ax.flat):
        # i chạy từ 0 đến (nrows*ncols-1); 
        # axi tương đương với ax[rowid][colid]
        # rowid = i // ncols
        # colid = i % ncols
        axi.axis('off')
        if (ai < len(imgs)):
            axi.imshow(imgs[ai],cmap=plt.cm.gray)
            if (len(imgs) == len(titles)): 
                axi.set_title(titles[ai])
            ai = ai + 1
    plt.tight_layout()
    plt.show()