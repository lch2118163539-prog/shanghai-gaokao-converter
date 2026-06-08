import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from main import calculate_gaokao_score, GRADE_MAP, SCORE_TO_GRADE


class TestGradeMap:
    def test_all_grades_have_three_keys(self):
        for grade, meta in GRADE_MAP.items():
            assert 'score' in meta
            assert 'converted' in meta

    def test_score_to_grade_reverse_mapping(self):
        for grade, meta in GRADE_MAP.items():
            assert SCORE_TO_GRADE[meta['score']] == grade

    def test_scores_are_in_descending_order(self):
        scores = [meta['score'] for _, meta in GRADE_MAP.items()]
        assert scores == sorted(scores, reverse=True)


class TestCalculateGaokaoScore:
    def test_valid_input_all_grades(self):
        result = calculate_gaokao_score(
            {'语文': 120, '数学': 130, '外语': 140},
            ['A+', 'A', 'B+']
        )
        assert result['main_total'] == 390
        assert result['original_elective_total'] == 70 + 67 + 64
        assert result['converted_elective_total'] == 97.5 + 90.0 + 80.0
        assert result['original_total'] == 390 + 70 + 67 + 64
        assert result['converted_total'] == 390 + 97.5 + 90.0 + 80.0
        assert len(result['elective_details']) == 3

    def test_valid_input_mixed_grades_and_scores(self):
        result = calculate_gaokao_score(
            {'语文': 100, '数学': 110, '外语': 120},
            ['A+', '67', 'B']
        )
        assert result['main_total'] == 330
        assert result['elective_details'][0]['input'] == 'A+'
        assert result['elective_details'][0]['grade'] == 'A+'
        assert result['elective_details'][1]['input'] == '67'
        assert result['elective_details'][1]['grade'] == 'A'
        assert result['elective_details'][2]['input'] == 'B'
        assert result['elective_details'][2]['grade'] == 'B'

    def test_valid_input_lowercase_grades(self):
        result = calculate_gaokao_score(
            {'语文': 100, '数学': 100, '外语': 100},
            ['a+', 'b-', 'e']
        )
        assert result['elective_details'][0]['grade'] == 'A+'
        assert result['elective_details'][1]['grade'] == 'B-'
        assert result['elective_details'][2]['grade'] == 'E'

    def test_valid_input_with_spaces(self):
        result = calculate_gaokao_score(
            {'语文': 100, '数学': 100, '外语': 100},
            ['  A+ ', ' B', 'c+']
        )
        assert result['elective_details'][0]['grade'] == 'A+'
        assert result['elective_details'][1]['grade'] == 'B'
        assert result['elective_details'][2]['grade'] == 'C+'

    def test_all_valid_scores_accepted(self):
        for score in [70, 67, 64, 61, 58, 55, 52, 49, 46, 43, 40]:
            result = calculate_gaokao_score(
                {'语文': 0, '数学': 0, '外语': 0},
                [str(score), 'A+', 'A+']
            )
            assert result['elective_details'][0]['score'] == score

    def test_missing_main_subject(self):
        with pytest.raises(ValueError, match='缺少主科目'):
            calculate_gaokao_score(
                {'语文': 100, '数学': 100},
                ['A+', 'A', 'A']
            )

    def test_main_score_out_of_range_negative(self):
        with pytest.raises(ValueError, match='0 到 150'):
            calculate_gaokao_score(
                {'语文': -1, '数学': 100, '外语': 100},
                ['A+', 'A', 'A']
            )

    def test_main_score_out_of_range_high(self):
        with pytest.raises(ValueError, match='0 到 150'):
            calculate_gaokao_score(
                {'语文': 151, '数学': 100, '外语': 100},
                ['A+', 'A', 'A']
            )

    def test_main_score_at_boundary_zero(self):
        result = calculate_gaokao_score(
            {'语文': 0, '数学': 0, '外语': 0},
            ['E', 'E', 'E']
        )
        assert result['main_total'] == 0

    def test_main_score_at_boundary_max(self):
        result = calculate_gaokao_score(
            {'语文': 150, '数学': 150, '外语': 150},
            ['E', 'E', 'E']
        )
        assert result['main_total'] == 450

    def test_wrong_number_of_electives(self):
        with pytest.raises(ValueError, match='数量应为3'):
            calculate_gaokao_score(
                {'语文': 100, '数学': 100, '外语': 100},
                ['A+', 'A']
            )

    def test_invalid_grade(self):
        with pytest.raises(ValueError, match='无法识别的输入'):
            calculate_gaokao_score(
                {'语文': 100, '数学': 100, '外语': 100},
                ['X', 'A', 'A']
            )

    def test_invalid_score(self):
        with pytest.raises(ValueError, match='不是合规的'):
            calculate_gaokao_score(
                {'语文': 100, '数学': 100, '外语': 100},
                ['80', 'A', 'A']
            )

    def test_float_main_scores(self):
        result = calculate_gaokao_score(
            {'语文': 100.5, '数学': 110.5, '外语': 120.5},
            ['A+', 'A', 'A']
        )
        assert result['main_total'] == 331.5

    def test_float_score_input_for_elective(self):
        result = calculate_gaokao_score(
            {'语文': 100, '数学': 100, '外语': 100},
            ['67.0', 'A', 'A']
        )
        assert result['elective_details'][0]['score'] == 67
