import pandas as pd
import numpy as np

# combines duplicate columns after merging
# selects non-null value first, if both values are not null, selects left right value (ie. more up-to-date entry)
def combine(merged, col):
    x = col + '_x'
    y = col + '_y'

    merged.loc[(merged[y].isnull() & merged[x].notnull()), col] = merged[x]
    merged.loc[(merged[y].notnull()), col] = merged[y]

    merged.drop([x, y], inplace=True, axis=1)

    return merged

# combines duplicate columns after merging
# selects non-null value first, if both values are not null, concatenates values with a comma
def concat_combine(merged, col):
    x = col + '_x'
    y = col + '_y'

    merged.loc[merged[y].isnull(), col] = merged[x]
    merged.loc[merged[x].isnull(), col] = merged[y]
    merged.loc[merged[x].notnull() & merged[y].notnull(), col] = merged[x] + ', ' + merged[y]

    merged.drop([x, y], inplace=True, axis=1)

    return merged
