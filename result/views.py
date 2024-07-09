from django.shortcuts import get_object_or_404, redirect, render

from information.models import Student, Section, Subject
from result.models import Result
from result.utilities import calculate_gpa, get_grade

# Create your views here.
def add_result(request):
    if request.user.is_authenticated:
        context = {}
        message = None
        if request.POST:
            post = dict(request.POST)
            student_id = post['student'][0]
            student = Student.objects.filter(id=student_id).first()
            exam_type = post['exam_type'][0]
            subject_id = post['subject']
            cq = [x if x != '' else 0 for x in post['cq']]
            mcq = [x if x != '' else 0 for x in post['mcq']]
            project = [x if x != '' else 0 for x in post['project']]
            practical = [x if x != '' else 0 for x in post['practical']]
            if student_id and exam_type and subject_id and (cq or mcq or practical or project):
                for idx in range(len(subject_id)):
                    subject = Subject.objects.filter(id=int(subject_id[idx])).first()
                    result = Result.objects.filter(
                        student=student, 
                        exam_type=exam_type, 
                        subject=subject
                    ).first()
                    if result:
                        result.cq = cq[idx]
                        result.mcq = mcq[idx]
                        result.practical = practical[idx]
                        result.project = project[idx]
                        try:
                            result.save()
                        except Exception as e:
                            print(e)
                            message = {
                                'error': 'Error updating marks. Please try again.'
                            }
                            break
                        message = {
                            'success': 'Marks updated successfully!'
                        }
                    else:
                        result = Result(
                            exam_type=exam_type,
                            student=student,
                            subject=subject,
                            cq=cq[idx],
                            mcq=mcq[idx],
                            practical=practical[idx],
                            project=project[idx]
                        )
                        try:
                            result.save()
                        except Exception as e:
                            message = {
                                'error': 'Error adding marks. Please try again.'
                            }
                            break
                        message = {
                            'success': 'Marks added successfully!'
                        }

        student = None
        subjects = None
        if request.GET:
            roll = request.GET.get('roll')
            section = request.GET.get('section')
            student = Student.objects.filter(
                roll=roll, 
                section=Section.objects.get(name=section)
            ).first()
            if student:
                subjects = student.student_class.subject_set.filter(group__in=[student.group, 'Common'])
                if section.lower() == 'b':
                    subjects = subjects.exclude(name__icontains='agricultural')
                elif section.lower() == 'a':
                    subjects = subjects.exclude(name__icontains='home science')
                results = Result.objects.filter(student=student, exam_type='Pretest', subject__in=subjects)
                subject_wise_result = {}
                for subject in subjects:
                    for result in results:
                        if result.subject == subject:
                            subject_wise_result[subject.name] = {
                                'subject': subject,
                                'result': result,
                            }
                if subject_wise_result:
                    context = {
                        'subject_wise_result': subject_wise_result
                    }
                else:
                    context = {
                        'subject_wise_result': {
                            subject.name: {
                                'subject': subject,
                                'result': None
                            } for subject in subjects
                        }
                    }
            else:
                message = {
                    'error': 'No student found matching the search criteria.'
                }
        print(context)
        context = {
            **context,
            'subjects': subjects,
            'student': student,
            'message': message
        }
        return render(request, 'result/add_result.html', context)
    else:
        return redirect('admin:login')
    
def view_results(request):
    if request.user.is_authenticated:
        context = {}
        if request.GET.get('section') and request.GET.get('exam_type'):
            students = Student.objects.filter(
                section=Section.objects.get(name=request.GET.get('section')))
            results = Result.objects.filter(student__in=students, exam_type=request.GET.get('exam_type'))
            print(results.count())
            if results.count() == 0:
                context = {
                    'message': {
                        'error': 'No results found for the selected section.'
                    }
                }
            subjects = Subject.objects.all()
            context = {
                **context,
                'results': results,
                'students': students,
                'subjects': subjects
            }
        return render(request, 'result/view_results.html', context)
    return redirect('admin:login')

def student_marksheet_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    results = Result.objects.filter(student=student)
    subjects = student.student_class.subject_set.all()
    marks = []
    assessment_mark = []
    assessment_sub = ['physical', 'career']
    for result in results:
        for subject in subjects:
            if result.subject == subject:
                total_marks = subject.total_marks
        if result.subject.name.lower().split(' ')[0] in assessment_sub:
            assessment_mark.append({
                'subject': result.subject,
                'cq': result.cq,
                'mcq': result.mcq,
                'practical': result.practical,
                'project': result.project,
                'obtained_mark': result.cq + result.mcq + result.practical + result.project,
                'total_marks': total_marks
            })
        else:
            marks.append({
                'subject': result.subject,
                'cq': result.cq,
                'mcq': result.mcq,
                'practical': result.practical,
                'project': result.project,
                'obtained_mark': result.cq + result.mcq + result.practical + result.project,
                'total_marks': total_marks
            })
    marks = get_grade(marks)
    assessment_mark = get_grade(assessment_mark, True)
    final_gpa = calculate_gpa(marks)
    context = {
        'student': student, 
        'marks': marks, 
        'assessment_mark': assessment_mark,
        'final_gpa': final_gpa
    }
    return render(request, 'result/student_marksheet.html', context)


def generate_reports(request, section):
    students = Student.objects.all()
    if section:
        report = []
        students = Student.objects.filter(section=Section.objects.filter(name=section.upper()).first())
        for student in students:
            results = Result.objects.filter(student=student)
            subjects = student.student_class.subject_set.all()
            marks = []
            assessment_mark = []
            assessment_sub = ['physical', 'career']
            for result in results:
                for subject in subjects:
                    if result.subject == subject:
                        total_marks = subject.total_marks
                if result.subject.name.lower().split(' ')[0] in assessment_sub:
                    assessment_mark.append({
                        'subject': result.subject,
                        'cq': result.cq,
                        'mcq': result.mcq,
                        'practical': result.practical,
                        'project': result.project,
                        'obtained_mark': result.cq + result.mcq + result.practical + result.project,
                        'total_marks': total_marks
                    })
                else:
                    marks.append({
                        'subject': result.subject,
                        'cq': result.cq,
                        'mcq': result.mcq,
                        'practical': result.practical,
                        'project': result.project,
                        'obtained_mark': result.cq + result.mcq + result.practical + result.project,
                        'total_marks': total_marks
                    })
            marks = get_grade(marks)
            assessment_mark = get_grade(assessment_mark, True)
            final_gpa = calculate_gpa(marks)

            report.append({
                'student': student, 
                'marks': marks, 
                'assessment_mark': assessment_mark,
                'final_gpa': final_gpa
            })

        print(report)
        return render(request, 'result/marksheets.html', context={'reports': report})
    return redirect('admin:login')