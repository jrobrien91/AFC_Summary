import act
import requests
import json 
import glob
import pandas as pd
import datetime as dt
import numpy as np
import xarray as xr
import dask
import matplotlib.pyplot as plt
import textwrap
import argparse
import importlib
from scipy import stats
from matplotlib.dates import DateFormatter
from matplotlib.dates import HourLocator
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import ListedColormap
from matplotlib import cm


def get_dqr(ds):
    """
    Queries DQR webservice for the datastream name passed in

    Parameters
    ----------
    ds : str
        ARM datastream name (ie, sgpmetE13.b1).

    """
    # Build URL and call through requests
    url = ''.join(("https://www.archive.arm.gov/dqrws/ARMDQR?datastream=", ds,
                   "&dqrfields=dqrid,starttime,endtime,metric,subject&timeformat=YYYYMMDD.hhmmss",
                   "&searchmetric=incorrect,suspect"))
    r = requests.get(url=url)

    # Run through the returns and compile data
    num = []
    sdate = []
    edate = []
    code = []
    sub = []
    for line in r.iter_lines():
        # filter out keep-alive new lines
        if line:
            decoded_line = line.decode('utf-8')
            result = decoded_line.split('|')
            num.append(result[0])
            sdate.append(result[1])
            edate.append(result[2])
            code.append(result[3])
            sub.append(result[4])

    return {'dqr_num': num, 'sdate': sdate, 'edate': edate, 'code': code, 'subject': sub}


def get_doi(site, dsname, c_start, c_end):
    # Get DOI Information from ARM's API
    doi_url = 'https://adc.arm.gov/citationservice/citation/inst-class?id=' + inst[ii] + '&citationType=apa'
    doi_url += '&site=' + site
    doi_url += '&dataLevel=' + dsname.split('.')[-1]
    doi_url += '&startDate=' + c_start
    doi_url += '&endDate=' + c_end
    doi = requests.get(url=doi_url).json()['citation']

    return doi


def get_metadata(ds, return_fac=False):
    # Get Metadata Information, particularly the description
    metadata_url = 'https://adc.arm.gov/solr8/metadata/select?q=datastream%3A' + ds
    r = requests.get(url=metadata_url)
    response = r.json()['response']
    response = response['docs'][0]
    description = response['instrument_name_text']
    if return_fac:
        description = response['facility_name']

    return description


