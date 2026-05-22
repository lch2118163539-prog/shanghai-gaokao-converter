def calculate_gaokao_score_v1():
    print("=== 上海高考分数换算器 V1.0 ===")
    
    # 建立等级、上海原始分、全国百分位赋分（100分制）的映射表
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
    
    # 创建反向查找表，用于通过分数匹配等级
    SCORE_TO_GRADE = {meta['score']: grade for grade, meta in GRADE_MAP.items()}

    # 1. 分开输入语数外三门分数
    main_subjects = ['语文', '数学', '外语']
    main_scores = {}
    
    print("\n[第一步] 请输入主三门分数（单科满分 150 分）：")
    for sub in main_subjects:
        try:
            score = float(input(f"请输入【{sub}】的分数："))
            if not (0 <= score <= 150):
                print(f"错误：{sub} 分数应在 0 到 150 之间。")
                return
            main_scores[sub] = score
        except ValueError:
            print("错误：请输入有效的数字。")
            return

    main_total = sum(main_scores.values())

    # 2. 输入小三门（支持等级或具体合规分数）
    original_elective_total = 0
    converted_elective_total = 0
    
    print("\n[第二步] 请输入小三门结果（输入等级如 A+, B- 或 对应合规分数 70, 67, ..., 40）：")
    for i in range(1, 4):
        user_input = input(f"请输入第 {i} 门小三门的结果：").strip().upper()
        
        # 判断用户输入的是等级还是分数
        if user_input in GRADE_MAP:
            grade = user_input
            orig_score = GRADE_MAP[grade]['score']
            conv_score = GRADE_MAP[grade]['converted']
        else:
            try:
                score_val = int(float(user_input))
                if score_val in SCORE_TO_GRADE:
                    grade = SCORE_TO_GRADE[score_val]
                    orig_score = score_val
                    conv_score = GRADE_MAP[grade]['converted']
                else:
                    print(f"错误：{user_input} 不是合规的上海高考小三门分数。")
                    print("合规分数仅限：70, 67, 64, 61, 58, 55, 52, 49, 46, 43, 40")
                    return
            except ValueError:
                print(f"错误：无法识别的输入 \"{user_input}\"，请输入正确的等级或分数。")
                return
        
        original_elective_total += orig_score
        converted_elective_total += conv_score

    # 3. 计算总分
    original_total = main_total + original_elective_total
    converted_total = main_total + converted_elective_total

    # 4. 输出明细与换算结果
    print("\n" + "="*15 + " 分数明细 " + "="*15)
    print(f"主三门总分：{round(main_total, 1)} 分 (语文:{main_scores['语文']}, 数学:{main_scores['数学']}, 外语:{main_scores['外语']})")
    print(f"小三门原分：{original_elective_total} 分")
    print(f"小三门换算：{round(converted_elective_total, 1)} 分")
    print("="*38)
    print(f"原本总分（满分660）：{round(original_total, 1)} 分")
    print(f"换算后总分（满分750）：{round(converted_total, 1)} 分")

if __name__ == "__main__":
    calculate_gaokao_score_v1()
