from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import FeedbackForm

def feedback(request):
    feedback_type = request.GET.get('type')
    if feedback_type:
        if request.method == 'POST':
            form = FeedbackForm(request.POST)
            if form.is_valid():
                feedback = form.save(commit=False)
                feedback.user = request.user
                feedback.feedback_type = feedback_type
                feedback.save()
                messages.success(request, f'Thanks {request.user.username} for filling the form')
                return redirect('feedback')
        else:
            form = FeedbackForm()

        return render(request, 'feedback/feedback_form.html', {'form': form, 'feedback_type': feedback_type})
    else:
        return render(request, 'feedback/feedback_type.html')

def feedback_thank_you_view(request):
    return render(request, 'feedback/thank_you.html')
