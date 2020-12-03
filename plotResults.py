# from utils.general import plot_results, plot_results_overlay 
import matplotlib.pyplot as plt

def plotLosses(filePath):

    f = open(filePath, 'r')
    allLines = f.readlines()
    f.close()

    x_giou_train = []
    x_giou_val = []
    x_box_train = []
    x_box_val = []
    x_class_train = []
    x_class_val = []
    x_total_train = []
    x_total_val = []
    x_P = []
    x_R = []

    y = [i for i in range(len(allLines))]

    for line in allLines:
        values = line.split()
        # print(values)
        giou_train = float(values[2])
        x_giou_train.append(giou_train)
        box_train = float(values[3])
        x_box_train.append(box_train)
        class_train = float(values[4])
        x_class_train.append(class_train)
        total_train = float(values[5])
        x_total_train.append(total_train)
        P = float(values[-7])
        x_P.append(P)
        R = float(values[-6])
        x_R.append(R)

        giou_val = float(values[-3])
        x_giou_val.append(giou_val)
        box_val = float(values[-2])
        x_box_val.append(box_val)
        class_val = float(values[-1])
        x_class_val.append(class_val)
        total_val = giou_val+box_val+class_val
        x_total_val.append(total_val)
        # print('train: ',giou_train, box_train, class_train, total_train)
        # print('val: ', giou_val, box_val, class_val, total_val)
    x_F1 = [ (2*x_P[i]*x_R[i])/(x_P[i]+x_R[i]) for i in range(len(y)) ] 

    fig, axes = plt.subplots(nrows=2, ncols=3)
    axes[0,0].plot(y, x_total_train, label='train', color='r',)
    axes[0,0].plot(y, x_total_val, label='val', color='g')
    axes[0,0].set_title('Total loss')
    axes[0,0].legend()

    axes[0,1].plot(y, x_giou_train, label='train', color='r',)
    axes[0,1].plot(y, x_giou_val, label='val', color='g')
    axes[0,1].set_title('GIoU loss')
    axes[0,1].legend()

    axes[0,2].plot(y, x_box_train, label='train', color='r',)
    axes[0,2].plot(y, x_box_val, label='val', color='g')
    axes[0,2].set_title('Box loss')
    axes[0,2].legend()

    axes[1,0].plot(y, x_class_train, label='train', color='r',)
    axes[1,0].plot(y, x_class_val, label='val', color='g')
    axes[1,0].set_title('Class loss')
    axes[1,0].legend()

    axes[1,1].plot(y, x_P, label='Precision', color='r',)
    axes[1,1].plot(y, x_R, label='Recall', color='g')
    axes[1,1].set_title('Precision,Recall')
    axes[1,1].legend()

    axes[1,2].plot(y, x_F1, label='F1', color='r',)
    axes[1,2].set_title('F1')
    axes[1,2].legend()    

    plt.show()


if __name__=='__main__':
    # plot_results_overlay()
    plotLosses('./runs/exp1/results.txt')
# plot_results_overlay()

