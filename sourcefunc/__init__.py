import pandas as pd


def head(df: pd.DataFrame, n=10):
    print(df.head(n).to_string())


def describe(df: pd.DataFrame, d=None):
    if d is None:
        d = [0.01, 0.05, 0.95, 0.99]
    elif not isinstance(d, list):
        d = [d]
    else:
        d = list(d)

    df.describe([0.1 * i for i in range(10)] + d)


def read(filename):
    import pickle
    with open(filename, 'rb') as f:
        return pickle.load(f)


def write(filename, input_):
    import pickle
    with open(filename, 'wb') as f:
        pickle.dump(input_, f)


def task_cost(ddf):
    """
    Аггрегирует между собой все пересекающиеся периоды
    """
    start = sorted(ddf[['start', 'tasks']].to_numpy(), key=lambda x: x[0], reverse=True)
    end = sorted(ddf[['end', 'tasks', 'tid']].to_numpy(), key=lambda x: x[0], reverse=True)
    r = []

    counter = 0
    x_start = start[-1][0]
    started_tasks = 0
    completed_tasks = list()

    while start or end:
        if start and (start[-1][0] < end[-1][0]):
            _, start_n = start.pop()
            counter += start_n
            started_tasks += start_n

        else:
            end_time, end_n, tid = end.pop()
            counter -= end_n
            completed_tasks.append((tid, end_n))

            if counter == 0:
                r.append([x_start, end_time, started_tasks, tuple(completed_tasks)])
                if start:
                    x_start = start[-1][0]
                    started_tasks = 0
                    completed_tasks = list()
                elif end:
                    assert False, "Here 'end' value must be empty"

    return pd.DataFrame(r, columns='start end tasks completed_tasks'.split())


