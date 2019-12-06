import pandas as pd


def process_data(num_list, input_val = 1):
    total_df = pd.DataFrame(
        {
            'source': [item.split(')')[0] for item in num_list],
            'target': [item.split(')')[1] for item in num_list]
        }

    )

    origin_df = total_df.loc[total_df['source'] == 'COM']
    origin_df.rename(columns = {'source': 'level_1', 'target': 'level_2'}, inplace = True)

    current_df = pd.DataFrame()

    x = 2
    while origin_df['level_{}'.format(x - 1)].tolist() != origin_df['level_{}'.format(x)].tolist():
        origin_df = origin_df.merge(total_df, left_on = 'level_{}'.format(x), right_on = 'source', how = 'left')
        origin_df.rename(columns = {'target': 'level_{}'.format(x + 1)}, inplace = True)
        origin_df.drop('source', axis = 1, inplace = True)

        if not origin_df.empty:
            current_df = origin_df.copy()

        x += 1

    current_df.drop_duplicates(inplace = True)

    connections = 0
    for x in range(3, 294):
        temp_df = current_df[[f'level_{a}' for a in range(1, x)]]
        temp_df.dropna(inplace = True)
        temp_df.drop_duplicates(inplace = True)

        temp_df['count'] = temp_df.count(axis = 1)
        temp_df['count'] -= 1

        connections += temp_df['count'].sum()

    print("direct and indirect orbits:", connections)

    current_df = current_df[(current_df.values == "SAN") | (current_df.values == "YOU")]

    transfers = len(list(set(current_df.values[0]).difference(current_df.values[1]))) + len(list(set(current_df.values[1]).difference(current_df.values[0]))) - 2

    print("transfers to get to Santa:", transfers)


if __name__ == '__main__':
    # part one
    DATA = open('input.txt', 'r').read().split('\n')

    process_data(DATA)
