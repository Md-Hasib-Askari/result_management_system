def get_grade(marks, assessment=False):
    for mark in marks:
        cq = mark['cq']
        mcq = mark['mcq']
        total = mark['obtained_mark']
        for total_mark in [50, 100, 200]:
            if mark['total_marks'] == total_mark:
                if mcq < 16 and not assessment and total_mark == 50:
                    mark['grade'] = 'F'
                    mark['gpa'] = 0
                    continue
                if (cq < 23 or mcq < 10) and not assessment and total_mark == 100:
                    mark['grade'] = 'F'
                    mark['gpa'] = 0
                    continue
                if (cq < 46 or mcq < 20) and not assessment and total_mark == 200:
                    mark['grade'] = 'F'
                    mark['gpa'] = 0
                    continue

                if total >= total_mark * 0.8:
                    mark['grade'] = 'A+'
                    mark['gpa'] = 5
                elif total >= total_mark * 0.7:
                    mark['grade'] = 'A'
                    mark['gpa'] = 4
                elif total >= total_mark * 0.6:
                    mark['grade'] = 'A-'
                    mark['gpa'] = 3.5
                elif total >= total_mark * 0.5:
                    mark['grade'] = 'B'
                    mark['gpa'] = 3
                elif total >= total_mark * 0.33:
                    mark['grade'] = 'C'
                    mark['gpa'] = 2
                else:
                    mark['grade'] = 'F'
                    mark['gpa'] = 0
    return marks


def calculate_gpa(marks):
    gpa_sum = 0
    optional_gpa = 0
    total_gpa = 45
    count = 0
    for mark in marks:
        if mark['subject'].optional:
            optional_gpa += mark['gpa']
            continue
        gpa_sum += mark['gpa']
        count += 1

    if optional_gpa == 5:
        gpa_sum += 3
    elif optional_gpa == 4:
        gpa_sum += 2
    elif optional_gpa == 3.5:
        gpa_sum += 1.5
    elif optional_gpa == 3:
        gpa_sum += 1
    
    if gpa_sum > total_gpa:
        gpa_sum = total_gpa
    
    if count == 0:
        return 0
    return round(gpa_sum / count, 2)