import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from scipy import stats

max_pwm = 70
# m_l = ['m1']

def mean_std_parser(faulty=False):
    global max_pwm

    prefix = 'csv/robot-'

    pwm_vel = []
    for i in range(0, max_pwm):
        pwm_vel.append([])

    max = range(0, 6) if not faulty else [10]
    m_l = ['m1', 'm2', 'm3', 'm4'] if not faulty else ['m1']

    for i in max:
        f_name = prefix + str(i) + '.csv'
        df = pd.read_csv(f_name)
        if not faulty:
            data = { 'pwm': list(df.to_dict()['pwm'].values()),
                'm1': list(df.to_dict()['m1'].values()),
                'm2': list(df.to_dict()['m2'].values()),
                'm3': list(df.to_dict()['m3'].values()),
                'm4': list(df.to_dict()['m4'].values())
            }
        else:
            data = { 'pwm': list(df.to_dict()['pwm'].values()),
                'm1': list(df.to_dict()['m1'].values()),
            }

        for m in m_l:
            motor_velocities = np.array(data[m]).reshape((-1, 70))
            for pwm in range(10, max_pwm):
                pwm_vel[pwm] += list(motor_velocities[:, pwm])

    pwm_vel = np.array(pwm_vel)
    for pwm in range(0, max_pwm):
        for i in range(0, len(pwm_vel[pwm])):
            pwm_vel[pwm][i] = -pwm_vel[pwm][i] if pwm_vel[pwm][i] < 0 else pwm_vel[pwm][i]
    
    return pwm_vel[10:]


def combined_p_test():
    global max_pwm

    prefix = 'csv/robot-'

    m_l = ['m1', 'm2', 'm3', 'm4']

    faulty_df = pd.read_csv('csv/robot-10.csv')
    faulty_data = { 'm1': list(faulty_df.to_dict()['m1'].values()) }
    faulty_motor_velocities = np.array(faulty_data['m1']).reshape((-1, 70))[:, 10:]
    comb_p_val_l = []

    for i in range(0, 6):
        f_name = prefix + str(i) + '.csv'
        df = pd.read_csv(f_name)
        data = { 'pwm': list(df.to_dict()['pwm'].values()),
            'm1': list(df.to_dict()['m1'].values()),
            'm2': list(df.to_dict()['m2'].values()),
            'm3': list(df.to_dict()['m3'].values()),
            'm4': list(df.to_dict()['m4'].values())
        }

        for m in m_l:
            motor_velocities = np.array(data[m]).reshape((-1, 70))[:, 10:]
            p_val_l = []

            for pwm in range(0, max_pwm-10):
                _, p = stats.wilcoxon(motor_velocities[:, pwm], faulty_motor_velocities[:, pwm])
                p_val_l.append(p)
            
            _, comb_p_val = stats.combine_pvalues(p_val_l)
            comb_p_val_l.append(comb_p_val)
    
    print(len(comb_p_val_l))
    print('\n\n')
    for p in comb_p_val_l:
        print('%0.4f' %(p))


    _, p = stats.combine_pvalues(comb_p_val_l)
    print('\n\n%0.4f' %(p))

    return comb_p_val_l



def main():
    global max_pwm
    global m_l

    pwm_vel = mean_std_parser()
    faulty_vel = mean_std_parser(faulty=True)
    
    pwm_mean, pwm_std = [np.mean(pwm_vel[i]) for i in range(0, max_pwm-10)], \
                            [np.std(pwm_vel[i]) for i in range(0, max_pwm-10)]

    faulty_mean, faulty_std = [np.mean(faulty_vel[i]) for i in range(0, max_pwm-10)], \
                                [np.std(faulty_vel[i]) for i in range(0, max_pwm-10)]

    print([stats.kstest(x, 'norm')[1] for x in pwm_vel])

    pwm_mean, pwm_std = np.array(pwm_mean).reshape(-1, 1), np.array(pwm_std).reshape(-1, 1)
    faulty_mean, faulty_std = np.array(faulty_mean).reshape(-1, 1), np.array(faulty_std).reshape(-1, 1)

    _, ax = plt.subplots()  
    # r1 = plt.errorbar(list(range(10, max_pwm)), pwm_mean, pwm_std, marker='.')
    # r2 = plt.errorbar(list(range(10, max_pwm)), faulty_mean, faulty_std, marker='^')

    r1 = plt.scatter(list(range(10, max_pwm)), pwm_mean)
    r2 = plt.scatter(list(range(10, max_pwm)), faulty_mean)

    ax.legend((r1, r2), ('Normal', 'Robot10'))
    plt.xlabel('PWM')
    plt.ylabel('Velocidade')
    plt.show()

    return

