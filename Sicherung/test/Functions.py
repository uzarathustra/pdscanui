import matplotlib.pyplot as plt


dataList = []
dataForErrorAnalysisMotor1 = []
dataForErrorAnalysisMotor2 = []
dataForErrorAnalysisMotor3 = []


def draw_plot(y_data, mot):
    x_data = []
    for i in range(len(y_data)):
        x_data.append(i)

    if mot == 1:
        plt.plot(x_data, y_data, label=f"Motor 1 - {y_data[-1]/8344*360}")
    if mot == 2:
        plt.plot(x_data, y_data, label=f"Motor 2 - {y_data[-1]/8344*360}")
    if mot == 3:
        plt.plot(x_data, y_data, label=f"Motor 3 - {y_data[-1]/8344*360}")

    plt.xlabel('x-axis')
    plt.ylabel('EncoderValue')

    plt.title('EncoderValue - photoDiodeDataMissing')
    # plt.legend()

    plt.draw()


def show_plots():
    plt.show()


def plot_test(y_data):
    plt.axis([-30000, 30000, -30000, 30000])

    for i in range(len(y_data)):
        plt.scatter(y_data[i], y_data[i])
        plt.pause(0.05)

    plt.show()
