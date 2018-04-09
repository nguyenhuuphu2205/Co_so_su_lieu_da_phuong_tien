import cv2
import math
import numpy as np
import time
#from scipy import spatial
# Ham tinh hieu giua 2 histogram 2frame lien tiep trong video
def distance_histograms():
    file=open("distance_3.txt",'w')
    cap=cv2.VideoCapture("video3.mp4")
    array_distance_hist=[]
    ret,frame_i=cap.read()
    i=0
    while cap.isOpened():
        if i>750:
            break

        ret,frame_j=cap.read()
        if ret:
            i=i+1
            frame_j_temp=cv2.cvtColor(frame_j,cv2.COLOR_BGR2GRAY)
            frame_i_temp=cv2.cvtColor(frame_i,cv2.COLOR_BGR2GRAY)
            hist_frame_i=cv2.calcHist([frame_i_temp],[0],None,[256],[0,256])
            hist_frame_j=cv2.calcHist([frame_j_temp],[0],None,[256],[0,256])
            #distance_hist=cv2.compareHist(hist_frame_i,hist_frame_j,cv2.HISTCMP_CORREL) # Tinh do tuong dong 2 histogram
            distance_hist=distance_histogram(hist_frame_i,hist_frame_j) # Tinh do tuong dong giua 2 histogram dung khoang cach euclide
            #distance_hist=spatial.distance.cosine(hist_frame_i,hist_frame_j) # Tinh do tuong dong 2 histogram dung khoang cach cosin
            file.write(str(distance_hist)+"\n")
            array_distance_hist.append(distance_hist)
            #del frame_j_temp[:]
            del frame_i_temp
            #del frame_i_temp[:]
            del frame_j_temp
            frame_i=frame_j
            del frame_j

        else :
            break
    cap.release()
    file.close()
    return array_distance_hist
# Ham tinh khoang cach 2 histogram theo khoang cach euclide
def distance_histogram(hist1,hist2):
    if len(hist1)==len(hist2):
        sum=0
        for i in xrange(len(hist1)):
            sum=sum+pow(hist1[i]-hist2[i],2)
        return math.sqrt(sum)
#Ham tim nguong cho video
# t=0 : nguong trung binh
# t=1 :nguong trung vi
def compute_threshold(list_distances,t):
    if t==0:
        return np.mean(list_distances)
    else:
        return np.median(list_distances)
def compute_threshold_extend(list_distances):
    temp=[]
    ind=np.argpartition(list_distances,-10)[-10:]
    for i in ind:
        temp.append(list_distances[i])
    return np.mean(temp)
def threshold_video():
    list_distances=distance_histograms()
    threshold=compute_threshold_extend(list_distances)
    array_index=[]
    for i in xrange(len(list_distances)):
        if list_distances[i]>=threshold*0.7:
            array_index.append(i)

    cap=cv2.VideoCapture('video3.mp4')
    array_frame_temp=[]
    i=0

    while cap.isOpened():
        if i>750:
            break
        if is_in_range(i,array_index)==True:
            if len(array_frame_temp)>10:
                write_video(array_frame_temp,"video_output"+str(i)+".avi")
                get_key_frame_extend(array_frame_temp,i)
                time.sleep(4)
            else:
                get_key_frame_extend(array_frame_temp, i)
                #array_frame_temp = []
            del array_frame_temp[:]
            del array_frame_temp
            array_frame_temp=[]

        ret, frame = cap.read()
        if ret:
            i=i+1
            array_frame_temp.append(frame)
        else:
            break
    cap.release()



# Ham ghi cac frame thanh 1 video
def write_video(list_frame,filename):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter("./video/"+filename, fourcc, 20, (1280, 720))
    for frame in list_frame:
        cv2.imshow('frame',frame)
        cv2.waitKey(25)
        out.write(frame)
    out.release()

def is_in_range(t,list):
    for i in list:
        if t==i:
            return True
    return False
def get_key_frame(list_frame,i):
    key=list_frame[len(list_frame)//2]
    cv2.imwrite('./keyframe/'+'keyframe_'+str(i-len(list_frame))+'-'+str(i)+'.jpg',key)
def get_key_frame_extend(list_frame,i):
    t=i
    array_hist=[]
    avg=[]
    sum = 0;
    smallestIndex = 0;
    smallest = 1000000;
    for i in list_frame:
        frame_i_temp = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)
        hist_frame_i = cv2.calcHist([frame_i_temp], [0], None, [256], [0, 256])
        array_hist.append(hist_frame_i)
    for j in range(len(array_hist[0])):
        sum=0;
        for i in range(len(array_hist)):
            sum+=array_hist[i][j]
        avg.append(sum/len(array_hist))

    for i in range(len(array_hist)):
        if(distance_histogram(array_hist[i],avg) < smallest):
            smallestIndex=i
            smallest=distance_histogram(array_hist[i],avg)
    cv2.imwrite('./keyframe/' + 'keyframe_' + str(t - len(list_frame)) + '-' + str(t) + '.jpg', list_frame[smallestIndex])


    # tb=np.mean(array_hist)
    # array_temp=[]
    # for i in list_frame:
    #     array_temp.append(abs(i-tb))
    # t=np.array(array_temp)
    # key=t.min()
    # cv2.imwrite('./keyframe/' + 'keyframe_' + str(i - len(list_frame)) + '-' + str(i) + '.jpg', )
if __name__=='__main__':
    threshold_video()



