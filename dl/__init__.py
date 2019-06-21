from datetime import datetime

import pandas as pd
import tzlocal


def concatData(i):
    return pd.concat(
        [pd.read_csv("../data/week" + str(i) + "/" + str(x), header=None) for x in range(7 * (i - 1), 7 * i)])


def genTime(timestamp):
    unix_timestamp = timestamp // 1000
    local_timezone = tzlocal.get_localzone()  # get pytz timezone
    local_time = datetime.fromtimestamp(unix_timestamp, local_timezone)
    return local_time.strftime("%Y-%m-%d %H:%M:%S")


def genWeekDay(timestamp):
    unix_timestamp = timestamp // 1000
    local_timezone = tzlocal.get_localzone()  # get pytz timezone
    local_time = datetime.fromtimestamp(unix_timestamp, local_timezone)
    return local_time.weekday()


def genIsWeekend(day):
    return 1 if day in [5, 6] else 0


def genIsPeakedTime(hour):
    return 1 if (hour > 6 and hour < 8) or (hour > 11 and hour < 14) or (hour > 16 and hour < 19.5) else 0

def genIsHoliday(timestamp):
    unix_timestamp = timestamp//1000
    local_timezone = tzlocal.get_localzone() # get pytz timezone
    local_time = datetime.fromtimestamp(unix_timestamp, local_timezone)
    day = (int(local_time.day),int(local_time.month))
    holiday = [(31,1),(2,9),(5,4),(20,10),(20,11),(1,1),(24,12),(30,4),(1,5),(1,6),(8,3)]
    out = 1 if day in holiday else 0
    return out

def genIsHoliday(timestamp):
    unix_timestamp = timestamp // 1000
    local_timezone = tzlocal.get_localzone()  # get pytz timezone
    local_time = datetime.fromtimestamp(unix_timestamp, local_timezone)
    day = (int(local_time.day), int(local_time.month))
    holiday = [(2, 9), (20, 10), (20, 11), (1, 1), (30, 4), (1, 5), (1, 6), (8, 3)]
    return 1 if day in holiday else 0


def genHours(timestamp):
    unix_timestamp = timestamp // 1000
    local_timezone = tzlocal.get_localzone()  # get pytz timezone
    local_time = datetime.fromtimestamp(unix_timestamp, local_timezone)
    hour = int(local_time.hour)
    minute = int(local_time.minute)
    second = int(local_time.second)
    return hour + (minute * 60 + second) / 3600


def genLable(speed):
    if speed < 5 and speed > 0:
        return "Red"
    elif speed >= 5 and speed < 10:
        return "Orange"
    elif speed >= 10 and speed < 15:
        return "Yellow"
    elif speed >= 15:
        return "Green"


def concatResData(lst):
    return pd.concat([pd.read_csv("../data/week" + str(x) + "/ltk_week_data.csv", low_memory=False) for x in lst])


def genDataSet(streetID, file_name_gen_for_week, datasetName):
    for i in list(range(1, 8)):
        df = concatData(i)
        df[0] = df[0].apply(lambda x: x - (streetID << 16))
        df = df[(df[0] > 0) & (df[0] < 100)].sort_values([0, 8]).reset_index()[[0, 1, 8]]
        df['weekday'] = df[8].apply(genWeekDay)
        df['hour'] = df[8].apply(genHours)
        df['isPeakedTime'] = df['hour'].apply(genIsPeakedTime)
        df['isWeekend'] = df['weekday'].apply(genIsWeekend)
        df['isHoliday'] = df[8].apply(genIsHoliday)
        df['congestion'] = df[1].apply(genLable)
        df.columns = ['segmentId', 'speed', 'timestamp', 'weekday', 'hour', 'isPeakedTime', 'isWeekend', 'isHoliday',
                      'congestion']
        df.to_csv('../data/week' + str(i) + '/' + file_name_gen_for_week + '.csv', index=False)
    df = concatResData(list(range(1, 8)))  # w 1,2,3,4,5,6,7
    df.to_csv(datasetName + '.csv', index=False)

def cleaning(dataset_name, cleaned_dataset_name):
    df = pd.read_csv(dataset_name + '.csv', low_memory=False)
    q1 = df['speed'].quantile(0.25)
    q3 = df['speed'].quantile(0.75)
    IQR = q3 - q1
    outlier_range = (q1 - IQR * 1.5, q3 + IQR * 1.5)
    res = df[(df.speed > outlier_range[0]) & (df.speed < outlier_range[1]) & (df.speed > 0)]
    res.to_csv(cleaned_dataset_name + '.csv', index=False)

def cleaning_simple(dataset_name, cleaned_dataset_name):
    df = pd.read_csv(dataset_name + '.csv', low_memory=False)
    res = df[(df.speed > 0)]
    res.to_csv(cleaned_dataset_name + '.csv', index=False)

def replicate(trainfile, outputfile, replicate_label, reference_label, header='infer'):
    df = pd.read_csv(trainfile, header=header, low_memory=False)
    df.columns = ['segmentId', 'weekday', 'hour', 'isPeakedTime', 'isWeekend', 'congestion']
    print("Before:")
    print(df['congestion'].value_counts(dropna=False))
    replicate_data = df[df['congestion'] == 'Red'].copy()
    newdf = df.copy()
    replicate_count = sum(df['congestion'] == replicate_label)
    reference_count = sum(df['congestion'] == reference_label)
    for i in range(int(round(reference_count / replicate_count, 0))):
        newdf.append(replicate_data)
    print("After:")
    print(newdf['congestion'].value_counts(dropna=False))
    newdf.to_csv(outputfile, index=False)


def drop_speed(clean_file, outputfile, header='infer'):
    dataset = pd.read_csv(clean_file)
    X = dataset.drop('speed', axis=1)
    X.to_csv(outputfile, index=False)

def precesorData():
    startTime = datetime.now().timestamp();
    print(datetime.now());

    # genDataSet(220860894, 'ltk_week_data', 'train_ltk')
    # genDataSet(219861105, 'tc_week_data', 'train_tc')
    #
    # cleaning('train_ltk', 'train_ltk_cleaned')
    # cleaning('train_tc', 'train_tc_cleaned')
    # drop_speed('train_ltk_cleaned.csv', 'new_train_ltk.csv')
    drop_speed('train_tc_cleaned.csv', 'new_train_tc.csv')
    print(datetime.now())
    print('Time took: ' + str(datetime.now().timestamp() - startTime) + ' s')

precesorData()