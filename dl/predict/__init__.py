import pandas as pd


def create_predict_file(date, time):
    # ['segmentId', 'weekday', 'hour', 'isPeakedTime', 'isWeekend']
    data = {'segmentId': [],
            'weekday': [],
            'hour': [],
            'isPeakedTime': [],
            'isWeekend': [],
            'isHoliday':[]
            }

    columns = ['segmentId', 'weekday', 'hour', 'isPeakedTime', 'isWeekend', 'isHoliday']
    df = pd.DataFrame(data, columns=columns)

    # export_csv = df.to_csv('../../data/predict/tc_predict_' + str(datetime.now().timestamp()) + '.csv', index=None,
    #                        header=True)  # Don't forget to add '.csv' at the end of the path
    export_csv = df.to_csv('../../data/predict/tc_predict.csv', index=None,
                           header=True)  # Don't forget to add '.csv' at the end of the path
    # df_old = pd.read_csv('../../data/predict/tc_predict.csv')
    for x in range(1, 40):
        df_old = pd.read_csv('../../data/predict/tc_predict.csv')
        new_data = [[x, 2, 8, 1, 0, 0]]
        # get column names of your existing data
        col_names = df_old.columns

        # make dataframe of new data that can be
        # easily appended to your old data
        df_new = pd.DataFrame(data=new_data, columns=col_names)

        # concatenate old and new
        df_complete = pd.concat([df_old, df_new], axis=0)
        # write your complete dataset to a new csv.
        df_complete.to_csv('../../data/predict/tc_predict.csv', index=False)

    # print(df)


if __name__ == '__main__':
    print('create predict file for Trường Chinh street')
    day = '2019-05-19'
    time = 8
    create_predict_file(day, time)