def normal_plot():
    pwm_vel = mean_std_parser()
    faulty_vel = mean_std_parser(faulty=True)

    _, ax = plt.subplots()
    r1 = plt.scatter(list(range(10, max_pwm)), pwm_vel)
    r2 = plt.scatter(list(range(10, max_pwm)), faulty_vel)
    ax.legend((r1, r2), ('Motor normal', 'Robot10'))
    plt.show()

def normal_plo2t():
    df_a = pd.read_csv('csv/robot-0.csv')
    
    data_a = {
                'm1': np.array(list(df_a.to_dict()['m1'].values())).reshape((-1, 70))[:, 10:],
                'm2': np.array(list(df_a.to_dict()['m2'].values())).reshape((-1, 70))[:, 10:],
                'm3': np.array(list(df_a.to_dict()['m3'].values())).reshape((-1, 70))[:, 10:],
                'm4': np.array(list(df_a.to_dict()['m4'].values())).reshape((-1, 70))[:, 10:],
                'mean': list(df_a.to_dict()['mean'].values()),
            }

    df_b = pd.read_csv('csv/robot-10.csv')

    data_b = { 'm1': np.array(list(df_b.to_dict()['m1'].values())).reshape((-1, 70))[:, 10:],
                'm2': np.array(list(df_b.to_dict()['m2'].values())).reshape((-1, 70))[:, 10:],
                'm3': np.array(list(df_b.to_dict()['m3'].values())).reshape((-1, 70))[:, 10:],
                'm4': np.array(list(df_b.to_dict()['m4'].values())).reshape((-1, 70))[:, 10:],
                'mean': list(df_b.to_dict()['mean'].values()),
            }
    
    
    _, ax = plt.subplots()
    x = list(range(10, max_pwm))

    for i in range(data_a['m1'].shape[0]):
        for j in range(data_a['m1'].shape[1]):
            if(data_a['m1'][i][j] < 0):
                data_a['m1'][i][j] = -data_a['m1'][i][j]
                data_a['m2'][i][j] = -data_a['m2'][i][j]
                data_a['m3'][i][j] = -data_a['m3'][i][j]
                data_a['m4'][i][j] = -data_a['m4'][i][j]
                data_b['m1'][i][j] = -data_b['m1'][i][j]

    plt.plot(x, list(map(np.mean, list(data_a['m1'].transpose()))), label="Motor 1")
    plt.plot(x, list(map(np.mean, list(data_a['m2'].transpose()))), label="Motor 2")
    plt.plot(x, list(map(np.mean, list(data_a['m3'].transpose()))), label="Motor 3")
    plt.plot(x, list(map(np.mean, list(data_a['m4'].transpose()))), label="Motor 4")
    plt.plot(x, list(map(np.mean, list(data_b['m1'].transpose()))), label="Motor Robot10")

    ax.legend(loc='top left')


    plt.xlabel('PWM')
    plt.ylabel('Velocidade')

    plt.show()

    return


# if __name__ == '__main__':
#     main()

#     _, ax = plt.subplots()
#     r1 = plt.scatter(list(range(10, max_pwm)), pwm_vel)
#     r2 = plt.scatter(list(range(10, max_pwm)), faulty_vel)
#     ax.legend((r1, r2), ('Motor normal', 'Robot10'))
#     plt.show()

if __name__ == '__main__':
    normal_plo2t()
    # normal_plot()
    # combined_p_test()
    # main()