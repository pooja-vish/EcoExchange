from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import FeedbackForm
from django.contrib.auth.decorators import login_required

@login_required
def submit_feedback(request):
    form = FeedbackForm()
    success = False

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.feedback_type = request.POST.get('feedback_type','feedback')  # Default to 'feedback' if not provided
            feedback.save()
            success = True  # Set success flag to True

    return render(request, 'feedback/submit_feedback.html', {'form': form, 'success': success})
