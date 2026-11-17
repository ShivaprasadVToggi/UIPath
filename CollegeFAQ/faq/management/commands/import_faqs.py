"""
Import / sync FAQs from CollegeFAQ.xlsx or faq_data.csv into the database.

Usage:
    python manage.py import_faqs --excel ../data/CollegeFAQ.xlsx
    python manage.py import_faqs --csv ../data/faq_data.csv
    python manage.py import_faqs --excel ../data/CollegeFAQ.xlsx --sync   # clears existing first
"""
import csv
import os

from django.core.management.base import BaseCommand, CommandError
from faq.models import FAQ


class Command(BaseCommand):
    help = 'Import or sync FAQs from an Excel (.xlsx) or CSV file.'

    def add_arguments(self, parser):
        parser.add_argument('--excel', type=str, help='Path to CollegeFAQ.xlsx')
        parser.add_argument('--csv', type=str, help='Path to faq_data.csv')
        parser.add_argument('--sync', action='store_true',
                            help='Delete all existing FAQs before importing')

    def handle(self, *args, **options):
        excel_path = options.get('excel')
        csv_path = options.get('csv')

        if not excel_path and not csv_path:
            # Try default locations relative to project root
            base = os.path.dirname(os.path.dirname(os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
            candidates = [
                os.path.join(base, '..', 'data', 'CollegeFAQ.xlsx'),
                os.path.join(base, '..', 'CollegeFAQAutomation', 'CollegeFAQ.xlsx'),
                os.path.join(base, 'CollegeFAQ.xlsx'),
            ]
            for c in candidates:
                if os.path.exists(c):
                    excel_path = c
                    self.stdout.write(self.style.NOTICE(f"Using default file: {c}"))
                    break
            if not excel_path:
                raise CommandError('Please provide --excel or --csv path.')

        if options['sync']:
            FAQ.objects.all().delete()
            self.stdout.write(self.style.WARNING('Cleared all existing FAQs (--sync).'))

        rows = []
        if excel_path:
            rows = self._read_excel(excel_path)
        elif csv_path:
            rows = self._read_csv(csv_path)

        created = 0
        skipped = 0
        for row in rows:
            category = (row.get('Category') or '').strip()
            question = (row.get('Question') or '').strip()
            answer = (row.get('Answer') or '').strip()
            if not question or not answer:
                skipped += 1
                continue
            if category not in ('VisitorFAQ', 'StudentFAQ'):
                category = 'VisitorFAQ'
            # Avoid duplicates by question text
            obj, was_created = FAQ.objects.get_or_create(
                question=question,
                defaults={'category': category, 'answer': answer},
            )
            if was_created:
                created += 1
            else:
                # Update answer/category if syncing
                obj.category = category
                obj.answer = answer
                obj.save()
                skipped += 1

        self.stdout.write(self.style.SUCCESS(
            f"Import complete. Created: {created}, Updated/Skipped: {skipped}"))

    @staticmethod
    def _read_excel(path):
        try:
            from openpyxl import load_workbook
        except ImportError:
            raise CommandError('openpyxl is required. Install with: pip install openpyxl')
        if not os.path.exists(path):
            raise CommandError(f'File not found: {path}')
        wb = load_workbook(path, read_only=True, data_only=True)
        ws = wb['Sheet1'] if 'Sheet1' in wb.sheetnames else wb.active
        rows = list(ws.iter_rows(values_only=True))
        if not rows:
            return []
        headers = [str(h).strip() if h else '' for h in rows[0]]
        result = []
        for r in rows[1:]:
            if not any(r):
                continue
            result.append({headers[i]: (str(r[i]) if r[i] is not None else '')
                           for i in range(len(headers))})
        wb.close()
        return result

    @staticmethod
    def _read_csv(path):
        if not os.path.exists(path):
            raise CommandError(f'File not found: {path}')
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return [dict(row) for row in reader]
