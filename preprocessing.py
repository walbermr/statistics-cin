import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

def main():
    list_f_str = ['robot-0', 'robot-1', 'robot-2', 'robot-3', 'robot-4', 'robot-5', 'robot-10']
    for f_str in list_f_str:
        d = []
        with open('dump/' + f_str + '.dump', 'r') as f:
            d = eval(f.readline())

        data = [ eval(i) for i in d ]
        print('File size: %d' %(len(data)))

        df = pd.DataFrame.from_records(data, columns=['pwm', 'm1', 'm2', 'm3', 'm4', 'mean'])
        df.to_csv('csv/' + f_str + '.csv', index=False)


if __name__ == '__main__':
    main()