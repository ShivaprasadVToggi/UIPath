from django.db import models


class FAQ(models.Model):
    CATEGORY_CHOICES = [
        ('VisitorFAQ', 'VisitorFAQ'),
        ('StudentFAQ', 'StudentFAQ'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='VisitorFAQ')
    question = models.CharField(max_length=300)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category', 'id']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return f"[{self.category}] {self.question[:60]}"
