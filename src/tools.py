import numpy as np
import pyqtgraph as pg

# def matplotlib_show(data: list[list | np.ndarray]) -> None:
#     """将数据打包显示至matplotlib图表"""
#     # matplotlib.use("QtAgg")
#
#     for i in range(len(data)):
#         plt.subplot(len(data), 1, i + 1)
#         plt.plot(data[i])
#     plt.show()

def plot_show(data):
    pw = pg.plot()
    curve = pw.plot()
    curve.setData(np.arange(len(data)), data)
    pg.Qt.exec_()