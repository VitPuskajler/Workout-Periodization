dic = {0: {0: {0: 'Bench Press', 1: '3', 2: '2'}, 1: {0: 'Pull Ups', 1: '3', 2: '2'}}, 1: {0: {0: 'Dips', 1: '3', 2: '2'}, 1: {0: 'Hack Squats', 1: '3', 2: '2'}}}

larger_dic = {0: {0: {0: 'Bench Press', 1: '', 2: ''}, 1: {0: 'Pull Ups', 1: '', 2: ''}, 2: {0: 'Leg Raises', 1: '', 2: ''}, 3: {0: 'Rows', 1: '', 2: ''}}, 1: {0: {0: 'Dips', 1: '', 2: ''}, 1: {0: 'Chest Press', 1: '', 2: ''}, 2: {0: 'Muscle Ups', 1: '', 2: ''}, 3: {0: 'Pike Push Ups', 1: '', 2: ''}}}

for i in larger_dic:
    print(f"{larger_dic[i][0][0]}\n{dic[i][1][0]}")