def get_da(site, dsname, dsname2, t_delta, d, dqr):
    """
    Function to calculate data availability for a particular instrument

    Parameters
    ----------
    site : str
        ARM Site ID
    dsname : str
        Datastream name to use, minus site
    dsname2 : str
        Secondary datastream name to use, minus site
        For instance if dsname = dlfptM1.b1, dsname2 = dlppiM1.b1
    t_delta : float
        Pre-defined time delta to use, otherwise resample to 1 minute
    d : str
        Date to process DA for
    dqr : dict
        Dictionary from get_dqr.  This allows for DQRing of data without
        multiple pings of the DQR web service at once

    Returns
    -------
    dict
        returns a dictionary of data and time deltas to use for plotting

    """

    # Get files for particular day, defaults to archive area for now
    ds = site + dsname
    files = glob.glob('/data/archive/' + site + '/' + ds + '/' + ds + '*' + d + '*nc')
    if len(files) == 0:
        files = glob.glob('/data/archive/' + site + '/' + ds + '/' + ds + '*' + d + '*cdf')
    files = sorted(files)

    # Set time delta to 1 minute if not specified
    if t_delta is None:
        t_delta = 1

    # Read data for primary datastream
    if len(files) > 0:
        try:
            obj = act.io.armfiles.read_netcdf(files)
        except ValueError: 
            obj = act.io.armfiles.read_netcdf(files[0])
        obj = obj.sortby('time')
    else:
        obj = None

    # Read data for secondary datastream
    if dsname2 is not None:
        ds2 = site + dsname2
        files2 = glob.glob('/data/archive/' + site + '/' + ds2 + '/' + ds2 + '*' + d + '*nc')
        if len(files2) == 0:
            files2 = glob.glob('/data/archive/' + site + '/' + ds2 + '/' + ds2 + '*' + d + '*cdf')
        files2 = sorted(files2)
        if len(files2) > 0:
            obj2 = act.io.armfiles.read_netcdf(files2, combine='nested', coords=['time'])
            obj2 = obj2.sortby('time')
            if obj is not None:
                obj = obj['time'].combine_first(obj2['time'])
                obj2.close()
            else:
                obj = obj2
    else:
        dsname2 = None

    # Set up dataframe with all expected times for day
    d0 = pd.to_datetime(d)
    d1 = d0 + dt.timedelta(days=1)
    d_range = pd.date_range(d0, d1, freq=str(t_delta) + 'T', closed='left')
    df1 = pd.DataFrame({'counts': np.zeros(len(d_range))}, index=d_range)

    # Join datasets with dataframe
    code_map = {'suspect':  2, 'incorrect': 3}
    if len(files) > 0:
        counts = obj['time'].resample(time=str(t_delta) + 'min').count().to_dataframe()
        counts[counts > 1] = 1
        dqr_counts = counts * 0.
        # Flag data for  DQRs
        # Work on passing DQR times to get_da to flag
        for jj, d in enumerate(dqr['dqr_num']):
            dqr_start = dt.datetime.strptime(dqr['sdate'][jj], '%Y%m%d.%H%M%S')
            dqr_end = dt.datetime.strptime(dqr['edate'][jj], '%Y%m%d.%H%M%S')
            idx = (counts.index > dqr_start) & (counts.index < dqr_end)
            idx = np.where(idx)[0]
            assessment = dqr['code'][jj]
            if len(idx) > 0:
                dqr_counts.iloc[idx]  = code_map[assessment]

        data = df1.join(counts)
        data.loc[data['time'] > 0, 'time'] = 1
        r_data = np.nan_to_num(data['time'].tolist())

        dqr_data = df1.join(dqr_counts)
        dqr_data.loc[dqr_data['time'] == 0, 'time'] = np.nan
        dqr_data = dqr_data['time'].tolist()
        obj.close()
    else:
        data = df1
        r_data = np.nan_to_num(data['counts'].tolist())
        dqr_data = r_data * 0.

    return {'data': r_data, 't_delta': t_delta, 'date': d0, 'dqr_data': dqr_data}


