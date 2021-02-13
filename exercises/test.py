# add sliding window

 window = deque([], maxlen=length_sliding_window)

    for pos, aa in enumerate(fasta):
        window.append(aa)
        average_hydropathy_score = 0
        for base in list(window):
            average_hydropathy_score += hydropathy_dict[base]
        average_hydropathy_score = average_hydropathy_score / len(window)
        hydropathy_sequence_list.append(average_hydropathy_score)