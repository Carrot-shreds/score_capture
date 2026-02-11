import time

import numpy as np
import pyqtgraph as pg

# from matplotlib import pyplot as plt


# def matplotlib_show(data: list[list | np.ndarray]) -> None:
#     """将数据打包显示至matplotlib图表"""
#     # matplotlib.use("QtAgg")

#     for i in range(len(data)):
#         plt.subplot(len(data), 1, i + 1)
#         plt.plot(data[i])
#     plt.show()


def timeit[T](func: T) -> T:
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)  # type:ignore
        end_time = time.time()
        print(
            f"{func.__name__ if hasattr(func, '__name__') else ''} executed in {end_time - start_time:.6f} seconds"
        )
        return result

    return wrapper  # type:ignore


def plot_show(data):
    pw = pg.plot()
    curve = pw.plot()
    curve.setData(np.arange(len(data)), data)
    pg.Qt.exec_()
