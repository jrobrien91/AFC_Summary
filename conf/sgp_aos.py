# dsname: Datastream name to pull data from
# dsname2: Secondary datastream(s) to include and merge
# t_delta: Script will resample data to 1 min.  If gaps are longer set this appropriately
# workers: Set to 1 in the case of radar data so it doesn't crash the system
conf = {
    'site': 'sgp',
    'facility': 'E13',
    'start_date': '2016-11-01',
    'end_date': '2022-03-01',
    'outname': '/home/theisen/www/afc_summary/sgp_aos.pdf', #options are png, pdf, etc
    'chart_style': 'linear',
    'info_style': 'simple',
    'data_path': '/data/archive',
    'dqr_table': True,
    'doi_table': True, #this will remove the DOI from besides the plots
    'instruments':{
        'acsm': {'dsname': 'aosacsmE13.b1', 't_delta': 30},
        'aps': {'dsname': 'aosapsE13.b1'},
        'aosmet': {'dsname': 'aosmetE13.a1'},
        'caps-pmex': {'dsname': 'aoscaps3wE13.b1'},
        'ccn': {'dsname': 'aosccn2colaE13.b1'},
        'cpc': {'dsname': 'aoscpcf1mE13.b1'},
        'cpcuf': {'dsname': 'aoscpcufE13.b1'},
        'htdma': {'dsname': 'aoshtdmaE13.a1', 't_delta': 60},
        'nanosmps': {'dsname': 'aosnanosmpsE13.b1', 't_delta': 30},
        'nephelometer': {'dsname': 'aosnephdry1mE13.b1'},
        'nephelometer': {'dsname': 'aosnephwet1mE13.b1'},
        'ozone': {'dsname': 'aoso3E13.b1'},
        'psap': {'dsname': 'aospsap3w1mE13.b1'},
        'smps': {'dsname': 'aossmpsE13.b1', 't_delta': 30},
        'so2': {'dsname': 'aosso2E13.b1'},
        'uhsas': {'dsname': 'aosuhsasE13.b1'},
    }
}
