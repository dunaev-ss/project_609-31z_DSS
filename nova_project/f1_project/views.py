from django.shortcuts import render
from django.db.models import Q

from . models import GrandPrix, Standing, Transfer


def season_results(request):
    gps = GrandPrix.objects.all().order_by('id')
    results_list = []

    for gp in gps:
        winner_standing = Standing.objects.filter(grand_prix=gp, pos='1').first()
        pp_standing = Standing.objects.filter(grand_prix=gp, pp=True).first()
        fl_standing = Standing.objects.filter(grand_prix=gp, fl=True).first()
        
        winner_team = "-"
        if winner_standing:
            event_date = winner_standing.event_date
            transfer = Transfer.objects.filter(
                driver=winner_standing.driver,
                start_date__lte=event_date
            ).filter(
                Q(end_date__gte=event_date) | Q(end_date__isnull=True)
            ).first()
        
        if transfer:
            winner_team = transfer.team.team
    
        results_list.append({
            'round': gp.id,
            'date': winner_standing.event_date if winner_standing else None,
            'gp_name': gp.grand_prix,
            'gp_country_flag': gp.country.flag.url if gp.country.flag else None,
            'winner': winner_standing.driver if winner_standing else "-",
            'winner_flag': winner_standing.driver.country.flag.url if winner_standing else None,
            'pole': pp_standing.driver if pp_standing else "-",
            'pole_flag': pp_standing.driver.country.flag.url if pp_standing else None,
            'faster_lap': fl_standing.driver if fl_standing else "-",
            'fl_flag': fl_standing.driver.country.flag.url if fl_standing else None,
            'team': winner_team,
            'team_flag': transfer.team.country.flag.url if transfer else None
        })

    return render(request, 'f1_project/result.html', {'result': results_list})