if __name__ == '__main__':
    """
    Main function to get information from configuration file and create DA plots

    Author : Adam Theisen
    """

    # Time trials
    now = pd.Timestamp.now()

    # Get configuration file passed in from command line
    parser = argparse.ArgumentParser(description='Create campaign summary plots.')
    parser.add_argument('-c', '--conf', type=str, required=True,
                       help='Conf file to get information from')
    args = parser.parse_args()

    # Executes the config file so that the variables are accessible to this program
    exec(open(args.conf).read())

    # Get configuration information
    site = conf['site']
    inst = list(conf['instruments'].keys())
    c_start = conf['start_date']
    c_end = conf['end_date']

    # Set date range for plots
    start = pd.to_datetime(c_start)
    end = pd.to_datetime(c_end)
    c_dates = pd.date_range(start, end + dt.timedelta(days=1), freq='d')
    #c_dates = c_dates[0:5]

    # Set up plot layout.  Since it's a PDF, it's  8 plots per page
    nrows = 8
    ncols = 3
    ct = 0

    # Create pdf file
    if 'outname' in conf:
        filename = conf['outname']
    pdf_pages = PdfPages(filename)

    # Process each instrument
    for ii in range(len(inst)):
        if ct ==  0:
            fig = plt.figure(figsize=(8.27, 11.69), constrained_layout=True, dpi=100)
            gs = fig.add_gridspec(nrows, ncols)

        dsname = conf['instruments'][inst[ii]]['dsname']
        ds = conf['site'] + dsname
        print(ds)

        dqr = get_dqr(ds)
        dsname2 = None
        ds2 = None
        # Get secondary datastream if specified
        if 'dsname2' in conf['instruments'][inst[ii]]:
            dsname2 = conf['instruments'][inst[ii]]['dsname2']
            ds2 = site + dsname2

        # Get time delta if specified
        t_delta = None
        if 't_delta' in conf['instruments'][inst[ii]]:
            t_delta = conf['instruments'][inst[ii]]['t_delta']

        # Get number of workers if defined.  Should be 1 worker for radars to
        # avoid core dumps
        workers = None
        if 'workers' in conf['instruments'][inst[ii]]:
            workers = conf['instruments'][inst[ii]]['workers']

        # Set up the initial title of the doc
        if ii == 0:
            ax0 = fig.add_subplot(gs[ct, :])
            ax0.set_frame_on(False)
            ax0.get_xaxis().set_visible(False)
            ax0.get_yaxis().set_visible(False)
            description = get_metadata(ds, return_fac=True)
            ax0.text(0.5, 0.7, '\n'.join(textwrap.wrap(description, width=50)), size=16,  ha='center')
            ax0.text(0.5, 0.4, 'Atmospheric Radiation Measurement User Facility', size=14,
                     ha='center')
            ct += 1

        # Dask loop for multiprocessing
        # workers should be set to 1 in the conf file for radars 
        task = []
        c_dates = c_dates
        for jj, d in enumerate(c_dates):
            #task.append(get_da(site, dsname, dsname2, t_delta, d.strftime('%Y%m%d'), dqr))
            task.append(dask.delayed(get_da)(site, dsname, dsname2, t_delta, d.strftime('%Y%m%d'), dqr))
        results = dask.compute(*task, num_workers=workers)

        # Get data from dask and create images for display
        t_delta = int(stats.mode([r['t_delta'] for r in results])[0][0])
        y_times = pd.date_range(start, start + dt.timedelta(days=1), freq=str(t_delta) + 'T', closed='left')
        y_times_time = np.array([ti.time() for ti in y_times])
        img = [list(r['data']) for r in results]
        dqr_img = [list(r['dqr_data']) for r in results]

        # Get DOI Information
        doi = get_doi(site, dsname, c_start, c_end)
        description = get_metadata(ds)

        # Add Subplot and start adding text
        # Just text on this plot
        ax0 = fig.add_subplot(gs[ct, 0])
        ax0.set_frame_on(False)
        ax0.get_xaxis().set_visible(False)
        ax0.get_yaxis().set_visible(False)
        fs = 8
        yi = 0.95
        tw = 47
        ax0.text(0, yi, '\n'.join(textwrap.wrap(description, width=tw)), size=fs, va='top')
        yi -= 0.125
        if len(description) > tw:
           yi -= 0.1 * np.floor(len(description)/tw)
        ax0.text(0, yi, 'ARM Name: ' + inst[ii].upper(), size=fs, va='top')
        yi -= 0.125
        ds_str = ds
        if dsname2 is not None:
            ds_str += ', ' + ds2
        ds_str = '\n'.join(textwrap.wrap(ds_str, width=tw))
            
        ax0.text(0, yi, 'Datastream: ' + ds_str, size=fs, va='top')
        yi -= 0.15
        if len(ds_str) > tw:
           yi -= 0.1 * np.floor(len(ds_str)/tw)
        ax0.text(0, yi, '\n'.join(textwrap.wrap(doi, width=tw)), va='top', size=fs)

        # Plot out the DA on the right plots
        newcmp = ListedColormap(['white', 'cornflowerblue', 'yellow', 'red'])
        ax1 = fig.add_subplot(gs[ct, 1:], rasterized=True)
        ax1.pcolormesh(c_dates, y_times, np.transpose(img), vmin=0, vmax=3,
                       cmap=newcmp, shading='flat', zorder=0, edgecolors='face')
        ax1.pcolor(c_dates, y_times, np.transpose(dqr_img), hatch='/', zorder=0, alpha=0)
        ax1.yaxis.set_major_locator(HourLocator(interval=6))
        ax1.yaxis.set_major_formatter(DateFormatter('%H:%M'))
        ax1.set_xlim([pd.to_datetime(c_start), pd.to_datetime(c_end) + pd.Timedelta('1 days')])

        ct += 1
        if ct == nrows:
            pdf_pages.savefig(fig)
            ct =  0
    pdf_pages.savefig(fig)
    pdf_pages.close()

    print(pd.Timestamp.now() - now)
