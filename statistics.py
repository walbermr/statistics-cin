import pandas as pd
import matplotlib.pyplot as plt

def main():

    df_a = pd.read_csv('csv/robot-0.csv')

    data_a = { 'pwm': list(df_a.to_dict()['pwm'].values()),
                'm1': list(df_a.to_dict()['m1'].values()),
                'm2': list(df_a.to_dict()['m2'].values()),
                'm3': list(df_a.to_dict()['m3'].values()),
                'm4': list(df_a.to_dict()['m4'].values()),
                'mean': list(df_a.to_dict()['mean'].values()),
            }

    df_b = pd.read_csv('csv/robot-10.csv')

    data_b = { 'pwm': list(df_b.to_dict()['pwm'].values()),
                'm1': list(df_b.to_dict()['m1'].values()),
                'm2': list(df_b.to_dict()['m2'].values()),
                'm3': list(df_b.to_dict()['m3'].values()),
                'm4': list(df_b.to_dict()['m4'].values()),
                'mean': list(df_b.to_dict()['mean'].values()),
            }


    m_l = ['m1', 'm2', 'm3', 'm4']
    for m in m_l:
        _, ax = plt.subplots()
        r1 = ax.scatter('pwm', m, c='b', data=data_a)
        r2 = ax.scatter('pwm', m, c='r', data=data_b)
        ax.legend((r1, r2), ('truth', 'test'))
        plt.show()

if __name__ == '__main__':
    main()