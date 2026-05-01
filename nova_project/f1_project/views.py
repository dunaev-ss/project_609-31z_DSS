from datetime import date

from django.shortcuts import render
from django.db.models import Q

from . models import GrandPrix, Standing, Transfer


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
            'gp_country_flag': gp.country.flag.url if gp.country and gp.country.flag else None,
            'winner': winner_standing.driver if winner_standing else "-",
            'winner_flag': winner_standing.driver.country.flag.url if winner_standing and winner_standing.driver.country and winner_standing.driver.country.flag else None,
            'pole': pp_standing.driver if pp_standing else "-",
            'pole_flag': pp_standing.driver.country.flag.url if pp_standing and pp_standing.driver.country and pp_standing.driver.country.flag else None,
            'faster_lap': fl_standing.driver if fl_standing else "-",
            'fl_flag': fl_standing.driver.country.flag.url if fl_standing and fl_standing.driver.country and fl_standing.driver.country.flag else None,
            'team': winner_team,
        })

    return render(request, 'f1_project/result.html', {'result': results_list, 'season_year': season_year})