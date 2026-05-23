from datetime import date
from django.shortcuts import render
from django.db.models import F, Q, Sum
from django.db.models.functions import ExtractYear
from f1_project.models import Driver, Team, Standing

def data_analysis(request):
    # 1. Получаем из базы данных список всех уникальных годов, где есть гонки
    db_years = (
        Standing.objects.annotate(year=ExtractYear('event_date'))
        .values_list('year', flat=True)
        .distinct()
        .order_by('-year')
    )
    # Превращаем QuerySet в обычный список питоновских чисел
    years_range = list(db_years)

    # Задаем дефолтный год: самый свежий из базы, либо текущий, если база пуста
    current_year = date.today().year
    default_year = years_range[0] if years_range else current_year

    # Получаем параметры из GET-запроса
    season_year = int(request.GET.get('season_year', default_year))
    standings_type = request.GET.get('type', 'drivers')
    
    season_start = date(season_year, 1, 1)
    season_end = date(season_year, 12, 31)

    labels = []
    values = []

    if standings_type == 'drivers':
        # Личный зачет пилотов
        driver_standings = Driver.objects.filter(
            standing__event_date__range=(season_start, season_end)
        ).annotate(
            total_pts=Sum('standing__pts', filter=Q(standing__event_date__range=(season_start, season_end)))
        ).order_by('-total_pts')

        labels = [driver.driver for driver in driver_standings]
        values = [driver.total_pts or 0 for driver in driver_standings]
        title_text = "Личный зачет"
    else:
        # Кубок конструкторов
        team_standings = Team.objects.filter(
            transfer__driver__standing__event_date__range=(season_start, season_end)
        ).annotate(
            total_pts=Sum(
                'transfer__driver__standing__pts',
                filter=(
                    Q(transfer__driver__standing__event_date__range=(season_start, season_end)) &
                    Q(transfer__start_date__lte=F('transfer__driver__standing__event_date')) &
                    (Q(transfer__end_date__gte=F('transfer__driver__standing__event_date')) | Q(transfer__end_date__isnull=True))
                )
            )
        ).distinct().order_by('-total_pts')

        labels = [team.team for team in team_standings]
        values = [team.total_pts or 0 for team in team_standings]
        title_text = "Кубок конструкторов"

    context = {
        'title': title_text,
        'chart_labels': labels,
        'chart_data': values,
        'season_year': season_year,
        'standings_type': standings_type,
        'years_range': years_range,
    }
    return render(request, 'charts/data_analysis.html', context)
