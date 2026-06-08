GRADE_MAP = {
    'A+': {'score': 70, 'converted': 97.5},
    'A':  {'score': 67, 'converted': 90.0},
    'B+': {'score': 64, 'converted': 80.0},
    'B':  {'score': 61, 'converted': 70.0},
    'B-': {'score': 58, 'converted': 60.0},
    'C+': {'score': 55, 'converted': 50.0},
    'C':  {'score': 52, 'converted': 40.0},
    'C-': {'score': 49, 'converted': 30.0},
    'D+': {'score': 46, 'converted': 20.0},
    'D':  {'score': 43, 'converted': 10.0},
    'E':  {'score': 40, 'converted': 2.5}
}

SCORE_TO_GRADE = {meta['score']: grade for grade, meta in GRADE_MAP.items()}


def calculate_gaokao_score(main_scores, elective_inputs):
    """
    计算上海高考分数换算
    :param main_scores: dict, {'语文': 120, '数学': 130, '外语': 110}
    :param elective_inputs: list of str, ['A+', '67', 'B']
    :return: dict with calculation details and totals
    :raises: ValueError on invalid input
    """
    main_subjects = ['语文', '数学', '外语']
    for sub in main_subjects:
        if sub not in main_scores:
            raise ValueError(f"缺少主科目: {sub}")
        score = main_scores[sub]
        if not (0 <= score <= 150):
            raise ValueError(f"{sub} 分数应在 0 到 150 之间，当前值: {score}")

    main_total = sum(main_scores.values())

    if len(elective_inputs) != 3:
        raise ValueError(f"小三门数量应为3，当前数量: {len(elective_inputs)}")

    elective_details = []
    original_elective_total = 0
    converted_elective_total = 0

    for user_input in elective_inputs:
        user_input = str(user_input).strip().upper()

        if user_input in GRADE_MAP:
            grade = user_input
            orig_score = GRADE_MAP[grade]['score']
            conv_score = GRADE_MAP[grade]['converted']
        else:
            try:
                score_val = int(float(user_input))
            except (ValueError, TypeError):
                raise ValueError(f"无法识别的输入 \"{user_input}\"，请输入正确的等级或分数")

            if score_val in SCORE_TO_GRADE:
                grade = SCORE_TO_GRADE[score_val]
                orig_score = score_val
                conv_score = GRADE_MAP[grade]['converted']
            else:
                raise ValueError(
                    f"\"{user_input}\" 不是合规的上海高考小三门分数。"
                    f"合规分数仅限：70, 67, 64, 61, 58, 55, 52, 49, 46, 43, 40"
                )

        elective_details.append({
            'input': user_input,
            'grade': grade,
            'score': orig_score,
            'converted': conv_score
        })
        original_elective_total += orig_score
        converted_elective_total += conv_score

    return {
        'main_total': round(main_total, 1),
        'main_details': dict(main_scores),
        'elective_details': elective_details,
        'original_elective_total': original_elective_total,
        'converted_elective_total': round(converted_elective_total, 1),
        'original_total': round(main_total + original_elective_total, 1),
        'converted_total': round(main_total + converted_elective_total, 1)
    }
