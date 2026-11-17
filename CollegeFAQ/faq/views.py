from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import FAQ
from .forms import FAQForm


def home(request):
    """Home page: search, category filter, FAQ list with answer modal."""
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', 'All FAQs')

    faqs = FAQ.objects.all()
    if category in ('VisitorFAQ', 'StudentFAQ'):
        faqs = faqs.filter(category=category)
    if query:
        faqs = faqs.filter(
            Q(question__icontains=query) | Q(answer__icontains=query)
        )

    context = {
        'faqs': faqs,
        'query': query,
        'selected_category': category,
        'categories': ['All FAQs', 'VisitorFAQ', 'StudentFAQ'],
    }
    return render(request, 'faq/home.html', context)


def manage_faqs(request):
    """Manage FAQs: add new FAQ form + delete existing ones."""
    if request.method == 'POST':
        if 'add_faq' in request.POST:
            form = FAQForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'FAQ added successfully!')
                return redirect('manage_faqs')
            else:
                messages.error(request, 'Please fill in all required fields.')
        elif 'delete_faq' in request.POST:
            faq_id = request.POST.get('faq_id')
            faq = get_object_or_404(FAQ, id=faq_id)
            faq.delete()
            messages.success(request, 'FAQ deleted successfully!')
            return redirect('manage_faqs')
    else:
        form = FAQForm()

    faqs = FAQ.objects.all()
    context = {'form': form, 'faqs': faqs}
    return render(request, 'faq/manage.html', context)


def chatbot(request):
    """Chatbot page: keyword-based FAQ search."""
    answer = None
    matched_question = None
    user_question = ''

    if request.method == 'POST':
        user_question = request.POST.get('question', '').strip()
        if user_question:
            keywords = user_question.lower().split()
            # Build OR query across question and answer fields
            q_objects = Q()
            for kw in keywords:
                q_objects |= Q(question__icontains=kw) | Q(answer__icontains=kw) | Q(category__icontains=kw)
            match = FAQ.objects.filter(q_objects).first()
            if match:
                answer = match.answer
                matched_question = match.question
            # else: answer stays None -> "answer unavailable"

    context = {
        'user_question': user_question,
        'answer': answer,
        'matched_question': matched_question,
    }
    return render(request, 'faq/chatbot.html', context)
