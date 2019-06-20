import pandas as pd
import matplotlib.pyplot as plt

def main():

    df = pd.read_csv('csv/robot-0.csv')

    data = { 'pwm': list(df.to_dict()['pwm'].values()),
                'm1': list(df.to_dict()['m1'].values()),
                'm2': list(df.to_dict()['m2'].values()),
                'm3': list(df.to_dict()['m3'].values()),
                'm4': list(df.to_dict()['m4'].values()),
                'mean': list(df.to_dict()['mean'].values()),
            }

    plt.scatter('pwm', 'm1', c='b', data=data)

    df = pd.read_csv('csv/robot-10.csv')

    data = { 'pwm': list(df.to_dict()['pwm'].values()),
                'm1': list(df.to_dict()['m1'].values()),
                'm2': list(df.to_dict()['m2'].values()),
                'm3': list(df.to_dict()['m3'].values()),
                'm4': list(df.to_dict()['m4'].values()),
                'mean': list(df.to_dict()['mean'].values()),
            }

    plt.scatter('pwm', 'm1', c='r', data=data)
    plt.show()

if __name__ == '__main__':
    main()