from datetime import date

from django.shortcuts import render
from django.db.models import F, Q, Sum

from . models import Driver, GrandPrix, Standing, Team, Transfer


def season_results(request):
    current_year = date.today().year
    season_year = int(request.GET.get('season_year', current_year))

    season_start = date(season_year, 1, 1)
    season_end = date(season_year, 12, 31)

    gps = GrandPrix.objects.filter(
        standing__event_date__range=(season_start, season_end)
    ).distinct().order_by('standing__event_date')

    results_list = []

    for gp in gps:
        transfer = None
        winner_standing = Standing.objects.filter(
            grand_prix=gp,
            pos='1',
            event_date__range=(season_start, season_end)
        ).first()
        pp_standing = Standing.objects.filter(
            grand_prix=gp,
            pp=True,
            event_date__range=(season_start, season_end)
            ).first()
        fl_standing = Standing.objects.filter(
            grand_prix=gp,
            fl=True,
            event_date__range=(season_start, season_end)
        ).first()
        
        winner_team = "-"
        if winner_standing:
            current_date = winner_standing.event_date
            transfer = Transfer.objects.filter(
                driver=winner_standing.driver,
                start_date__lte=current_date
            ).filter(
                Q(end_date__gte=current_date) | Q(end_date__isnull=True)
            ).first()
        
        if transfer:
            winner_team = transfer.team.team
    
        results_list.append({
            'round': len(results_list) + 1,
            'date': winner_standing.event_date if winner_standing else None,
            'gp_name': gp.grand_prix,
            'gp_abbr': gp.gp_abbr,
            'gp_country_flag': gp.country.flag.url if gp.country and gp.country.flag else None,
            'winner': winner_standing.driver if winner_standing else "-",
            'winner_abbr': winner_standing.driver.driver_abbr if winner_standing else "-",
            'winner_flag': winner_standing.driver.country.flag.url if winner_standing and winner_standing.driver.country and winner_standing.driver.country.flag else None,
            'pole': pp_standing.driver if pp_standing else "-",
            'pole_abbr': pp_standing.driver.driver_abbr if pp_standing else "-",
            'pole_flag': pp_standing.driver.country.flag.url if pp_standing and pp_standing.driver.country and pp_standing.driver.country.flag else None,
            'faster_lap': fl_standing.driver if fl_standing else "-",
            'fl_abbr': fl_standing.driver.driver_abbr if fl_standing else "-",
            'fl_flag': fl_standing.driver.country.flag.url if fl_standing and fl_standing.driver.country and fl_standing.driver.country.flag else None,
            'team': winner_team,
            'team_abbr': transfer.team.team_abbr if transfer else "-",
            'team_flag': transfer.team.country.flag.url if transfer and transfer.team.country.flag else None,
        })

    return render(request, 'f1_project/result.html', {'result': results_list, 'season_year': season_year})


def season_standings(request):
    season_year = int(request.GET.get('season_year', date.today().year))
    standings_type = request.GET.get('type', 'drivers')
    
    season_start = date(season_year, 1, 1)
    season_end = date(season_year, 12, 31)

    gps = GrandPrix.objects.filter(
        standing__event_date__range=(season_start, season_end)
    ).distinct().order_by('standing__event_date')

    standings_data = []

    if standings_type == 'drivers':
        driver_standings = Driver.objects.filter(
            standing__event_date__range=(season_start, season_end)
        ).annotate(
            total_pts=Sum('standing__pts', filter=Q(standing__event_date__range=(season_start, season_end)))
        ).order_by('-total_pts')

        for driver in driver_standings:
            results = []
            driver_teams = set()
            for gp in gps:
                res = Standing.objects.filter(driver=driver, grand_prix=gp, event_date__range=(season_start, season_end)).first()
                if res:
                    transfer = Transfer.objects.filter(
                        driver=driver, start_date__lte=res.event_date
                    ).filter(Q(end_date__gte=res.event_date) | Q(end_date__isnull=True)).first()
                    if transfer:
                        driver_teams.add(transfer.team.team)
                results.append({
                    'pts': res.pts if res else None,
                    'pp': res.pp if res else False,
                    'fl': res.fl if res else False,
                })
            standings_data.append({
                'name': driver.driver,
                'subtext': ", ".join(sorted(driver_teams)),
                'flag': driver.country.flag.url if driver.country.flag else None,
                'results': results,
                'total_pts': driver.total_pts
            })

    else:
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

        for team in team_standings:
            results = []
            for gp in gps:
                gp_data = Standing.objects.filter(grand_prix=gp, event_date__range=(season_start, season_end)).first()
                pts_sum = None
                if gp_data:
                    pts_sum = Standing.objects.filter(
                        grand_prix=gp, event_date=gp_data.event_date,
                        driver__transfer__team=team,
                        driver__transfer__start_date__lte=gp_data.event_date
                    ).filter(
                        Q(driver__transfer__end_date__gte=gp_data.event_date) | Q(driver__transfer__end_date__isnull=True)
                    ).aggregate(total=Sum('pts'))['total']
                results.append({'pts': pts_sum})

            standings_data.append({
                'name': team.team,
                'subtext': None,
                'flag': team.country.flag.url if team.country.flag else None,
                'results': results,
                'total_pts': team.total_pts
            })

    return render(request, 'f1_project/standings.html', {
        'gps': gps,
        'standings': standings_data,
        'season_year': season_year,
        'type': standings_type
    })


def calendar_view(request):
    return render(request, 'f1_project/stub.html', {'title': 'Календарь'})


def teams_list(request):
    return render(request, 'f1_project/stub.html', {'title': 'Команды'})


def drivers_list(request):
    return render(request, 'f1_project/stub.html', {'title': 'Пилоты'})


def data_analysis(request):
    return render(request, 'f1_project/stub.html', {'title': 'Анализ данных'})
